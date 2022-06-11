from dataclasses import dataclass
from typing import List, Union

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
    genes: List[Gene]

    def express(self) -> List[Phenotype]:
        """
        Expresses feature genes allowed by control genes.
        Suppressed feature genes may still be carried forward by elite Creatures.
        """
        expressed: List[Gene] = []
        for gene in self.genes:
            if gene.control_expression > Gene.threshold_for_exrpession():
                expressed.append(gene)
        return [
            Phenotype.parse_dna(gene=gene, gene_count=i+1)
            for i, gene
            in enumerate(expressed)]

    @staticmethod
    def parse_dna(data: Union[str, List[float]]) -> "Dna":
        """
        Reads the DNA code and reads its available Gene,
        finally producing an instance of Dna.
        """
        assert data
        assert isinstance(data, str) or (isinstance(data, List) and isinstance(data[0], float))
        assert not isinstance(data, str) or len(data.split(',')) >= Gene.length()
        assert not isinstance(data, List) or len(data) >= Gene.length()
        dna_code = Dna._read_dna_code_from(data) if isinstance(data, str) else data
        genes = Dna._read_genes_from(dna_code)
        return Dna(code=dna_code, genes=genes)

    @staticmethod
    def _read_dna_code_from(data: str) -> List[float]:
        return [float(gene) for gene in data.split(',')]

    @staticmethod
    def _read_genes_from(dna_code: List[float]) -> List[Gene]:
        features: List[Gene] = []
        i, end = 0, len(dna_code)
        while i < end:
            dna_segment = dna_code[i:i+Gene.length()]
            if len(dna_segment) < Gene.length():
                break
            features.append(Gene(code=dna_segment))
            i += Gene.length()
        return features