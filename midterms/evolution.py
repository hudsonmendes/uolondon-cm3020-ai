from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import itertools

import pybullet as p
import pandas as pd
from tqdm import tqdm
from scipy.stats import entropy

from hyperparams import Hyperparams
from gene import Gene
from dna import Dna
from creature import Creature
from population import Population
from reproduction import Reproduction
from simulation import Simulation


class Evolver:
    """
    The Evolution Mechanism itself, responsible for iterating through to the
    next generation of population. Reponsible for collecting the `adam` and `eve`
    elite duo from the previous population, running reproduction against them,
    generating a new population and finally returning the fitness map for the offspring.
    """
    hyperparams: Hyperparams

    def __init__(self, hyperparams: Hyperparams):
        self.hyperparams = hyperparams

    def evolve(
            self,
            generation_id: int,
            previous: Optional[Population] = None) -> "EvolutionGeneration":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        with Simulation(connection_mode=p.DIRECT, hyperparams=self.hyperparams) as simulation:
            previous_fittest = previous.fittest if previous else None
            genesis = self._ensure_previous_population(previous)
            offspring = self._reproduce_into_offspring_population(genesis, elitist=self.hyperparams.elitist_behaviour)
            for creature in tqdm(offspring.creatures, desc=f"gen #{str(generation_id).rjust(3, '0')}"):
                simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
            offspring_fittest = offspring.fittest if offspring else None
            offspring_fitness = [
                EvolutionRecord.from_creature(creature, is_previous_fittest=(creature == previous_fittest))
                for creature
                in offspring.creatures]
            return EvolutionGeneration(
                generation_id=generation_id,
                hyperparams=self.hyperparams,
                metrics=EvolutionMetrics.from_records(offspring_fitness, hyperparams=self.hyperparams),
                elite_previous=EvolutionRecord.from_creature(previous_fittest, is_previous_fittest=True) if previous_fittest else None,
                elite_offspring=EvolutionRecord.from_creature(offspring_fittest, is_previous_fittest=False) if offspring_fittest else None,
                offspring_fitness=sorted(offspring_fitness, key=lambda of: of.fitness_score, reverse=True))

    def _ensure_previous_population(self, population: Optional[Population]) -> Population:
        if not population:
            population = Population.populate_for(
                size=2,
                gene_count=self.hyperparams.gene_count_genesis,
                threshold_for_expression=self.hyperparams.expression_threshold)
        return population

    def _reproduce_into_offspring_population(self, previous: Population, elitist: bool) -> Population:
        reproduction = Reproduction(self.hyperparams)
        viable_creatures: List[Creature] = []
        creatures_without_previous_elite: List[Creature] = []
        if elitist:
            fittest = previous.fittest
            if fittest:
                viable_creatures.append(fittest)
        while len(viable_creatures) < self.hyperparams.population_size:
            adam, eve = previous.next_roulette_pair()
            if adam and eve:
                new = reproduction.reproduce(adam.dna.code, eve.dna.code)
                child = Creature.develop_from(dna=Dna.parse_dna(new), threshold_for_expression=self.hyperparams.expression_threshold)
                if child:
                    creatures_without_previous_elite.append(child)
                    viable_creatures.append(child)
        return Population(viable_creatures)


@dataclass(eq=True, frozen=True, order=True)
class EvolutionGeneration:
    """
    Keeps record of the evolution, so it can be persisted, loaded and parsed
    into other components such as Population and Fitness data.
    """
    generation_id: int
    hyperparams: Hyperparams
    metrics: "EvolutionMetrics"
    elite_previous: Optional["EvolutionRecord"] = None
    elite_offspring: Optional["EvolutionRecord"] = None
    offspring_fitness: Optional[List["EvolutionRecord"]] = None

    def to_population(self) -> Population:
        """
        Turns the offpsring information into a population that can be used
        as parents of a new offspring.
        """
        creatures: List[Creature] = []
        if self.offspring_fitness:
            for fitness in self.offspring_fitness:
                creature = Creature.develop_from(
                    dna=Dna.parse_dna(fitness.dna_code),
                    threshold_for_expression=self.hyperparams.expression_threshold)
                if creature:
                    creature.movement.track(fitness.extract_last_position_as_tuple())
                    creature.movement.lethal_move = fitness.died_during_motion
                    if not creature.movement.lethal_move:
                        creatures.append(creature)
        return Population(creatures)


@dataclass(eq=True, frozen=True, order=True)
class EvolutionMetrics:
    fitness_mean: float
    fitness_p95: float
    fitness_stdev: float
    fitness_lowest: float
    fitness_highest: float
    dna_count_all: int
    dna_count_unique: int
    entropy_dna_pool: float
    entropy_fitness_scores: float
    bases_not_in_genes: int
    genes_total: int
    genes_min: int
    genes_max: int
    genes_expressed: int
    genes_supressed: int
    creatures_survived: int
    creatures_dead: int

    @staticmethod
    def from_records(records: List["EvolutionRecord"], hyperparams: Hyperparams) -> "EvolutionMetrics":
        scores = [r.fitness_score for r in records if not r.is_elite_from_previous and not r.died_during_motion]
        scores_df = pd.DataFrame(scores)
        dna_all = [Dna.parse_dna(r.dna_code) for r in records]
        dna_unique = [Dna.parse_dna(code) for code in set([r.dna_code for r in records])]
        dna_pool = list(itertools.chain(*[dna.code for dna in dna_all]))
        control_bases = list(itertools.chain(*[[gene.control_expression for gene in dna.genes] for dna in dna_all]))
        return EvolutionMetrics(
            fitness_mean=float(scores_df.mean()),
            fitness_p95=float(scores_df.quantile(0.95)),
            fitness_stdev=float(scores_df.std()),
            fitness_lowest=float(scores_df.min()),
            fitness_highest=float(scores_df.max()),
            dna_count_all=len(dna_all),
            dna_count_unique=len(dna_unique),
            entropy_dna_pool=entropy(dna_pool),
            entropy_fitness_scores=entropy(scores),
            bases_not_in_genes=sum([len(dna.code) % Gene.length() for dna in dna_all]),
            genes_total=sum([len(dna.genes) for dna in dna_all]),
            genes_max=max([len(dna.genes) for dna in dna_all]),
            genes_min=min([len(dna.genes) for dna in dna_all]),
            genes_expressed=sum(1 for cb in control_bases if cb >= hyperparams.expression_threshold),
            genes_supressed=sum(1 for cb in control_bases if cb < hyperparams.expression_threshold),
            creatures_survived=len([r for r in records if not r.died_during_motion]),
            creatures_dead=len([r for r in records if r.died_during_motion]))


@dataclass(eq=True, frozen=True, order=True)
class EvolutionRecord:
    dna_code: str
    phenotype_count: int
    first_position: str
    last_position: str
    fitness_score: float
    is_elite_from_previous: bool = False
    died_during_motion: bool = False

    @staticmethod
    def from_creature(creature: Creature, is_previous_fittest: bool) -> "EvolutionRecord":
        return EvolutionRecord(
            dna_code=str(creature.dna),
            phenotype_count=len(creature.phenotypes),
            is_elite_from_previous=is_previous_fittest,
            died_during_motion=creature.movement.lethal_move,
            first_position=' '.join(str(x) for x in list(creature.movement.initial)),
            last_position=' '.join(str(x) for x in list(creature.movement.last)) if creature.movement.last else '0 0 0',
            fitness_score=creature.movement.distance)

    def extract_last_position_as_tuple(self) -> Tuple[float, float, float]:
        x, y, z = [float(d) for d in self.last_position.split(' ')]
        return (x, y, z)
