import unittest
from unittest.mock import patch, Mock

import random

from gene import Gene
from dna import Dna
from creature import Creature
from population import Population


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.population_size = random.randint(100, 1000)
        self.genes_pool = [[random.random() for _ in range(Gene.length())] for _ in range(self.population_size)]
        self.dna_pool = [Dna.parse_dna(genes) for genes in self.genes_pool]
        self.all_creatures = [Creature.develop_from(dna) for dna in self.dna_pool]
        self.viable_creatures = [c for c in self.all_creatures if c]
        self.population = Population(generation_id=random.randint(1, 10), creatures=self.viable_creatures)

    def test_class_exists(self):
        self.assertIsNotNone(Population)

    def test_class_creatures_match_viable_creatures(self):
        self.assertEqual(len(self.viable_creatures), len(self.population.creatures))

    @patch("creature.Creature")
    def test_report_creature_movement_keeps_record_of_first_and_last_positions(self, mock_creature: Mock):
        distances_walked = [(random.random(), random.random(), random.random()) for _ in range(random.randint(1, 10))]
        [self.population.report_movement(mock_creature, dist) for dist in distances_walked]
        actual = self.population.distances_for(mock_creature)
        self.assertEqual(distances_walked[0], actual.initial)
        self.assertEqual(distances_walked[-1], actual.last)
