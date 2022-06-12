import unittest
from unittest.mock import patch, Mock

from hypothesis import given
from hypothesis.strategies import integers

from hyperparams import Hyperparams
from evolution import Evolver


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.hyperparams = Hyperparams()
        self.evolver = Evolver(hyperparams=self.hyperparams)

    def test_lass_exists(self):
        self.assertIsNotNone(Evolver)

    @given(integers(-1, 100))
    def test_evolve_produces_evolution(self, n: int):
        self.assertIsNotNone(self.evolver.evolve(generation_id=n))

    @given(integers(-1, 100))
    def test_genesis_evolution_produces_generation_id(self, n: int):
        self.assertEqual(n, self.evolver.evolve(generation_id=n).generation_id)

    @given(integers(-1, 100))
    def test_genesis_evolution_produces_2_previous_elite_when_not_based_in_previous_generation(self, n: int):
        self.assertEqual(2, len(self.evolver.evolve(generation_id=n).previous_elite))
