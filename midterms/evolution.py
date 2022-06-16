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
            genesis = self._ensure_previous_population(previous)
            offspring = self._reproduce_into_offspring_population(genesis, elitist=self.hyperparams.elitist_behaviour)
            for creature in tqdm(offspring.creatures):
                simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
            offspring_fitness = [
                EvolutionRecord.from_creature(creature, elite_from_previous=(creature == offspring.fittest if previous else False))
                for creature
                in offspring.creatures]
            return EvolutionGeneration(
                generation_id=generation_id,
                hyperparams=self.hyperparams,
                metrics=EvolutionMetrics.from_records(offspring_fitness, hyperparams=self.hyperparams),
                elite_previous=EvolutionRecord.from_creature(genesis.fittest, elite_from_previous=True) if previous else None,
                elite_offspring=EvolutionRecord.from_creature(offspring.fittest, elite_from_previous=False) if offspring else None,
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
            viable_creatures.append(previous.fittest)
        while len(viable_creatures) < self.hyperparams.population_size:
            adam, eve = previous.next_roulette_pair()
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
    dna_pool_entropy: float
    non_gene_bases: int
    genes_total: int
    genes_min: int
    genes_max: int
    genes_expressed: int
    genes_supressed: int

    @staticmethod
    def from_records(records: List["EvolutionRecord"], hyperparams: Hyperparams) -> "EvolutionMetrics":
        scores = pd.DataFrame([r.fitness_score for r in records if not r.elite_from_previous])
        dna_all = [Dna.parse_dna(r.dna_code) for r in records]
        dna_unique = [Dna.parse_dna(code) for code in set([r.dna_code for r in records])]
        dna_pool = list(itertools.chain(*[dna.code for dna in dna_all]))
        control_bases = list(itertools.chain(*[[gene.control_expression for gene in dna.genes] for dna in dna_all]))
        return EvolutionMetrics(
            fitness_mean=float(scores.mean()),
            fitness_p95=float(scores.quantile(0.95)),
            fitness_stdev=float(scores.std()),
            fitness_lowest=float(scores.min()),
            fitness_highest=float(scores.max()),
            dna_count_all=len(dna_all),
            dna_count_unique=len(dna_unique),
            dna_pool_entropy=entropy(dna_pool),
            non_gene_bases=sum([len(dna.code) % Gene.length() for dna in dna_all]),
            genes_total=sum([len(dna.genes) for dna in dna_all]),
            genes_max=max([len(dna.genes) for dna in dna_all]),
            genes_min=min([len(dna.genes) for dna in dna_all]),
            genes_expressed=sum(1 for cb in control_bases if cb >= hyperparams.expression_threshold),
            genes_supressed=sum(1 for cb in control_bases if cb < hyperparams.expression_threshold))


@dataclass(eq=True, frozen=True, order=True)
class EvolutionRecord:
    dna_code: str
    phenotype_count: int
    first_position: str
    last_position: str
    fitness_score: float
    elite_from_previous: bool = False

    @staticmethod
    def from_creature(creature: Creature, elite_from_previous: bool) -> "EvolutionRecord":
        return EvolutionRecord(
            dna_code=str(creature.dna),
            phenotype_count=len(creature.phenotypes),
            elite_from_previous=elite_from_previous,
            first_position=' '.join(str(x) for x in list(creature.movement.initial)),
            last_position=' '.join(str(x) for x in list(creature.movement.last)) if creature.movement.last else '0 0 0',
            fitness_score=creature.movement.distance)

    def extract_last_position_as_tuple(self) -> Tuple[float, float, float]:
        x, y, z = [float(d) for d in self.last_position.split(' ')]
        return (x, y, z)
