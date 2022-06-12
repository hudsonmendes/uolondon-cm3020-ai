import unittest
from unittest.mock import patch

import random

from hyperparams import Hyperparams
from evolution import Evolver
from population import Population
from creature import Creature
from dna import Dna


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dna_pool = [[random.random() for _ in range(100)]] * 10
        self.creatures = [Creature.develop_from(dna=Dna.parse_dna(dna)) for dna in self.dna_pool]
        self.viable_creatures = [c for c in self.creatures if c]
        self.elite_previous = self.viable_creatures[3]
        self.elite_offspring = self.viable_creatures[4]

        self.mock_simulation = patch("evolution.Simulation").start()
        self.mock_population = patch("evolution.Population").start()
        self.mock_reproduction = patch("evolution.Reproduction").start()
        self.mock_population.populate_for.return_value.next_roulette_pair.return_value = self.viable_creatures[2], self.viable_creatures[5]
        self.mock_population.populate_for.return_value.fittest = self.elite_previous
        self.mock_population.populate_for.return_value = Population(creatures=self.viable_creatures)
        self.mock_population.return_value.creatures = self.viable_creatures
        self.mock_population.return_value.fittest = self.elite_offspring
        self.mock_reproduction.return_value.reproduce.return_value = self.dna_pool[-1]

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
        self.assertEqual(str(self.elite_previous.dna), self.evolver.evolve(generation_id=0).elite_previous)

    def test_evolve_produces_elite_offspring(self):
        self.assertEqual(str(self.elite_offspring.dna), self.evolver.evolve(generation_id=0).elite_offspring)
