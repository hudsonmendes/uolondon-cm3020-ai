from typing import Dict, List, Tuple, Optional

import numpy as np

from creature import Creature
from population import Population


class Fitness:
    """
    Keeps the fitness trackers for each one of the creature and
    can calculate the fitest and roullete_pair
    """
    trackers: Dict[Creature, "FitnessTracker"]

    def __init__(self) -> None:
        self.trackers = {}

    def report_movement(self, creature: Creature, position: Tuple[float, float, float]):
        """
        Reports that a particular creature has moved to a point,
        later used to calculate the fitness map.
        """
        self.trackers.setdefault(creature, FitnessTracker()).track(position=position)

    def tracker_for(self, creature: Creature) -> "FitnessTracker":
        """
        Returns the PopulationTracker for the creature.
        We default to an empty tracker instead of returning None.
        """
        return self.trackers.get(creature, FitnessTracker())

    def calculate_fittest_from(self, population: Population) -> Creature:
        """
        Calculates the fitest of a population with the information available in the tracking system.
        """
        dists = np.array([self.tracker_for(c).distance_travelled for c in population.creatures])
        winner = np.argmax(dists)
        return population.creatures[winner]

    def next_roullete_pair_from(self, population: Population) -> Tuple[Creature, Creature]:
        """ 
        Using the fitness map, select randomly two parents,
        with odds proportional to their fitness.
        """
        creatures = population.creatures
        fm = self._calculate_fitness_map(creatures)
        return self._select_parent(creatures, fm), self._select_parent(creatures, fm)

    def _calculate_fitness_map(self, creatures: List[Creature]) -> List[float]:
        out: List[float] = []
        total = 0.
        for creature in creatures:
            total += self.tracker_for(creature).distance_travelled
            out.append(total)
        return out

    def _select_parent(self, creatures: List[Creature], fm: List[float]) -> Creature:
        r = np.random.rand()
        r *= fm[-1]
        for i in range(len(fm)):
            if r <= fm[i]:
                return creatures[i]
        raise IndexError(f"The random '{r}' could not be found in the fitness map: {','.join([str(f) for f in fm])}")


class FitnessTracker:
    """
    Keeps track of the initial and last position,
    and calculates the distance travelled.
    """
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
