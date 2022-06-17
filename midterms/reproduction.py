from dataclasses import dataclass
from typing import List

import random

import numpy as np

from hyperparams import Hyperparams
from gene import Gene


@dataclass(eq=True, frozen=True, order=True)
class Reproduction:
    hyperparams: Hyperparams

    def reproduce(self, a: List[float], b: List[float]) -> List[float]:
        dna_code = self._crossover(np.array(a), np.array(b))
        dna_code = self._point_mutate(dna_code)
        dna_code = self._mutate_shrink(dna_code)
        dna_code = self._mutate_grow(dna_code)
        dna_code = self._clip_dna_len(dna_code)
        return dna_code.tolist()

    def _crossover(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        full = max(len(a), len(b))
        min_len = Gene.length() // 2
        cut_min, cut_max = int(full * 0.25), int(full * 0.75)
        cut = random.randint(cut_min, cut_max)
        cut_a, cut_b = min(cut, len(a) - min_len), min(cut, len(b) - min_len)
        child_code = np.concatenate([a[:cut_a], b[cut_b:]])
        return child_code

    def _point_mutate(self, before: np.ndarray) -> np.ndarray:
        after = before.copy()
        for i in range(len(after)):
            if random.random() < self.hyperparams.point_mutation_rate:
                after[i] += self.hyperparams.point_mutation_amount
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
                if random.random() < self.hyperparams.shrink_mutation_rate:
                    to_remove.append(i)
            for i in reversed(to_remove):
                after = np.delete(after, i, 0)
        return after

    def _mutate_grow(self, before: np.ndarray) -> np.ndarray:
        after = before.copy()
        growth = int(len(after) * self.hyperparams.grow_mutation_rate)
        if growth:
            new_bases = np.random.rand(growth)
            after = np.concatenate([after, new_bases])
        return after

    def _clip_dna_len(self, dna_code: np.ndarray) -> np.ndarray:
        gen_count_max = self.hyperparams.gene_count_max
        max_len = gen_count_max * Gene.length()
        if len(dna_code) > max_len:
            dna_code = dna_code[:max_len]
        return dna_code
