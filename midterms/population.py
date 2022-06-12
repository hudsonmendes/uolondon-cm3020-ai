from typing import Dict, List, Iterable, Tuple, Optional

import numpy as np

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature


class Population:
    id: int
    creatures: List[Creature]

    @staticmethod
    def populate_for(size: int, gene_count: int) -> "Population":
        viable_creatures: List[Creature] = []
        while len(viable_creatures) < size:
            dna_code = PrimordialSoup.spark_life(gene_count=gene_count)
            creature = Creature.develop_from(dna=Dna.parse_dna(dna_code))
            if creature:
                viable_creatures.append(creature)
        return Population(viable_creatures)

    def __init__(self, creatures: Iterable[Creature]) -> None:
        self.creatures = sorted(set(creatures))
