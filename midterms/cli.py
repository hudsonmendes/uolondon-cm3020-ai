from typing import List, Optional

from argparse import ArgumentParser, Namespace

from simulation import Simulation
from primordial_soup import PrimordialSoup

import pybullet as p

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    args = collect_args()
    if args.cmdroot == "creature":
        if args.cmdrobot == "new":
            action_new(args)
        if args.cmdrobot == "render":
            action_render(args)


def action_new(args: Namespace):
    filename = args.target_folder / f'{args.species_name}.dna'
    dna_code = PrimordialSoup.spark_life(args.gene_count)
    write_dna(dna_code, filename=filename, override=args.override_dna)
    if args.auto_load:
        Simulation(connection_mode=p.GUI).simulate(species_name=args.species_name, dna_code=dna_code)


def action_render(args: Namespace):
    filename = args.target_folder / f'{args.species_name}.dna'
    dna_code = read_dna(filename=filename, index=args.dna_index)
    if dna_code:
        Simulation(connection_mode=p.GUI).simulate(species_name=args.species_name, dna_code=dna_code)


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
    parser_creature_new.add_argument("--species_name", type=str, help="You must name the species you are creating")
    parser_creature_new.add_argument("--gene_count", type=int, default=1, help="Tell the number of genes you want to generate")
    parser_creature_new.add_argument("--override_dna", action="store_true", help="Should we override the DNA file?")
    parser_creature_new.add_argument("--target_folder", type=dir_path, default="./target", help="To what folder should we output the [species_name].urdf and [species_name].dna")
    parser_creature_new.add_argument("--auto_load", action="store_true", help="Should we automatically load the URDF after saved?")
    parser_creature_render = parser_creature_subparsers.add_parser("render")
    parser_creature_render.add_argument("--dna_index", type=int, help="Which DNA from the list should we use?")
    parser_creature_render.add_argument("--target_folder", type=dir_path, default="./target", help="Which folder will be sourcing the URDF file?")
    parser_creature_render.add_argument("--species_name", type=str, help="What's the name of your bot? It must match the name of the URDF file in the `target_folder`")

    parser_evo = parser_subparsers.add_parser("evo")
    parser_evo_subparsers = parser_evo.add_subparsers(dest="cmdevo")
    parser_evo_genesis = parser_evo_subparsers.add_parser("genesis")
    parser_evo_genesis.add_argument("--evolution_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
    parser_evo_iterate = parser_evo_subparsers.add_parser("iterate")
    parser_evo_iterate.add_argument("--evolution_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
    parser_evo_iterate.add_argument("--multi_threaded", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")

    args = parser.parse_args()
    return args


def read_dna(filename: str, index: int) -> Optional[str]:
    with open(filename, 'r+', encoding='utf-8') as fh:
        i = 0
        for line in fh:
            if i == index:
                print(f"> Read DNA[{i}] : {line}")
                return line
            i += 1
    return None


def write_dna(dna_code: List[float], filename: str, override: bool):
    with open(filename, 'w+' if override else 'a+', encoding='utf-8') as fh:
        fh.write(",".join([str(base) for base in dna_code]))
        fh.write("\n")
    print(f"> Output DNA : {str(filename)}")


main()
