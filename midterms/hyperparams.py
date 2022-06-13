from argparse import Namespace
from dataclasses import dataclass, fields
from typing import Optional


@dataclass(eq=True, frozen=True, order=True)
class Hyperparams:
    crossover_min_len: float
    crossover_max_len: float
    point_mutation_enabled: bool
    point_mutation_rate: float
    point_mutation_amount: float
    shrink_mutation_enabled: bool
    shrink_mutation_rate: float
    grow_mutation_enabled: bool
    grow_mutation_rate: float
    reproduction_max_attempts: int
    elitist_behaviour: bool
    expression_threshold: float
    population_size: int
    simulation_steps: int
    gene_count: int

    @staticmethod
    def from_args(args: Namespace) -> "Hyperparams":
        arg_dict = dict()
        for field in fields(Hyperparams):
            if field.name in args and args.__dict__[field.name]:
                arg_dict[field.name] = args.__dict__[field.name]
        return Hyperparams(**arg_dict)
