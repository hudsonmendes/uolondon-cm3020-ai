from argparse import ArgumentParser, Namespace

import os
from pathlib import Path

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature
from creature_renderer import CreatureRenderer


def main():
    args = collect_args()
    code = PrimordialSoup.spark_life(args.gene_count)
    dna = Dna.parse_dna(code)
    robot = Creature.develop_from(name=args.species_name, dna=dna)
    if robot:
        print("Robot '{robot.name}' is born.")
        write_dna(dna, filename=args.out_folder / f'{args.species_name}.dna', append=args.append_dna)
        write_robot(robot, filename=args.out_folder / f'{args.species_name}.urdf')
    else:
        print("Robot could not be generated")


def collect_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--species_name", type=str, help="You must name the species you are creating")
    parser.add_argument("--gene_count", type=int, default=1, help="Tell the number of genes you want to generate")
    parser.add_argument("--append_dna", action="store_true", help="Should we append the DNA to the file?")
    parser.add_argument("--out_folder", type=Path, default="./target", help="To what folder should we output the [species_name].urdf and [species_name].dna")
    args = parser.parse_args()
    if not os.path.isdir(args.out_folder):
        os.makedirs(args.out_folder)
    return args


def write_dna(dna: Dna, filename: str, append: bool):
    with open(filename, 'a+' if append else 'w+', encoding='utf-8') as fh:
        fh.write(",".join([str(base) for base in dna.code]))
        fh.write("\n")
    print(f"> Output DNA : {str(filename)}")


def write_robot(robot: Creature, filename: str):
    render = CreatureRenderer(robot)
    with open(filename, 'w+', encoding='utf-8') as fh:
        fh.write(render.render())
    print(f"> Output URDF: {str(filename)}")


main()
