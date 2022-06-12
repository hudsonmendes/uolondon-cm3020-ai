from dataclasses import dataclass
from distutils.ccompiler import gen_preprocess_options
from typing import List, Tuple, Optional

import pybullet as p

from fitness import Fitness, FitnessTracker
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

    def __init__(self, hyperparams: Hyperparams, fitness: Fitness):
        self.hyperparams = hyperparams
        self.fitness = fitness

    def evolve(
            self,
            generation_id: int,
            genesis: Optional[Population] = None) -> "Evolution":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        simulation = Simulation(connection_mode=p.DIRECT)
        genesis = self._ensure_previous_population(genesis)
        offspring = self._reproduce_into_offspring_population(genesis)
        for creature in offspring.creatures:
            simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            elite_previous=str(self.fitness.calculate_fittest_from(genesis).dna),
            elite_offspring=str(self.fitness.calculate_fittest_from(offspring).dna),
            offspring_fitness=[EvolutionDnaFitness.from_tracker(tracker) for tracker in self.fitness.trackers_for(offspring)])

    def _ensure_previous_population(self, population: Optional[Population]) -> Population:
        if not population:
            population = Population.populate_for(size=2, gene_count=self.hyperparams.gene_count)
        return population

    def _reproduce_into_offspring_population(self, previous: Population) -> Population:
        reproduction = Reproduction(self.hyperparams)
        viable_creatures: List[Creature] = []
        while len(viable_creatures) < self.hyperparams.population_size:
            adam, eve = self.fitness.next_roullete_pair_from(previous)
            new = reproduction.reproduce(adam.dna.code, eve.dna.code)
            child = Creature.develop_from(dna=Dna.parse_dna(new))
            if child:
                viable_creatures.append(child)
        return Population(viable_creatures)


@dataclass(eq=True, frozen=True, order=True)
class Evolution:
    """
    Keeps record of the evolution, so it can be persisted, loaded and parsed
    into other components such as Population and Fitness data.
    """
    generation_id: int
    hyperparams: Hyperparams
    elite_previous: str
    elite_offspring: str
    offspring_fitness: List["EvolutionDnaFitness"]

    def to_population(self) -> Population:
        """
        Turns the offpsring information into a population that can be used
        as parents of a new offspring.
        """
        creatures: List[Creature] = []
        for fitness in self.offspring_fitness:
            creature = Creature.develop_from(dna=Dna.parse_dna(fitness.dna_code))
            if creature:
                creature.tracker.track(fitness.extract_last_position_as_tuple())
                creatures.append(creature)
        return Population(creatures)


@dataclass(eq=True, frozen=True, order=True)
class EvolutionDnaFitness:
    dna_code: str
    first_position: str
    last_position: str
    fitness_score: float

    @staticmethod
    def from_tracker(tracker: FitnessTracker) -> "EvolutionDnaFitness":
        return EvolutionDnaFitness(
            dna_code=str(tracker.creature.dna),
            first_position=' '.join(str(x) for x in list(tracker.initial)),
            last_position=' '.join(str(x) for x in list(tracker.last)) if tracker.last else '0 0 0',
            fitness_score=tracker.distance_travelled)

    def extract_last_position_as_tuple(self) -> Tuple[float, float, float]:
        x, y, z = [float(d) for d in self.last_position.split(' ')]
        return (x, y, z)
