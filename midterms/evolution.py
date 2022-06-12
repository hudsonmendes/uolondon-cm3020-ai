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

    def evolve(self, generation_id: Optional[int]) -> List["EvolutionDnaFitness"]:
        return []


@dataclass
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
