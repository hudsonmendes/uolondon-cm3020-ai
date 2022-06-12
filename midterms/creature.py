from dataclasses import dataclass
from typing import List, Optional

import random

from dna import Dna
from phenotype import Phenotype


@dataclass
class Creature:
    """
    Represents a living organism or robot who has a DNA (genetic code)
    and also a body from which its parts are spanned.
    """
    dna: Dna
    phenotypes: List[Phenotype]
    body: "CreaturePart"
    unique_id: str = "creature-%032x" % random.getrandbits(64)

    @staticmethod
    def develop_from(dna: Dna) -> Optional["Creature"]:
        """
        If the DNA expresses any phenotye, return the resulting creature.
        Otherwise, returns None, signaling that no viable creature couldb e expressed.
        """
        phenotypes = dna.express()
        if phenotypes:
            body = CreaturePart.part_hierarchy_from(phenotypes)
            return Creature(dna=dna, phenotypes=phenotypes, body=body)
        else:
            return None


@dataclass
class CreaturePart:
    """
    Represents a part of the body of the creature, linking
    it to the children parts, as well as the phenotype that produced it.
    """
    phenotype: Phenotype
    children: List["CreaturePart"]

    @staticmethod
    def part_hierarchy_from(
            phenotypes: List[Phenotype],
            phenotype_index: int = 0) -> "CreaturePart":
        child_phenotype_indexes = [i for i, p in enumerate(phenotypes) if p.joint_parent == phenotype_index]
        return CreaturePart(
            phenotype=phenotypes[phenotype_index],
            children=[
                CreaturePart.part_hierarchy_from(phenotypes=phenotypes, phenotype_index=child_i)
                for child_i
                in child_phenotype_indexes])
