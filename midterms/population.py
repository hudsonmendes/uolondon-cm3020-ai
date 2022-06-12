from typing import Dict, List, Iterable, Tuple, Optional

import numpy as np

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature


class Population:
    id: int
    creatures: List[Creature]
    trackers: Dict[Creature, "PopulationTracker"]

    @staticmethod
    def generate_for(size: int, gene_count: int) -> "Population":
        viable_creatures: List[Creature] = []
        while len(viable_creatures) < size:
            dna_code = PrimordialSoup.spark_life(gene_count=gene_count)
            creature = Creature.develop_from(dna=Dna.parse_dna(dna_code))
            if creature:
                viable_creatures.append(creature)
        return Population(viable_creatures)

    def __init__(self, creatures: Iterable[Creature]) -> None:
        self.creatures = sorted(set(creatures))
        self.trackers = {}

    def report_movement(self, creature: Creature, position: Tuple[float, float, float]):
        """
        Reports that a particular creature has moved to a point,
        later used to calculate the fitness map.
        """
        if creature not in self.creatures:
            self.creatures.append(creature)
        self.trackers.setdefault(creature, PopulationTracker()).track(position=position)

    def tracker_for(self, creature: Creature) -> "PopulationTracker":
        """
        Returns the PopulationTracker for the creature.
        We default to an empty tracker instead of returning None.
        """
        return self.trackers.get(creature, PopulationTracker())

    @property
    def fittest(self) -> Creature:
        dists = np.array([self.tracker_for(c).distance_travelled for c in self.creatures])
        winner = np.argmax(dists)
        return self.creatures[winner]

    @property
    def roulet_pair(self) -> Tuple[Creature, Creature]:
        """ 
        Using the fitness map, select randomly two parents,
        with odds proportional to their fitness.
        """
        fm = self._calculate_fitness_map()
        return self._select_parent(fm), self._select_parent(fm)

    def _calculate_fitness_map(self) -> List[float]:
        out: List[float] = []
        total = 0.
        for creature in self.creatures:
            total += self.tracker_for(creature).distance_travelled
            out.append(total)
        return out

    def _select_parent(self, fm: List[float]) -> Creature:
        r = np.random.rand()
        r *= fm[-1]
        for i in range(len(fm)):
            if r <= fm[i]:
                return self.creatures[i]
        raise IndexError(f"The random '{r}' could not be found in the fitness map: {','.join([str(f) for f in fm])}")


class PopulationTracker:
    initial: Tuple[float, float, float]
    last: Optional[Tuple[float, float, float]]

    def __init__(self):
        self.initial = 0., 0., 0.
        self.last = None

    @property
    def distance_travelled(self) -> float:
        if self.last:
            p1 = np.asarray(self.initial)
            p2 = np.asarray(self.last)
            dist = np.linalg.norm(p1-p2)
            return float(dist)
        return 0.

    def track(self, position: Tuple[float, float, float]):
        if position:
            self.last = position
