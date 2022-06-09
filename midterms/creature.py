from dataclasses import dataclass
from typing import List, Optional

from dna import Dna
from phenotype import Phenotype


@dataclass
class Creature:
    """
    Represents a living organism or robot who has a DNA (genetic code)
    and also a body from which its parts are spanned.
    """
    dna: Dna
    body: "CreaturePart"

    @staticmethod
    def develop_from(dna: Dna) -> Optional["Creature"]:
        phenotypes = dna.express()
        if phenotypes:
            children: List["CreaturePart"] = []
            return Creature(
                dna=dna,
                body=CreaturePart(
                    phenotype=phenotypes[0],
                    parent=None,
                    children=children))
        return None


@dataclass
class CreaturePart:
    phenotype: Phenotype
    parent: Optional["CreaturePart"]
    children: List["CreaturePart"]
