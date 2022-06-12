from dataclasses import dataclass
from typing import List, Optional

import pybullet as p

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
            previous_population: Optional[Population] = None) -> "Evolution":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        previous = self._ensure_previous_population(previous_population)
        offspring = self._reproduce_into_offspring_population(previous)
        simulation = Simulation(connection_mode=p.DIRECT, population=offspring)
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            elite_previous=previous.elite_duo,
            elite_offspring=[child.dna.code for child in offspring.roulet_pair],
            offspring=[child.dna.code for child in offspring.creatures])

    def _ensure_previous_population(self, population: Optional[Population]) -> Population:
        if not population:
            population = Population.generate_for(size=2, gene_count=self.hyperparams.gene_count_on_genesis)
        return population

    def _reproduce_into_offspring_population(self, population: Population) -> Population:
        reproduction = Reproduction(self.hyperparams)
        viable_creatures: List[Creature] = []
        while len(viable_creatures) < self.hyperparams.population_size:
            dna_code = reproduction.reproduce(adam.dna.code, eve.dna.code)
            creature = Creature.develop_from(dna=Dna.parse_dna(dna_code))
            if creature:
                viable_creatures.append(creature)
        return Population(creatures=viable_creatures)


@dataclass(eq=True, frozen=True, order=True)
class Evolution:
    generation_id: int
    hyperparams: Hyperparams
    elite_previous: List[List[float]]
    elite_offspring: List[List[float]]
    offspring_fitness: List["EvolutionDnaFitness"]


@dataclass(eq=True, frozen=True, order=True)
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
