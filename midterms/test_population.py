from collections import namedtuple
import unittest
from unittest.mock import patch, Mock

import random

from population import Population


class PopulationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.population_size = random.randint(100, 1000)
        self.gene_count = random.randint(1, 10)
        self.population = Population.populate_for(size=self.population_size, gene_count=self.gene_count)

    def test_class_exists(self):
        self.assertIsNotNone(Population)

    def test_class_creatures_match_viable_creatures(self):
        self.assertEqual(self.population_size, len(self.population.creatures))

    def test_fittest_shows_creature_who_travelled_furthest(self):
        creatures = self.population.creatures[0:3]
        creature1, creature2, creature3 = creatures
        creature1.movement.track((0.1, 0.2, 0.3))
        creature2.movement.track((1., 2., 3.))
        creature3.movement.track((10., 20., 30.))
        top1 = self.population.fittest
        self.assertEqual(top1, creature3)

    def test_calculate_fitness_map_creates_not_a_uniform_distribution_when_creatures_moved(self):
        for creature in self.population.creatures:
            creature.movement.track((random.random(), random.random(), random.random()))
        fm = self.population._calculate_fitness_map(self.population.creatures)
        self.assertTrue(all([c.movement.last is not None for c in self.population.creatures]))
        for i in range(len(fm) - 3):
            self.assertNotAlmostEqual(fm[i+2]-fm[i+1], fm[i+1]-fm[i+0])

    def test_calculate_fitness_map_creates_uniform_distribution_when_none_moved(self):
        fm = self.population._calculate_fitness_map(self.population.creatures)
        self.assertTrue(all([c.movement.last is None for c in self.population.creatures]))
        for i in range(len(fm) - 3):
            self.assertAlmostEqual(fm[i+2]-fm[i+1], fm[i+1]-fm[i+0])
