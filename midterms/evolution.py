from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import pybullet as p
import pandas as pd
from tqdm import tqdm

from hyperparams import Hyperparams
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
            previous: Optional[Population] = None) -> "Evolution":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        with Simulation(connection_mode=p.DIRECT) as simulation:
            genesis = self._ensure_previous_population(previous)
            genesis_elite = EvolutionRecord.from_creature(genesis.fittest) if previous else None
            offspring = self._reproduce_into_offspring_population(genesis, elitist=self.hyperparams.elitist_behaviour)
            for creature in tqdm(offspring.creatures):
                simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
            offspring_fitness = [EvolutionRecord.from_creature(creature) for creature in offspring.creatures]
            return Evolution(
                generation_id=generation_id,
                hyperparams=self.hyperparams,
                elite_previous=genesis_elite,
                elite_offspring=EvolutionRecord.from_creature(offspring.fittest) if offspring else None,
                fitness_p95=Evolver._calculate_fitness_p95(offspring_fitness, previous_elite=genesis_elite),
                offspring_fitness=sorted(offspring_fitness, key=lambda of: of.fitness_score, reverse=True))

    def _ensure_previous_population(self, population: Optional[Population]) -> Population:
        if not population:
            population = Population.populate_for(size=2, gene_count=self.hyperparams.gene_count)
        return population

    def _reproduce_into_offspring_population(self, previous: Population, elitist: bool) -> Population:
        reproduction = Reproduction(self.hyperparams)
        viable_creatures: List[Creature] = []
        if elitist:
            viable_creatures.append(previous.fittest)
        while len(viable_creatures) < self.hyperparams.population_size:
            adam, eve = previous.next_roulette_pair()
            new = reproduction.reproduce(adam.dna.code, eve.dna.code)
            child = Creature.develop_from(dna=Dna.parse_dna(new), threshold_for_expression=self.hyperparams.expression_threshold)
            if child:
                viable_creatures.append(child)
        return Population(viable_creatures)

    @staticmethod
    def _calculate_fitness_p95(offspring_fitness: List["EvolutionRecord"], previous_elite: "EvolutionRecord") -> float:
        if offspring_fitness:
            scores = [f.fitness_score for f in offspring_fitness if not previous_elite or f.dna_code != previous_elite.dna_code]
            return float(pd.DataFrame(scores).quantile(0.95))
        else:
            return 0.


@dataclass(eq=True, frozen=True, order=True)
class Evolution:
    """
    Keeps record of the evolution, so it can be persisted, loaded and parsed
    into other components such as Population and Fitness data.
    """
    generation_id: int
    hyperparams: Hyperparams
    elite_previous: Optional["EvolutionRecord"] = None
    elite_offspring: Optional["EvolutionRecord"] = None
    fitness_p95: Optional[float] = 0.
    offspring_fitness: Optional[List["EvolutionRecord"]] = None

    def to_population(self) -> Population:
        """
        Turns the offpsring information into a population that can be used
        as parents of a new offspring.
        """
        creatures: List[Creature] = []
        if self.offspring_fitness:
            for fitness in self.offspring_fitness:
                creature = Creature.develop_from(dna=Dna.parse_dna(fitness.dna_code))
                if creature:
                    creature.movement.track(fitness.extract_last_position_as_tuple())
                    creatures.append(creature)
        return Population(creatures)


@dataclass(eq=True, frozen=True, order=True)
class EvolutionRecord:
    dna_code: str
    phenotype_count: int
    first_position: str
    last_position: str
    fitness_score: float

    @staticmethod
    def from_creature(creature: Creature) -> "EvolutionRecord":
        return EvolutionRecord(
            dna_code=str(creature.dna),
            phenotype_count=len(creature.phenotypes),
            first_position=' '.join(str(x) for x in list(creature.movement.initial)),
            last_position=' '.join(str(x) for x in list(creature.movement.last)) if creature.movement.last else '0 0 0',
            fitness_score=creature.movement.distance)

    def extract_last_position_as_tuple(self) -> Tuple[float, float, float]:
        x, y, z = [float(d) for d in self.last_position.split(' ')]
        return (x, y, z)
