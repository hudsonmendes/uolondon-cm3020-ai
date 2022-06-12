from dataclasses import dataclass
from distutils.ccompiler import gen_preprocess_options
from typing import List, Optional

import pybullet as p
from fitness import Fitness

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
            genesis: Optional[Population] = None) -> "Evolution":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        fitness = Fitness()
        simulation = Simulation(connection_mode=p.DIRECT, fitness=fitness)
        genesis = self._ensure_previous_population(genesis)
        offspring = self._reproduce_into_offspring_population(genesis, fitness)
        for creature in offspring.creatures:
            simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            elite_previous=str(fitness.calculate_fittest_from(genesis).dna),
            elite_offspring=str(fitness.calculate_fittest_from(offspring).dna),
            offspring_fitness=[
                EvolutionDnaFitness(
                    dna_code=str(child.dna),
                    fitness_score=fitness.tracker_for(child).distance_travelled)
                for child
                in offspring.creatures])

    def _ensure_previous_population(self, population: Optional[Population]) -> Population:
        if not population:
            population = Population.populate_for(size=2, gene_count=self.hyperparams.gene_count)
        return population

    def _reproduce_into_offspring_population(self, previous: Population, fitness: Fitness) -> Population:
        reproduction = Reproduction(self.hyperparams)
        viable_creatures: List[Creature] = []
        while len(viable_creatures) < self.hyperparams.population_size:
            adam, eve = fitness.next_roullete_pair_from(previous)
            new = reproduction.reproduce(adam.dna.code, eve.dna.code)
            child = Creature.develop_from(dna=Dna.parse_dna(new))
            if child:
                viable_creatures.append(child)
        return Population(viable_creatures)


@dataclass(eq=True, frozen=True, order=True)
class Evolution:
    generation_id: int
    hyperparams: Hyperparams
    elite_previous: str
    elite_offspring: str
    offspring_fitness: List["EvolutionDnaFitness"]


@dataclass(eq=True, frozen=True, order=True)
class EvolutionDnaFitness:
    dna_code: str
    fitness_score: float
