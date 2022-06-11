from creature_renderer import CreatureRenderer
from creature import Creature
from dna import Dna
from typing import Tuple, Optional

import time
from pathlib import Path

import pybullet as p

import logging
LOGGER = logging.getLogger(__name__)


class Simulation:
    """
    Carries out the simulation either for interactive
    visualisation OR for fitness test
    """
    connection_mode: int
    pid: int

    def __init__(
            self,
            connection_mode: int,
    ):
        self.connection_mode = connection_mode
        self.pid = p.connect(connection_mode)
        self._disable_gui_debug_if_applicable()
        self._setup_engine()
        self._setup_ground()

    def born_in_the_world(
            self,
            dna_code: str,
            gen: Optional[int] = None,
            race: Optional[int] = None) -> Tuple[Creature, int]:
        if not gen:
            gen = 0
        if not race:
            race = 0
        name = f'evo-gen-{gen}-{race}'
        dna = Dna.parse_dna(dna_code)
        creature = Creature.develop_from(name=name, dna=dna)
        if creature:
            urdf = CreatureRenderer(creature).render()
            filename = Path(f'/tmp/urdf-{name}.urdf')
            filename.write_text(urdf)
            return creature, self._setup_bot(filename)
        else:
            raise Exception(F"DNA could not generate a creature: {dna_code}")

    def run(self, dna_code: str, steps: Optional[int] = None):
        creature, creature_id = self.born_in_the_world(dna_code)
        self._wait_completion(creature, creature_id, steps)

    def _disable_gui_debug_if_applicable(self):
        if self.connection_mode == p.GUI:
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

    def _setup_bot(self, urdf: Path) -> int:
        bot = p.loadURDF(str(urdf))
        p.resetBasePositionAndOrientation(bot, [0, 0, 5], [0, 0, 0, 1])
        LOGGER.info(f"Simulation, Bot #{bot} Loaded")
        return bot

    def _wait_completion(self, creature: Creature, creature_id: int, steps: Optional[int]):
        p.setRealTimeSimulation(1)
        try:
            LOGGER.info("Simulation, Iterative Loop Starting Now")
            i = 0
            while steps is None or i < steps:
                self._run_simulation_step(step=i, steps=steps)
                self._update_creature_motors(creature, creature_id)
                self._wait_interactive_time()
                i += 1
            LOGGER.info(f"Simulation, Iterative Loop, Completed Steps: {steps}")
        except p.error as e:
            LOGGER.info("The simulation has been interrupted")
            pass

    def _run_simulation_step(self, step: int, steps: Optional[int]):
        LOGGER.debug(f"Simulation, Step {step} out of {steps if steps else '∞'}")
        p.stepSimulation(physicsClientId=self.pid)

    def _update_creature_motors(self, creature: Creature, creature_id: int):
        for jid in range(p.getNumJoints(creature_id, physicsClientId=self.pid)):
            motor = creature.motors[jid]
            p.setJointMotorControl2(
                creature_id,
                jid,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=motor.get_output(),
                force=5,
                physicsClientId=self.pid)

    def _wait_interactive_time(self):
        if self.connection_mode == p.GUI:
            time.sleep(1.0/240)
