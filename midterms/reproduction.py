from dataclasses import dataclass
from typing import List

import copy
import random

import numpy as np


@dataclass
class ReproductiveSettings:
    crossover_min_len = 0.25
    crossover_max_len = 0.75
    point_mutation_enabled: bool = True
    point_mutation_rate: float = 0.1
    point_mutation_amount: float = 0.1
    shrink_mutation_enabled: bool = True
    shrink_mutation_rate: float = 0.25
    grow_mutation_enabled: bool = True
    grow_mutation_rate: float = 0.1


@dataclass
class Reproduction:
    dna_code_a: List[float]
    dna_code_b: List[float]
    settings: ReproductiveSettings = ReproductiveSettings()

    def reproduce(self) -> List[float]:
        dna = self._crossover()
        if self.settings.point_mutation_enabled:
            dna = self._point_mutate(dna)
        return dna

    def _crossover(self) -> List[float]:
        x1_min = int(max(1, len(self.dna_code_a) * self.settings.crossover_min_len))
        x1_max = int(min(len(self.dna_code_a), len(self.dna_code_a) * self.settings.crossover_max_len))
        x2_min = int(max(1, len(self.dna_code_b) * self.settings.crossover_min_len))
        x2_max = int(min(len(self.dna_code_b), len(self.dna_code_b) * self.settings.crossover_max_len))
        x1 = random.randint(x1_min, x1_max)
        x2 = random.randint(x2_min, x2_max)
        g3 = np.concatenate([self.dna_code_a[:x1], self.dna_code_b[x2:]])
        return g3.tolist()

    def _point_mutate(self, before: List[float]) -> List[float]:
        after = copy.copy(before)
        for i in range(len(after)):
            if random.random() < self.settings.point_mutation_rate:
                after[i] += self.settings.point_mutation_amount
                after[i] = min(0.99999, after[i])
                after[i] = max(0.00001, after[i])
        return after
