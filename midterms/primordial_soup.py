from audioop import bias
from typing import List

import itertools
import random

from gene import Gene


class PrimordialSoup:

    @staticmethod
    def spark_life(gene_count: int, bias_to_expression: float = 0.7) -> List[float]:
        features_code = [PrimordialSoup._spark_gene() for _ in range(gene_count)]
        controls_code = [PrimordialSoup._spark_controls(gene_count, bias_to_expression)]
        dna_code = list(itertools.chain(*(features_code + controls_code)))
        return dna_code

    @staticmethod
    def _spark_gene() -> List[float]:
        return [random.random() for _ in range(Gene.length())]

    @staticmethod
    def _spark_controls(gene_count: int, bias_to_expression: float) -> List[float]:
        expression_threshold = 0.5
        controls = [random.random() for _ in range(gene_count)]
        for i, control in enumerate(controls):
            threshold = 1. - bias_to_expression
            if control < expression_threshold and random.random() >= threshold:
                controls[i] = min(1., 0.5 + control)
        if not any([base > expression_threshold for base in controls]):
            i = random.randint(0, gene_count)
            controls[i] = min(1., 0.5 + controls[i])
        return controls
