from typing import Set, Dict, Iterable, Tuple, Optional

import numpy as np

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature


class Population:
    id: int
    creatures: Set[Creature]
    trackers: Dict[Creature, "PopulationTracker"]

    @staticmethod
    def generate_for(size: int, gene_count: int) -> "Population":
        bases_pool = [PrimordialSoup.spark_life(gene_count=gene_count) for _ in range(size)]
        dna_pool = [Dna.parse_dna(bases) for bases in bases_pool]
        all_creatures = [Creature.develop_from(dna) for dna in dna_pool]
        viable_creatures = [c for c in all_creatures if c]
        return Population(viable_creatures)

    def __init__(self, creatures: Iterable[Creature]) -> None:
        self.creatures = set(creatures)
        self.trackers = {}

    def report_movement(self, creature: Creature, position: Tuple[float, float, float]):
        self.creatures.add(creature)
        self.trackers.setdefault(creature, PopulationTracker()).track(position=position)

    def tracker_for(self, creature: Creature):
        return self.trackers.get(creature, PopulationTracker())

    @property
    def elite_duo(self) -> Tuple[Creature, Creature]:
        creatures = sorted(self.creatures)
        dists = np.array([self.tracker_for(c).distance_travelled for c in creatures])
        za_dist_indexes = list(reversed(np.argsort(dists)))
        top_1_index, top_2_index = za_dist_indexes[0:2]
        return creatures[top_1_index], creatures[top_2_index]


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
