from dataclasses import dataclass
from typing import List, Optional

from hyperparams import Hyperparams
from creature import Creature
from population import Population
from simulation import Simulation
from primordial_soup import PrimordialSoup


class Evolver:
    hyperparams: Hyperparams

    def __init__(self, hyperparams: Hyperparams):
        self.hyperparams = hyperparams

    def evolve(self, generation_id: int, based_on_generation_id: Optional[int] = None) -> "Evolution":
        previous_elite = self._read_elite_from(generation_id=based_on_generation_id)
        offspring: List[List[float]] = []
        fitness_map: List["EvolutionDnaFitness"] = []
        return Evolution(
            generation_id=generation_id,
            based_on_generation_id=based_on_generation_id,
            hyperparams=self.hyperparams,
            previous_elite=previous_elite,
            offspring=offspring,
            fitness_map=fitness_map)

    def _read_elite_from(self, generation_id: Optional[int]) -> List[List[float]]:
        elite: List[List[float]] = []
        if generation_id is None:
            genesis_gene_count = self.hyperparams.gene_count_on_genesis
            elite.append(PrimordialSoup.spark_life(gene_count=genesis_gene_count))
            elite.append(PrimordialSoup.spark_life(gene_count=genesis_gene_count))
        return elite


@dataclass
class Evolution:
    generation_id: int
    based_on_generation_id: Optional[int]
    hyperparams: Hyperparams
    previous_elite: List[List[float]]
    offspring: List[List[float]]
    fitness_map: List["EvolutionDnaFitness"]


@dataclass
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
