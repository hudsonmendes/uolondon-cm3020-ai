from audioop import bias
from typing import List

import itertools
import random

from gene import Gene


class PrimordialSoup:

    @staticmethod
    def spark_life(gene_count: int) -> List[float]:
        genes = [PrimordialSoup.spark_gene() for _ in range(gene_count)]
        return list(itertools.chain(*genes))

    @staticmethod
    def spark_gene() -> List[float]:
        return [random.random() for _ in range(Gene.length())]
