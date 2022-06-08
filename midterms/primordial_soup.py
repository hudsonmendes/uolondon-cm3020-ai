from typing import Optional

import random

import dna


class PrimordialSoup:
    organic_molecule_len: int

    def __init__(self, organic_molecule_len: int) -> None:
        self.organic_molecule_len = organic_molecule_len

    def spark_life(self) -> dna.Dna:
        dna_code = [random.random() for _ in range(self.organic_molecule_len)]
        dna_data = ",".join([str(base) for base in dna_code])
        gene_len = self.organic_molecule_len - 1 if self.organic_molecule_len > 1 else 1
        return dna.Dna.parse(dna_data, gene_len=gene_len)
