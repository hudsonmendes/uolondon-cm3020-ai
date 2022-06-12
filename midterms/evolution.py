from dataclasses import dataclass
from distutils.ccompiler import gen_preprocess_options
from typing import List, Tuple, Optional

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
            previous: Optional[Population] = None) -> "Evolution":
        """
        Runs the next generation of evolution.
        :param generation_id {int}: the unique identifier of the generation, used for record keeping
        :param previous_population {Population}: if we are seeding the original population from persistence, uses that instead of generating a random one.
        """
        simulation = Simulation(connection_mode=p.DIRECT)
        genesis = self._ensure_previous_population(previous)
        offspring = self._reproduce_into_offspring_population(genesis, elitist=self.hyperparams.elitist_behaviour)
        for creature in offspring.creatures:
            simulation.simulate(creature, steps=self.hyperparams.simulation_steps)
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            elite_previous=str(genesis.fittest.dna) if previous else None,
            elite_offspring=str(offspring.fittest.dna),
            offspring_fitness=[EvolutionDnaFitness.from_creature(creature) for creature in offspring.creatures])

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
    elite_previous: Optional[str] = None
    elite_offspring: Optional[str] = None
    offspring_fitness: Optional[List["EvolutionDnaFitness"]] = None

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
class EvolutionDnaFitness:
    dna_code: str
    first_position: str
    last_position: str
    fitness_score: float

    @staticmethod
    def from_creature(creature: Creature) -> "EvolutionDnaFitness":
        return EvolutionDnaFitness(
            dna_code=str(creature.dna),
            first_position=' '.join(str(x) for x in list(creature.movement.initial)),
            last_position=' '.join(str(x) for x in list(creature.movement.last)) if creature.movement.last else '0 0 0',
            fitness_score=creature.movement.distance)

    def extract_last_position_as_tuple(self) -> Tuple[float, float, float]:
        x, y, z = [float(d) for d in self.last_position.split(' ')]
        return (x, y, z)
