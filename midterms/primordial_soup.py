from typing import List

import itertools
import random

from gene import Gene


class PrimordialSoup:

    @staticmethod
    def spark_life(gene_count: int) -> List[float]:
        genes_code = [PrimordialSoup.spark_gene() for _ in range(gene_count)]
        genes_code += [[1. for _ in range(gene_count)]]
        dna_code = list(itertools.chain(*genes_code))
        return dna_code

    @staticmethod
    def spark_gene() -> List[float]:
        return [random.random() for _ in range(Gene.length())]
