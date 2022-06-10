from argparse import ArgumentParser, Namespace

from primordial_soup import PrimordialSoup
from dna import Dna
from creature import Creature
from creature_renderer import CreatureRenderer


def main():
    args = collect_args()
    if args.cmdroot == "robot":
        if args.cmdrobot == "create":
            action_creation(args)
        if args.cmdrobot == "view":
            action_view(args)


def action_creation(args: Namespace):
    code = PrimordialSoup.spark_life(args.gene_count)
    dna = Dna.parse_dna(code)
    robot = Creature.develop_from(name=args.species_name, dna=dna)
    if robot:
        print(f"Robot '{robot.name}' is born.")
        write_dna(dna, filename=args.out_folder / f'{args.species_name}.dna', override=args.override_dna)
        write_robot(robot, filename=args.out_folder / f'{args.species_name}.urdf')
    else:
        print("Robot could not be generated")


def action_view(args: Namespace):
    import time
    import pybullet as p
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.setGravity(0, 0, -10)
    plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    p.createMultiBody(plane_shape, plane_shape)
    filename = args.src_folder / f'{args.species_name}.urdf'
    p.loadURDF(str(filename))
    p.setRealTimeSimulation(1)
    print("Press CTRL+C to interrupt...")
    while True:
        p.stepSimulation()
        time.sleep(1.0/240)


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
    parser_robot_create = parser_robot_subparsers.add_parser("create")
    parser_robot_create.add_argument("--species_name", type=str, help="You must name the species you are creating")
    parser_robot_create.add_argument("--gene_count", type=int, default=1, help="Tell the number of genes you want to generate")
    parser_robot_create.add_argument("--override_dna", action="store_true", help="Should we override the DNA file?")
    parser_robot_create.add_argument("--out_folder", type=dir_path, default="./target", help="To what folder should we output the [species_name].urdf and [species_name].dna")
    parser_robot_view = parser_robot_subparsers.add_parser("view")
    parser_robot_view.add_argument("--src_folder", type=dir_path, default="./target", help="Which folder will be sourcing the URDF file?")
    parser_robot_view.add_argument("--species_name", type=dir_path, help="What's the name of your bot? It must match the name of the URDF file in the `src_folder`")

    parser_evo = parser_subparsers.add_parser("evo")
    parser_evo_subparsers = parser_evo.add_subparsers(dest="cmdevo")
    parser_evo_genesis = parser_evo_subparsers.add_parser("genesis")
    parser_evo_genesis.add_argument("--evolution_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
    parser_evo_iterate = parser_evo_subparsers.add_parser("iterate")
    parser_evo_iterate.add_argument("--evolution_folder", type=dir_path, default="./evolution", help="Which directory will keep record of the evolution?")
    parser_evo_iterate.add_argument("--multi_threaded", action="store_true", help="Do you want to run the simulation as a multi-threaded process?")

    args = parser.parse_args()
    return args


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
