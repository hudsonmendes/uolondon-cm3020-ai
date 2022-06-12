from dataclasses import dataclass
from typing import List, Optional

from hyperparams import Hyperparams
from creature import Creature
from population import Population
from simulation import Simulation
from primordial_soup import PrimordialSoup


class Evolution:
    hyperparams: Hyperparams

    def __init__(self, hyperparams: Hyperparams):
        self.hyperparams = hyperparams

    def evolve(self, generation_id: int) -> "EvolutionRecord":
        fitness_map: List["EvolutionRecordDnaFitness"] = []
        return EvolutionRecord(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            fitness_map=fitness_map)


@dataclass
class EvolutionRecord:
    generation_id: int
    hyperparams: Hyperparams
    fitness_map: List["EvolutionRecordDnaFitness"]


@dataclass
class EvolutionRecordDnaFitness:
    dna_code: List[float]
    fitness_score: float
