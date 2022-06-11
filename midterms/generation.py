from typing import Set, Dict, Optional

import numpy as np

from creature import Creature


class Generation:
    id: int
    creatures: Set[Creature]
    trackers: Dict[Creature, "GenerationTracker"]

    def __init__(self, generation_id: int) -> None:
        self.generation_id = generation_id
        self.creatures = set()
        self.trackers = dict()

    def report_movement(self, creature: Creature, position: float):
        self.creatures.add(creature)
        self.trackers.setdefault(creature, GenerationTracker()).track(position=position)

    def distances_for(self, creature: Creature):
        return self.trackers.get(creature, GenerationTracker())


class GenerationTracker:
    _initial: Optional[float]
    _last: Optional[float]

    def __init__(self, initial: Optional[float] = None, last: Optional[float] = None) -> None:
        self._initial = initial
        self._last = last

    @property
    def initial(self) -> float:
        return self._initial if self._initial is not None else 0.

    @property
    def last(self) -> float:
        return self._last if self._last is not None else 0.

    @property
    def distance_travelled(self) -> float:
        p1 = np.asarray(self.initial)
        p2 = np.asarray(self.last)
        dist = np.linalg.norm(p1-p2)
        return float(dist)

    def track(self, position: float):
        if self._initial is None:
            self._initial = position
        self._last = position
