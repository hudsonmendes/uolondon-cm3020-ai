from typing import Optional

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

    def __init__(self, connection_mode: int):
        self.connection_mode = connection_mode
        self.pid = p.connect(connection_mode)

    def run(self, urdf: Path, steps: Optional[int] = None):
        self._disable_gui_debug_if_applicable()
        self._setup_engine()
        self._setup_ground()
        self._setup_bot(urdf)
        self._wait_completion(steps)

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

    def _wait_completion(self, steps: Optional[int]):
        p.setRealTimeSimulation(1)
        try:
            step = 0
            LOGGER.info("Simulation, Iterative Loop Starting Now")
            while steps is None or step < steps:
                LOGGER.debug(f"Simulation, Step {step} out of {steps if steps else '∞'}")
                p.stepSimulation(physicsClientId=self.pid)
                time.sleep(1.0/240)
                step += 1
            LOGGER.info(f"Simulation, Iterative Loop, Completed Steps: {steps}")
        except p.error as e:
            LOGGER.info("The simulation has been interrupted")
            pass
