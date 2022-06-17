from cmath import isnan
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import uuid

import numpy as np

from dna import Dna
from phenotype import Phenotype


@dataclass(eq=True, frozen=True, order=True, unsafe_hash=False)
class Creature:
    """
    Represents a living organism or robot who has a DNA (genetic code)
    and also a body from which its parts are spanned.
    """
    dna: Dna = field(repr=False)
    phenotypes: List[Phenotype] = field(repr=False)
    body: "CreaturePart" = field(repr=False)
    name: Optional[str] = field(repr=True, default_factory=lambda: f"creature-{uuid.uuid4().hex[-6:]}")
    movement: "CreatureMovement" = field(init=False, repr=True, compare=False, default_factory=lambda: CreatureMovement())
    _unique_id: int = field(init=False, repr=False, compare=True, default_factory=lambda: uuid.uuid4().int)

    @staticmethod
    def develop_from(dna: Dna, threshold_for_expression: float) -> Optional["Creature"]:
        """
        If the DNA expresses any phenotye, return the resulting creature.
        Otherwise, returns None, signaling that no viable creature couldb e expressed.
        """
        phenotypes = dna.express(threshold_for_expression)
        if phenotypes:
            body = CreaturePart.part_hierarchy_from(phenotypes)
            return Creature(dna=dna, phenotypes=phenotypes, body=body)
        else:
            return None

    def __hash__(self) -> int:
        return self._unique_id


@dataclass(eq=True, frozen=True, order=True)
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


@dataclass(eq=True, frozen=False, order=True)
class CreatureMovement:
    """
    Keeps track of the initial and last position,
    and calculates the distance travelled.
    """
    initial: Tuple[float, float, float]
    last: Optional[Tuple[float, float, float]]
    lethal_move: bool = False

    def __init__(self):
        self.initial = 0., 0., 0.
        self.last = None

    def track(self, position: Tuple[float, float, float]):
        if position:
            self.last = position
            y = position[2]
            too_high_for_own_safety = y > 7
            if too_high_for_own_safety:
                self.lethal_move = True

    @property
    def distance(self) -> float:
        if self.last:
            p1 = np.asarray(self.initial)
            p2 = np.asarray(self.last)
            dist = np.linalg.norm(p1-p2)
            parsed = float(dist)
            if parsed and not isnan(parsed):
                return parsed
        return 0.
