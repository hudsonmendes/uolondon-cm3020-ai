from dataclasses import dataclass
from typing import List, Optional

from hyperparams import Hyperparams
from dna import Dna
from creature import Creature
from population import Population
from reproduction import Reproduction


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
        adam, eve = self._ensure_previous_population(previous_population).elite_duo
        offspring = self._reproduce_into_offspring_population(adam, eve)
        fitness_map: List["EvolutionDnaFitness"] = []
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            elite_previous=[adam.dna.code, eve.dna.code],
            elite_offspring=[child.dna.code for child in offspring.elite_duo],
            offspring=[child.dna.code for child in offspring.creatures],
            fitness_map=fitness_map)

    def _ensure_previous_population(self, previous_population: Optional[Population]) -> Population:
        if not previous_population:
            previous_population = Population.generate_for(size=2, gene_count=self.hyperparams.gene_count_on_genesis)
        return previous_population

    def _reproduce_into_offspring_population(self, adam: Creature, eve: Creature) -> Population:
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
    offspring: List[List[float]]
    fitness_map: List["EvolutionDnaFitness"]


@dataclass(eq=True, frozen=True, order=True)
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
