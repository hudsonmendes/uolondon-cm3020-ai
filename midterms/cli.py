from argparse import ArgumentParser, Namespace
from hyperparams import Hyperparams

from persistence import DnaRepository, EvolutionRepository, PersistenceSettings
from simulation import Simulation
from primordial_soup import PrimordialSoup
from evolution import Evolver

import pybullet as p

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.WARN)
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


def action_new(args: Namespace):
    dna_code = PrimordialSoup.spark_life(args.gene_count)
    repository = DnaRepository(settings=PersistenceSettings(folder=args.target_folder))
    repository.write(species=args.species, dna_code=dna_code, override=args.override_dna)
    if args.auto_load:
        Simulation(connection_mode=p.GUI).simulate(dna_code)


def action_render(args: Namespace):
    repository = DnaRepository(settings=PersistenceSettings(folder=args.target_folder))
    dna = repository.read(species=args.species, individual=args.dna_index)
    if dna:
        Simulation(connection_mode=p.GUI).simulate(dna.code)


def action_evolve(args: Namespace):
    evolution_repository = EvolutionRepository(settings=PersistenceSettings(folder=args.target_folder))

    previous = evolution_repository.read(args.gen_id)
    genesis = None
    if previous:
        LOGGER.info(f"Evolve, loaded generation #{args.gen_id}")
        genesis = previous.to_population()

    hyperparams = Hyperparams(population_size=args.hp_pop_size, gene_count=args.hp_gene_count)
    evolver = Evolver(hyperparams)
    evolving_id = 0 if args.gen_id is None else args.gen_id + 1
    LOGGER.info(f"Evolve, will evolve #{evolving_id}")

    evolution = evolver.evolve(generation_id=evolving_id, previous=genesis)

    LOGGER.info(f"Evolve, storing results #{evolving_id}")
    evolution_repository.write(evolution)

    if evolution.elite_offspring:
        LOGGER.info(f"Evolve, best bot")
        Simulation(connection_mode=p.GUI).simulate(evolution.elite_offspring)


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
    parser_evo_iterate = parser_evo_subparsers.add_parser("evolve")
    parser_evo_iterate.add_argument("--gen_id", type=int, help="The id of the generation that will be EVOLVED")
    parser_evo_iterate.add_argument("--show_winner", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")
    parser_evo_iterate.add_argument("--target_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
    parser_evo_iterate.add_argument("--multi_threaded", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")
    parser_evo_iterate.add_argument("--hp_pop_size", type=int, default=10, help="Hyperparams, population size for the experiments")
    parser_evo_iterate.add_argument("--hp_gene_count", type=int, default=1, help="Hyperparams, number of genes in the seed process")

    args = parser.parse_args()
    return args


main()
