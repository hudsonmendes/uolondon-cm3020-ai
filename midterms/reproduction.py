from dataclasses import dataclass
from typing import List

import copy
import random

import numpy as np

from gene import Gene


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
    settings: ReproductiveSettings = ReproductiveSettings()

    def reproduce(self, a: List[float], b: List[float]) -> List[float]:
        dna_code = self._crossover(np.array(a), np.array(b))
        if self.settings.point_mutation_enabled:
            dna_code = self._point_mutate(dna_code)
        if self.settings.shrink_mutation_enabled:
            dna_code = self._mutate_shrink(dna_code)
        if self.settings.grow_mutation_enabled:
            dna_code = self._mutate_shrink(dna_code)
        return dna_code.tolist()

    def _crossover(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a_min = int(max(1, len(a) * self.settings.crossover_min_len))
        a_max = int(min(len(a), len(a) * self.settings.crossover_max_len))
        a_cut = random.randint(a_min, a_max)
        b_min = int(max(1, len(b) * self.settings.crossover_min_len))
        b_max = int(min(len(b), len(b) * self.settings.crossover_max_len))
        b_cut = random.randint(b_min, b_max)
        child_code = np.concatenate([a[:a_cut], b[b_cut:]])
        return child_code

    def _point_mutate(self, before: np.ndarray) -> np.ndarray:
        after = before.copy()
        for i in range(len(after)):
            if random.random() < self.settings.point_mutation_rate:
                after[i] += self.settings.point_mutation_amount
                after[i] = min(0.99999, after[i])
                after[i] = max(0.00001, after[i])
        return after

    def _mutate_shrink(self, before: np.ndarray) -> np.ndarray:
        after = before.copy()
        if len(after) > Gene.length():
            to_remove: List[int] = []
            for i in range(len(after)):
                if len(after) - len(to_remove) <= Gene.length():
                    break
                if random.random() < self.settings.shrink_mutation_rate:
                    to_remove.append(i)
            for i in reversed(to_remove):
                after = np.delete(after, i, 0)
        return after

    def _mutate_grow(self, before: np.ndarray) -> np.ndarray:
        after = before.copy()
        growth = int(len(after) * self.settings.grow_mutation_rate)
        if growth:
            new_bases = np.random.rand(growth)
            after = np.concatenate([after, new_bases])
        return after
