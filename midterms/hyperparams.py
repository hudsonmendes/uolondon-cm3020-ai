from dataclasses import dataclass


@dataclass
class Hyperparams:
    crossover_min_len = 0.25
    crossover_max_len = 0.75
    point_mutation_enabled: bool = True
    point_mutation_rate: float = 0.1
    point_mutation_amount: float = 0.1
    shrink_mutation_enabled: bool = True
    shrink_mutation_rate: float = 0.25
    grow_mutation_enabled: bool = True
    grow_mutation_rate: float = 0.1
    population_count: int = 100
    generation_steps: int = 2400