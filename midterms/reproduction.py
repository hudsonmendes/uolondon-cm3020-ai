from typing import List

import random

import numpy as np


class Reproduction:
    dna_code_a: List[float]
    dna_code_b: List[float]

    def __init__(
            self,
            dna_code_a: List[float],
            dna_code_b: List[float]) -> None:
        self.dna_code_a = dna_code_a
        self.dna_code_b = dna_code_b

    def reproduce(self) -> List[float]:
        dna = self._crossover()
        return dna

    def _crossover(self) -> List[float]:
        x1 = random.randint(1, len(self.dna_code_a)-1)
        x2 = random.randint(1, len(self.dna_code_b)-1)
        g3 = np.concatenate([self.dna_code_a[:x1], self.dna_code_b[x2:]])
        return g3.tolist()
