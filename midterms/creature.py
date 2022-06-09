from audioop import reverse
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

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
            body = None
            return Creature(dna=dna, body=body)
        else:
            return None


@dataclass
class CreaturePart:
    phenotype: Phenotype
    parent: Optional["CreaturePart"]
    children: List["CreaturePart"]
