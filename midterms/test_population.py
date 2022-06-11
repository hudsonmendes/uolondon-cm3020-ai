import unittest
from unittest.mock import patch, Mock

import random

from population import Population


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.generation = Population(generation_id=random.randint(1, 10))

    def test_class_exists(self):
        self.assertIsNotNone(Population)

    @patch("creature.Creature")
    def test_report_creature_movement_keeps_record_of_first_and_last_positions(self, mock_creature: Mock):
        distances_walked = [(random.random(), random.random(), random.random()) for _ in range(random.randint(1, 10))]
        [self.generation.report_movement(mock_creature, dist) for dist in distances_walked]
        actual = self.generation.distances_for(mock_creature)
        self.assertEqual(distances_walked[0], actual.initial)
        self.assertEqual(distances_walked[-1], actual.last)
