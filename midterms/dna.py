from dataclasses import dataclass
from typing import List, Tuple


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

    def express(self) -> List[List[float]]:
        """
        Expresses feature genes allowed by control genes.
        Suppressed feature genes may still be carried forward by elite Creatures.
        """
        expressed: List[List[float]] = []
        for feature, control in zip(self.genes_features, self.genes_control):
            if control:
                expressed.append(feature)
        return expressed

    @staticmethod
    def read(data: str, gene_len: int = 1) -> "Dna":
        """
        Reads the DNA code and splits it into feature
        genes and control genes, producing an instance of DNA
        """
        assert data and len(data.split(',')) > gene_len
        dna_code = Dna._read_dna_code_from(data)
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
            end -= 1
        for i in range(end, len(dna_code)):
            controls.append(dna_code[i] > 0.5)
        return features, controls
