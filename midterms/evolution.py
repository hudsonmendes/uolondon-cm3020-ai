from dataclasses import dataclass
from typing import List, Tuple, Optional

from hyperparams import Hyperparams
from creature import Creature
from population import Population
from simulation import Simulation


class Evolver:
    hyperparams: Hyperparams

    def __init__(self, hyperparams: Hyperparams):
        self.hyperparams = hyperparams

    def evolve(self, generation_id: int, based_on_generation_id: Optional[int] = None) -> "Evolution":
        adam, eve = self._read_elite_from(generation_id=based_on_generation_id)
        offspring = self._generate_offspring(adam, eve)
        fitness_map: List["EvolutionDnaFitness"] = []
        return Evolution(
            generation_id=generation_id,
            based_on_generation_id=based_on_generation_id,
            hyperparams=self.hyperparams,
            previous_elite=list([adam, eve]),
            offspring=offspring,
            fitness_map=fitness_map)

    def _read_elite_from(self, generation_id: Optional[int]) -> Tuple[List[float], List[float]]:
        if generation_id is None:
            gene_count = self.hyperparams.gene_count_on_genesis
            population = Population.generate_for(size=2, gene_count=gene_count)
            adam, eve = population.elite_duo
            return adam.dna.code, eve.dna.code
        raise NotImplementedError("Only Adam & Even generation available")

    def _generate_offspring(self, adam: List[float], eve:  List[float]) -> List[List[float]]:
        return []


@dataclass(eq=True, frozen=True, order=True)
class Evolution:
    generation_id: int
    based_on_generation_id: Optional[int]
    hyperparams: Hyperparams
    previous_elite: List[List[float]]
    offspring: List[List[float]]
    fitness_map: List["EvolutionDnaFitness"]


@dataclass(eq=True, frozen=True, order=True)
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
