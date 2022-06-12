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
