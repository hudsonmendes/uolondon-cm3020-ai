from dataclasses import dataclass


@dataclass
class DQNHyperparams:
    frames: int = 4
    gamma: float = 0.99