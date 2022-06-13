from argparse import ArgumentParser, Namespace

import shutil
import random
import numpy as np

from hyperparams import Hyperparams
from persistence import DnaRepository, EvolutionRepository, PersistenceSettings
from population import Population
from simulation import Simulation
from primordial_soup import PrimordialSoup
from evolution import Evolver

import pybullet as p

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def main():
    args = collect_args()
    if args.cmdroot == "creature":
        if args.cmdrobot == "new":
            action_new(args)
        elif args.cmdrobot == "render":
            action_render(args)
    elif args.cmdroot == "evolution":
        if args.cmdevo == "evolve":
            action_evolve(args)
        if args.cmdevo == "optimise":
            action_optimise(args)


def action_new(args: Namespace):
    dna_code = PrimordialSoup.spark_life(args.gene_count)
    repository = DnaRepository(settings=PersistenceSettings(folder=args.target_folder))
    repository.write(species=args.species, dna_code=dna_code, override=args.override_dna)
    if args.auto_load:
        with Simulation(connection_mode=p.GUI) as simulation:
            simulation.simulate(dna_code)


def action_render(args: Namespace):
    repository = DnaRepository(settings=PersistenceSettings(folder=args.target_folder))
    dna = repository.read(species=args.species, individual=args.dna_index)
    if dna:
        with Simulation(connection_mode=p.GUI) as simulation:
            simulation.simulate(dna.code)


def action_evolve(args: Namespace, last_score: float = 0) -> float:
    persistence_settings = PersistenceSettings(folder=args.target_folder)
    evolution_repository = EvolutionRepository(settings=persistence_settings)
    dna_repository = DnaRepository(settings=persistence_settings)
    previous = evolution_repository.read(args.gen_id)
    genesis = None
    if previous:
        if args.show_winner:
            LOGGER.info(f"Generation #{args.gen_id}, loaded")
        genesis = previous.to_population()
    hyperparams = Hyperparams()
    evolver = Evolver(hyperparams)
    evolving_id = 0 if args.gen_id is None else args.gen_id + 1
    if args.show_winner:
        LOGGER.info(f"Generation #{args.gen_id}, will evolve generation #{evolving_id}")
    evolution = evolver.evolve(generation_id=evolving_id, previous=genesis)
    if args.show_winner:
        LOGGER.info(f"Generation #{args.gen_id}, storing results #{evolving_id}")
    evolution_repository.write(evolution)
    if evolution.elite_offspring:
        dna_repository.write("elite", evolution.elite_offspring.dna_code)
        message = f"Generation #{args.gen_id}, best bot walked {evolution.elite_offspring.fitness_score}, P95={evolution.fitness_p95}"
        if evolution.elite_previous and evolution.elite_offspring.dna_code != evolution.elite_previous.dna_code:
            message += f" > {evolution.elite_previous.fitness_score}"
        LOGGER.info(message)
        try:
            if args.show_winner and last_score < evolution.elite_offspring.fitness_score:
                with Simulation(connection_mode=p.GUI) as simulation:
                    simulation.simulate(evolution.elite_offspring.dna_code)
        except Exception as _:
            pass
        except KeyboardInterrupt as _:
            pass
        return evolution.elite_offspring.fitness_score
    return 0.


def action_optimise(args: Namespace):
    random.seed(0)
    np.random.seed(0)
    if not args.genesis_filepath or not args.genesis_filepath.is_file:
        raise FileNotFoundError(args.genesis_filepath)
    
    shutil.copy(args.genesis_filepath, args.target_folder / "generation-0.evo")
    args.gen_id = 0
    last_score = 0.
    for _ in range(args.n_generations - 1):
        last_score = max(last_score, action_evolve(args, last_score))
        args.gen_id += 1
    persistence_settings = PersistenceSettings(folder=args.target_folder)
    dna_repository = DnaRepository(settings=persistence_settings)
    dna_repository.dedup("elite")


def collect_args() -> Namespace:
    import os
    from pathlib import Path

    def dir_path(folder: str) -> Path:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return Path(folder)

    parser = ArgumentParser()
    parser_subparsers = parser.add_subparsers(dest="cmdroot")

    parser_creature = parser_subparsers.add_parser("creature")
    parser_creature_subparsers = parser_creature.add_subparsers(dest="cmdrobot")
    parser_creature_new = parser_creature_subparsers.add_parser("new")
    parser_creature_new.add_argument("--species", type=str, help="You must name the species you are creating")
    parser_creature_new.add_argument("--gene_count", type=int, default=1, help="Tell the number of genes you want to generate")
    parser_creature_new.add_argument("--override_dna", action="store_true", help="Should we override the DNA file?")
    parser_creature_new.add_argument("--target_folder", type=dir_path, default="./target", help="To what folder should we output the [species].urdf and [species].dna")
    parser_creature_new.add_argument("--auto_load", action="store_true", help="Should we automatically load the URDF after saved?")
    parser_creature_render = parser_creature_subparsers.add_parser("render")
    parser_creature_render.add_argument("--dna_index", type=int, help="Which DNA from the list should we use?")
    parser_creature_render.add_argument("--target_folder", type=dir_path, default="./target", help="Which folder will be sourcing the URDF file?")
    parser_creature_render.add_argument("--species", type=str, help="What's the name of your bot? It must match the name of the URDF file in the `target_folder`")

    parser_evo = parser_subparsers.add_parser("evolution")
    parser_evo_subparsers = parser_evo.add_subparsers(dest="cmdevo")
    parser_evo_evolve = parser_evo_subparsers.add_parser("evolve")
    parser_evo_optimise = parser_evo_subparsers.add_parser("optimise")
    parser_evo_parsers = parser_evo_evolve, parser_evo_optimise
    parser_evo_optimise.add_argument("--genesis_filepath", type=Path, required=True, help="If you want to reutilise an evolution from another experiment, enter the path")
    parser_evo_optimise.add_argument("--n_generations", type=int, help="The number of generations for which we will optimise")
    for parser_evo_parser in parser_evo_parsers:
        parser_evo_parser.add_argument("--gen_id", type=int, help="The id of the generation that will be EVOLVED")
        parser_evo_parser.add_argument("--show_winner", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")
        parser_evo_parser.add_argument("--target_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
        parser_evo_parser.add_argument("--multi_threaded", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")

    args = parser.parse_args()
    return args


main()
