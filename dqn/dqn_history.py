from dataclasses import dataclass
from typing import List


@dataclass
class DQNEntry:
    state: List[List[List[int]]]
    action: int
    total_reward: float
    next_state: List[List[int]]
    ended: bool
