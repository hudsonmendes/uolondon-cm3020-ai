from dataclasses import dataclass
from typing import List, Optional

from pathlib import Path

import pybullet as p

from creature import Creature
from population import Population
from simulation import Simulation
from primordial_soup import PrimordialSoup
from reproduction import ReproductiveSettings


@dataclass
class EvolutionHyperparameters:
    population_count: int
    generation_steps: int = 2400
    reproduction_settings: ReproductiveSettings = ReproductiveSettings()

class Evolution:
    hyperparams: EvolutionHyperparameters

    def __init__(self, hyperparams: EvolutionHyperparameters):
        self.hyperparams = hyperparams

    def evolve(self, generations: int, genesis_generation: Optional[int] = 0):
        genesis = None
        if genesis_generation is None or genesis_generation < 0:
            genesis_generation = 0
            genesis = EvolutionResult()
        else:
            pass
            

        for generation_id in range(genesis_generation, generations):
            population = Population(generation_id=generation_id)
            simulation = Simulation(connection_mode=p.DIRECT, population=population)
            simulation.simulate(
                species_name="generation-{generation_id}",
                dna_code=PrimordialSoup.spark_life(gene_count=10),
                steps=self.hyperparams.generation_steps)

@dataclass
class EvolutionResult:
    fitness: List["EvolutionResultItem"]

    @staticmethod
    def read_from_disk(folder: Path, generation_id: int) -> "EvolutionResult":
        with open(folder / f'generation-{id}.results') as fh:
            return EvolutionResult()

@dataclass
class EvolutionResultItem:
    creature_dna_code: List[float]
    fitness_score: float