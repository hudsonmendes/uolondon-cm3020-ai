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

    @property
    def fittest(self) -> Creature:
        """
        Calculates the fitest of a population with the information available in the tracking system.
        """
        dists = np.array([c.movement.distance for c in self.creatures])
        winner = np.argmax(dists)
        return self.creatures[winner]

    def next_roulette_pair(self) -> Tuple[Creature, Creature]:
        """ 
        Using the fitness map, select randomly two parents,
        with odds proportional to their fitness.
        """
        creatures = self.creatures
        fm = Population._calculate_fitness_map(creatures)
        return Population._select_parent(creatures, fm), Population._select_parent(creatures, fm)

    @staticmethod
    def _calculate_fitness_map(creatures: List[Creature]) -> List[float]:
        out: List[float] = []
        total = 0.
        if all([c.movement.last is None for c in creatures]):
            uniform = 1. / len(creatures)
            out.extend([(i+1) * uniform for i in range(len(creatures))])
        else:
            for creature in creatures:
                total += creature.movement.distance
                out.append(total)
        return out

    @staticmethod
    def _select_parent(creatures: List[Creature], fm: List[float]) -> Creature:
        r = np.random.rand()
        r *= fm[-1]
        for i in range(len(fm)):
            if r <= fm[i]:
                return creatures[i]
        raise IndexError(f"The random '{r}' could not be found in the fitness map: {','.join([str(f) for f in fm])}")
