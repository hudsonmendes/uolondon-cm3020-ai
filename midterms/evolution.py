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

    def evolve(self, generation_id: int) -> "Evolution":
        previous_elite: List[List[float]]
        offspring: List[List[float]]
        fitness_map: List["EvolutionDnaFitness"] = []
        return Evolution(
            generation_id=generation_id,
            hyperparams=self.hyperparams,
            previous_elite=previous_elite,
            offspring=offspring,
            fitness_map=fitness_map)


@dataclass
class Evolution:
    generation_id: int
    hyperparams: Hyperparams
    previous_elite: List[List[float]]
    offspring: List[List[float]]
    fitness_map: List["EvolutionDnaFitness"]


@dataclass
class EvolutionDnaFitness:
    dna_code: List[float]
    fitness_score: float
