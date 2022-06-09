import unittest
import random

from primordial_soup import PrimordialSoup


class PrimordialSoupTest(unittest.TestCase):

    def test_spark_life_with_organic_molecule_len_1(self):
        actual = PrimordialSoup(organic_molecule_len=1).spark_life()
        self.assertEqual(1, len(actual.genes_features))
        self.assertEqual(1, len(actual.genes_features[0]))
        self.assertEqual(0, len(actual.genes_control))

    def test_spark_life_with_organic_molecule_len_2(self):
        actual = PrimordialSoup(organic_molecule_len=2).spark_life()
        self.assertEqual(1, len(actual.genes_features))
        self.assertEqual(1, len(actual.genes_features[0]))
        self.assertEqual(1, len(actual.genes_control))

    def test_spark_life_with_organic_molecule_len_3(self):
        actual = PrimordialSoup(organic_molecule_len=3).spark_life()
        self.assertEqual(1, len(actual.genes_features))
        self.assertEqual(2, len(actual.genes_features[0]))
        self.assertEqual(1, len(actual.genes_control))

    def test_spark_life_with_organic_molecule_len_n(self):
        n = random.randint(3, 100)
        actual = PrimordialSoup(organic_molecule_len=n).spark_life()
        self.assertEqual(1, len(actual.genes_features))
        self.assertEqual(n - 1, len(actual.genes_features[0]))
        self.assertEqual(1, len(actual.genes_control))
