from dataclasses import dataclass
from typing import List, Tuple, Union

import itertools

from phenotype import Phenotype
from gene import Gene


@dataclass
class Dna:
    """
    Holds the genetic code, and the information about
    Feature Genes (that may be expressed as phenotypes) and
    Control Genes (that will allow/disallow Feature genes to be expressed).
    """
    code: List[float]
    genes_features: List[Gene]
    genes_control: List[bool]

    def express(self) -> List[Phenotype]:
        """
        Expresses feature genes allowed by control genes.
        Suppressed feature genes may still be carried forward by elite Creatures.
        """
        expressed: List[Gene] = []
        for feature, control in itertools.zip_longest(self.genes_features, self.genes_control):
            if control is None or control == True:
                expressed.append(feature)
        return [
            Phenotype.parse_dna(gene=gene, gene_count=i+1)
            for i, gene
            in enumerate(expressed)]

    @staticmethod
    def parse_dna(data: Union[str, List[float]]) -> "Dna":
        """
        Reads the DNA code and splits it into feature
        genes and control genes, producing an instance of DNA
        """
        assert data
        assert isinstance(data, str) or (isinstance(data, List) and isinstance(data[0], float))
        assert not isinstance(data, str) or len(data.split(',')) >= Gene.length()
        assert not isinstance(data, List) or len(data) >= Gene.length()
        dna_code = Dna._read_dna_code_from(data) if isinstance(data, str) else data
        features, controls = Dna._read_genes_from(dna_code)
        return Dna(code=dna_code, genes_features=features, genes_control=controls)

    @staticmethod
    def _read_dna_code_from(data: str) -> List[float]:
        return [float(gene) for gene in data.split(',')]

    @staticmethod
    def _read_genes_from(dna_code: List[float]) -> Tuple[List[Gene], List[bool]]:
        features: List[Gene] = []
        controls: List[bool] = []
        i, end = 0, len(dna_code)
        while i < end:
            dna_segment = dna_code[i:i+Gene.length()]
            features.append(Gene(code=dna_segment))
            i += Gene.length()
            if len(dna_code) % Gene.length() > 0:
                end -= 1
        for i in range(end, len(dna_code)):
            controls.append(dna_code[i] > 0.5)
        return features, controls
