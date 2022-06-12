import unittest
from unittest.mock import patch, Mock

import random

from evolution import Evolver


class EvolutionTest(unittest.TestCase):

    def test_lass_exists(self):
        self.assertIsNotNone(Evolver)

    def setUp(self) -> None:
        self.evolution = Evolver()

    @patch("simulation.Simulation")
    def test_evolve_shoud_run_simulation(self, simulation_mock: Mock):
        generations = random.randint(10, 100)
        self.evolution.evolve(generations=generations)
        self.assertEquals(generations, len(simulation_mock.mock_calls))
