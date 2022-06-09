from dataclasses import dataclass
from typing import List, Tuple, Union

import itertools

import phenotype


@dataclass
class Dna:
    """
    Holds the genetic code, and the information about
    Feature Genes (that may be expressed as phenotypes) and
    Control Genes (that will allow/disallow Feature genes to be expressed).
    """
    code: List[float]
    genes_features: List[List[float]]
    genes_control: List[bool]

    def express(self) -> List[phenotype.Phenotype]:
        """
        Expresses feature genes allowed by control genes.
        Suppressed feature genes may still be carried forward by elite Creatures.
        """
        expressed: List[List[float]] = []
        for feature, control in itertools.zip_longest(self.genes_features, self.genes_control):
            if control:
                expressed.append(feature)
        return [phenotype.Phenotype.parse_dna(dna) for dna in expressed]

    @staticmethod
    def parse_dna(data: Union[str, List[float]], gene_len: int = 1) -> "Dna":
        """
        Reads the DNA code and splits it into feature
        genes and control genes, producing an instance of DNA
        """
        assert data
        assert isinstance(data, str) or (isinstance(data, List) and isinstance(data[0], float))
        assert not isinstance(data, str) or len(data.split(',')) >= gene_len
        assert not isinstance(data, List) or len(data) >= gene_len
        dna_code = Dna._read_dna_code_from(data) if isinstance(data, str) else data
        features, controls = Dna._read_genes_from(dna_code, gene_len)
        return Dna(code=dna_code, genes_features=features, genes_control=controls)

    @staticmethod
    def _read_dna_code_from(data: str) -> List[float]:
        return [float(gene) for gene in data.split(',')]

    @staticmethod
    def _read_genes_from(dna_code: List[float], gene_len: int) -> Tuple[List[List[float]], List[bool]]:
        features: List[List[float]] = []
        controls: List[bool] = []
        i, end = 0, len(dna_code)
        while i < end:
            features.append(dna_code[i:i+gene_len])
            i += gene_len
            if len(dna_code) > 1:
                end -= 1
        for i in range(end, len(dna_code)):
            controls.append(dna_code[i] > 0.5)
        return features, controls
