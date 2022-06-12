import unittest
from unittest.mock import patch

import random

from hyperparams import Hyperparams
from evolution import Evolver
from simulation import Simulation
from reproduction import Reproduction
from population import Population
from creature import Creature
from dna import Dna
from fitness import Fitness


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dna_pool = [[random.random() for _ in range(100)]] * 10
        self.creatures = [Creature.develop_from(dna=Dna.parse_dna(dna)) for dna in self.dna_pool]
        self.viable_creatures = [c for c in self.creatures if c]
        self.elite_previous = self.viable_creatures[3]
        self.elite_offspring = self.viable_creatures[4]

        self.mock_simulate = patch.object(Simulation, "simulate").start()
        self.mock_reproduce = patch.object(Reproduction, "reproduce").start()
        self.mock_reproduce.return_value = self.dna_pool[-1]
        self.mock_populate = patch.object(Population, "populate_for").start()
        self.mock_populate.return_value = Population(creatures=self.viable_creatures)
        self.mock_elite = patch.object(Fitness, "calculate_fittest_from").start()
        self.mock_elite.return_value = self.viable_creatures[3]

        self.hyperparams = Hyperparams()
        self.evolver = Evolver(hyperparams=self.hyperparams)

    def tearDown(self) -> None:
        patch.stopall()

    def test_lass_exists(self):
        self.assertIsNotNone(Evolver)

    def test_evolve_produces_evolution(self):
        self.assertIsNotNone(self.evolver.evolve(generation_id=0))

    def test_evolve_produces_generation_id(self):
        n = random.randint(1, 100)
        self.assertEqual(n, self.evolver.evolve(generation_id=n).generation_id)

    def test_evolve_produces_elite_previous(self):
        self.assertEqual(self.elite_previous.dna.code, self.evolver.evolve(generation_id=0).elite_previous)

    def test_evolve_produces_elite_offspring(self):
        self.assertEqual(self.elite_offspring.dna.code, self.evolver.evolve(generation_id=0).elite_offspring)
