from typing import List, Tuple, Optional, Union

import time
from pathlib import Path

import pybullet as p

from hyperparams import Hyperparams
from motor import Motor
from dna import Dna
from creature import Creature, CreatureMovement
from creature_renderer import CreatureRenderer

import logging
LOGGER = logging.getLogger(__name__)


class Simulation:
    """
    Carries out the simulation either for interactive visualisation OR for fitness test
    for creatures. It can also report back into a population while tracking the movements
    of creatures, so that the fitness can be calculated.
    """
    hyperparams: Hyperparams
    connection_mode: int
    pid: int

    def __init__(self, connection_mode: int, hyperparams: Hyperparams):
        self.hyperparams = hyperparams
        self.connection_mode = connection_mode
        self.is_interactive = connection_mode == p.GUI

    def __enter__(self):
        self.pid = p.connect(self.connection_mode)
        return self

    def __exit__(self, type, value, traceback):
        p.disconnect(physicsClientId=self.pid)

    def simulate(self, creature_data: Union[Creature, str, List[float]], steps: Optional[int] = None):
        SimulatorSetup(is_interactive=self.is_interactive, pid=self.pid).setup()
        creature, creature_id = self._place_creature_into(creature_data=creature_data)
        self._wait_end_of_simulation(creature, creature_id, steps)

    def _place_creature_into(self, creature_data: Union[Creature, List[float], str]) -> Tuple[Creature, int]:
        creature = creature_data if isinstance(creature_data, Creature) else Creature.develop_from(dna=Dna.parse_dna(creature_data), threshold_for_expression=self.hyperparams.expression_threshold)
        if creature:
            logging.debug(f"Creature, Born with name '{creature.name}'")
            urdf = CreatureRenderer(creature).render()
            filename = Path(f'/tmp/evo-{creature.name}.urdf')
            filename.write_text(urdf)
            creature_id = p.loadURDF(str(filename), physicsClientId=self.pid)
            p.resetBasePositionAndOrientation(creature_id, list(creature.movement.reset()), [0, 0, 0, 1], physicsClientId=self.pid)
            LOGGER.debug(f"Simulation, Bot #{creature_id} Loaded")
            return creature, creature_id
        else:
            raise Exception(F"DNA could not generate a creature: {creature_data}")

    def _wait_end_of_simulation(self, creature: Creature, creature_id: int, steps: Optional[int]):
        SimulationRunner(
            self.is_interactive,
            creature=creature,
            creature_id=creature_id,
            steps=steps,
            pid=self.pid).run()


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
            LOGGER.debug("Simulation, Debuggin Disabled")

    def _setup_engine(self):
        p.resetSimulation(physicsClientId=self.pid)
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=self.pid)
        p.setGravity(0, 0, -10, physicsClientId=self.pid)
        LOGGER.debug("Simulation, Engine Ready")

    def _setup_ground(self):
        shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=self.pid)
        p.createMultiBody(shape, shape, physicsClientId=self.pid)
        LOGGER.debug("Simulation, Ground Instantiated")


class SimulationRunner:
    is_interactive: bool
    creature: Creature
    creature_id: int
    steps: Optional[int]
    pid: int

    def __init__(
            self,
            is_interactive: bool,
            creature: Creature,
            creature_id: int,
            steps: Optional[int],
            pid: int) -> None:
        self.is_interactive = is_interactive
        self.creature = creature
        self.creature_id = creature_id
        self.pid = pid
        self.steps = steps

    def run(self):
        p.setRealTimeSimulation(1, physicsClientId=self.pid)
        try:
            LOGGER.debug("Simulation, Iterative Loop Starting Now")
            i = 0
            while self.steps is None or i < self.steps:
                self._run_simulation_step(step=i)
                self._update_creature_motors()
                self._track_crature_movement()
                self._wait_if_interactive()
                i += 1
            LOGGER.debug(f"Simulation, Iterative Loop, Completed Steps: {self.steps}")
        except p.error as e:
            LOGGER.debug("The simulation has been interrupted")
            pass

    def _run_simulation_step(self, step: int):
        if self.steps and not self.is_interactive:
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
        try:
            pos, _ = p.getBasePositionAndOrientation(self.creature_id, physicsClientId=self.pid)
            self.creature.movement.track(pos)
            if self.is_interactive:
                LOGGER.debug(f"Creature {self.creature.name} now in position {pos}")
                p.resetDebugVisualizerCamera(cameraDistance=5, cameraYaw=100, cameraPitch=-50, cameraTargetPosition=pos, physicsClientId=self.pid)
        except Exception as e:
            if not self.is_interactive:
                raise e

    def _wait_if_interactive(self):
        if self.is_interactive:
            time.sleep(1.0/240)
