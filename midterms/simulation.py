from typing import List, Tuple, Optional, Union

import time
from pathlib import Path

import pybullet as p

from population import Population
from motor import Motor
from dna import Dna
from creature import Creature
from creature_renderer import CreatureRenderer

import logging
LOGGER = logging.getLogger(__name__)


class Simulation:
    """
    Carries out the simulation either for interactive visualisation OR for fitness test
    for creatures. It can also report back into a population while tracking the movements
    of creatures, so that the fitness can be calculated.
    """
    connection_mode: int
    pid: int
    population: Optional[Population]

    def __init__(self, connection_mode: int, population: Optional[Population] = None):
        self.population = population
        self.is_interactive = connection_mode == p.GUI
        self.pid = p.connect(connection_mode)

    def simulate(self, species_name: str, dna_code: Union[str, List[float]], steps: Optional[int] = None):
        SimulatorSetup(is_interactive=self.is_interactive, pid=self.pid).setup()
        creature, creature_id = self._dna_into_creature(name=species_name, dna_code=dna_code)
        self._wait_end_of_simulation(creature, creature_id, steps, self.population)

    def _dna_into_creature(self, name: str, dna_code: Union[List[float], str]) -> Tuple[Creature, int]:
        dna = Dna.parse_dna(dna_code)
        creature = Creature.develop_from(name=name, dna=dna)
        if creature:
            logging.info(f"Creature, Born with name '{creature.name}'")
            urdf = CreatureRenderer(creature).render()
            filename = Path(f'/tmp/evo-{name}.urdf')
            filename.write_text(urdf)
            creature_id = p.loadURDF(str(filename))
            p.resetBasePositionAndOrientation(creature_id, [0, 0, 5], [0, 0, 0, 1])
            LOGGER.info(f"Simulation, Bot #{creature_id} Loaded")
            return creature, creature_id
        else:
            raise Exception(F"DNA could not generate a creature: {dna_code}")

    def _wait_end_of_simulation(self, creature: Creature, creature_id: int, steps: Optional[int], population: Optional[Population]):
        SimulationRunner(
            self.is_interactive,
            creature=creature,
            creature_id=creature_id,
            steps=steps,
            pid=self.pid,
            population=population).run()


class SimulatorSetup:
    is_interactive: bool
    pid: int

    def __init__(self, is_interactive: bool, pid: int):
        self.is_interactive = is_interactive
        self.pid = pid

    def setup(self):
        self._disable_gui_debug_if_applicable()
        self._setup_engine()
        self._setup_ground()

    def _disable_gui_debug_if_applicable(self):
        if self.is_interactive:
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0, physicsClientId=self.pid)
            LOGGER.info("Simulation, Debuggin Disabled")

    def _setup_engine(self):
        p.resetSimulation(physicsClientId=self.pid)
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=self.pid)
        p.setGravity(0, 0, -10, physicsClientId=self.pid)
        LOGGER.info("Simulation, Engine Ready")

    def _setup_ground(self):
        shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=self.pid)
        p.createMultiBody(shape, shape)
        LOGGER.info("Simulation, Ground Instantiated")


class SimulationRunner:
    is_interactive: bool
    creature: Creature
    creature_id: int
    steps: Optional[int]
    pid: int
    population: Optional[Population]

    def __init__(
            self,
            is_interactive: bool,
            creature: Creature,
            creature_id: int,
            steps: Optional[int],
            pid: int,
            population: Optional[Population]) -> None:
        self.is_interactive = is_interactive
        self.creature = creature
        self.creature_id = creature_id
        self.pid = pid
        self.steps = steps
        self.population = population

    def run(self):
        p.setRealTimeSimulation(1)
        try:
            LOGGER.info("Simulation, Iterative Loop Starting Now")
            i = 0
            while self.steps is None or i < self.steps:
                self._run_simulation_step(step=i)
                self._update_creature_motors()
                self._track_crature_movement()
                self._wait_if_interactive()
                i += 1
            LOGGER.info(f"Simulation, Iterative Loop, Completed Steps: {self.steps}")
        except p.error as e:
            LOGGER.info("The simulation has been interrupted")
            pass

    def _run_simulation_step(self, step: int):
        LOGGER.debug(f"Simulation, Step {step} out of {self.steps if self.steps else '∞'}")
        p.stepSimulation(physicsClientId=self.pid)

    def _update_creature_motors(self):
        for jid in range(p.getNumJoints(self.creature_id, physicsClientId=self.pid)):
            phenotype = self.creature.phenotypes[jid+1]
            motor = Motor.generate_from(phenotype)
            p.setJointMotorControl2(
                self.creature_id,
                jid,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=next(motor),
                force=5,
                physicsClientId=self.pid)

    def _track_crature_movement(self):
        pos, _ = p.getBasePositionAndOrientation(self.creature_id, physicsClientId=self.pid)
        LOGGER.debug(f"Creature {self.creature.name} now in position {pos}")
        if self.population:
            self.population.report_movement(self.creature, pos)
        if self.is_interactive:
            p.resetDebugVisualizerCamera(cameraDistance=5, cameraYaw=100, cameraPitch=-50, cameraTargetPosition=pos, physicsClientId=self.pid)

    def _wait_if_interactive(self):
        if self.is_interactive:
            time.sleep(1.0/240)
