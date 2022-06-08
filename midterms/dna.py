from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Dna:
    code: List[float]
    genes: List[List[float]]
    controls: List[bool]

    @staticmethod
    def read(data: str, gene_len: int = 1) -> "Dna":
        dna_code = Dna._read_dna_code_from(data)
        genes, controls = Dna._read_genes_from(dna_code, gene_len)
        return Dna(code=dna_code, genes=genes, controls=controls)

    @staticmethod
    def _read_dna_code_from(data: str) -> List[float]:
        assert data
        return [float(gene) for gene in data.split(',')]

    @staticmethod
    def _read_genes_from(dna_code: List[float], gene_len: int) -> Tuple[List[List[float]], List[bool]]:
        assert len(dna_code) > gene_len
        genes: List[List[float]] = []
        controls: List[bool] = []
        i: int = 0
        end: int = len(dna_code)
        while i < end:
            genes.append(dna_code[i:i+gene_len])
            i += gene_len
            end -= 1
        return genes, controls
