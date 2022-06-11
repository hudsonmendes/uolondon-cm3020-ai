from typing import Set, Dict, Tuple, Optional

import numpy as np

from creature import Creature


class Population:
    id: int
    creatures: Set[Creature]
    trackers: Dict[Creature, "PopulationTracker"]

    def __init__(self, generation_id: int) -> None:
        self.generation_id = generation_id
        self.creatures = set()
        self.trackers = dict()

    def report_movement(self, creature: Creature, position: Tuple[float, float, float]):
        self.creatures.add(creature)
        self.trackers.setdefault(creature, PopulationTracker()).track(position=position)

    def distances_for(self, creature: Creature):
        return self.trackers.get(creature, PopulationTracker())


class PopulationTracker:
    initial: Optional[Tuple[float, float, float]]
    last: Optional[Tuple[float, float, float]]

    def __init__(self):
        self.initial = None
        self.final = None

    @property
    def distance_travelled(self) -> float:
        if self.initial and self.last:
            p1 = np.asarray(self.initial)
            p2 = np.asarray(self.last)
            dist = np.linalg.norm(p1-p2)
            return float(dist)
        return 0.

    def track(self, position: Tuple[float, float, float]):
        if position:
            if not self.initial:
                self.initial = position
            self.last = position
