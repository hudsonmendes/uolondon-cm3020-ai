from typing import Optional

from argparse import ArgumentParser, Namespace

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature
from creature_renderer import CreatureRenderer
from simulation import Simulation

import sys, logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    args = collect_args()
    if args.cmdroot == "robot":
        if args.cmdrobot == "new":
            action_new(args)
            if args.auto_load:
                action_view(args)
        if args.cmdrobot == "render":
            action_render(args)
            action_view(args)
        if args.cmdrobot == "view":
            action_view(args)


def action_new(args: Namespace):
    code = PrimordialSoup.spark_life(args.gene_count)
    dna = Dna.parse_dna(code)
    robot = Creature.develop_from(name=args.species_name, dna=dna)
    if robot:
        print(f"Robot '{robot.name}' is born.")
        write_dna(dna, filename=args.target_folder / f'{args.species_name}.dna', override=args.override_dna)
        write_robot(robot, filename=args.target_folder / f'{args.species_name}.urdf')
    else:
        print("Robot could not be generated")


def action_render(args: Namespace):
    code = read_dna(filename=args.target_folder / f'{args.species_name}.dna', index=args.dna_index)
    if code:
        dna = Dna.parse_dna(code)
        robot = Creature.develop_from(name=args.species_name, dna=dna)
        if robot:
            print(f"Robot '{robot.name}' is re-born.")
            write_robot(robot, filename=args.target_folder / f'{args.species_name}.urdf')
        else:
            print("Robot could not be rendered")


def action_view(args: Namespace):
    import pybullet as p
    simulation = Simulation(connection_mode=p.GUI)
    simulation.run(args.target_folder / f'{args.species_name}.urdf')


def collect_args() -> Namespace:
    import os
    from pathlib import Path

    def dir_path(folder: str) -> Path:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return Path(folder)

    parser = ArgumentParser()
    parser_subparsers = parser.add_subparsers(dest="cmdroot")

    parser_robot = parser_subparsers.add_parser("robot")
    parser_robot_subparsers = parser_robot.add_subparsers(dest="cmdrobot")
    parser_robot_new = parser_robot_subparsers.add_parser("new")
    parser_robot_new.add_argument("--species_name", type=str, help="You must name the species you are creating")
    parser_robot_new.add_argument("--gene_count", type=int, default=1, help="Tell the number of genes you want to generate")
    parser_robot_new.add_argument("--override_dna", action="store_true", help="Should we override the DNA file?")
    parser_robot_new.add_argument("--target_folder", type=dir_path, default="./target", help="To what folder should we output the [species_name].urdf and [species_name].dna")
    parser_robot_new.add_argument("--auto_load", action="store_true", help="Should we automatically load the URDF after saved?")
    parser_robot_render = parser_robot_subparsers.add_parser("render")
    parser_robot_render.add_argument("--dna_index", type=int, help="Which DNA from the list should we use?")
    parser_robot_render.add_argument("--target_folder", type=dir_path, default="./target", help="Which folder will be sourcing the URDF file?")
    parser_robot_render.add_argument("--species_name", type=str, help="What's the name of your bot? It must match the name of the URDF file in the `target_folder`")
    parser_robot_view = parser_robot_subparsers.add_parser("view")
    parser_robot_view.add_argument("--target_folder", type=dir_path, default="./target", help="Which folder will be sourcing the URDF file?")
    parser_robot_view.add_argument("--species_name", type=str, help="What's the name of your bot? It must match the name of the URDF file in the `target_folder`")

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


def write_dna(dna: Dna, filename: str, override: bool):
    with open(filename, 'w+' if override else 'a+', encoding='utf-8') as fh:
        fh.write(",".join([str(base) for base in dna.code]))
        fh.write("\n")
    print(f"> Output DNA : {str(filename)}")


def write_robot(robot: Creature, filename: str):
    render = CreatureRenderer(robot)
    with open(filename, 'w+', encoding='utf-8') as fh:
        fh.write(render.render())
    print(f"> Output URDF: {str(filename)}")


main()
