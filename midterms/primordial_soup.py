from audioop import bias
from typing import List

import itertools
import random

from gene import Gene


class PrimordialSoup:

    @staticmethod
    def spark_life(gene_count: int, bias_to_expression: float = 0.7) -> List[float]:
        genes = [PrimordialSoup.spark_gene() for _ in range(gene_count)]
        genes = PrimordialSoup._ensure_genes_minimum_expression(genes, bias_to_expression)
        return list(itertools.chain(*genes))

    @staticmethod
    def spark_gene() -> List[float]:
        return [random.random() for _ in range(Gene.length())]

    @staticmethod
    def _ensure_genes_minimum_expression(genes: List[List[float]], bias_to_expression: float) -> List[List[float]]:
        for gene in genes:
            if gene[-1] < Gene.threshold_for_expression() and random.random() >= (1. - bias_to_expression):
                gene[-1] = min(1., gene[-1] + Gene.threshold_for_expression())
        return genes
