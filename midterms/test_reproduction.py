import unittest

from hypothesis import given
from hypothesis.strategies import integers

import random

from reproduction import Reproduction
from gene import Gene


class ReproductionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.adam = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.eve = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.reproduction = Reproduction(dna_code_a=self.adam, dna_code_b=self.eve)
        self.child = self.reproduction.reproduce()

    def test_class_exists(self):
        self.assertIsNotNone(Reproduction)

    def test_breed_generates_new_dna(self):
        self.assertNotEqual(self.child, self.adam)
        self.assertNotEqual(self.child, self.eve)

    def test_breed_generates_dna_not_empty(self):
        self.assertGreater(len(self.child), 0)

    def test_breed_dna_contains_left_sequence_from_adam(self):
        diff_from_adam = [i for i in range(len(self.child)) if i >= len(self.adam) or self.child[i] != self.adam[i]]
        limit = min(diff_from_adam) - 1
        self.assertGreater(len(self.adam[:limit]), 0)
        self.assertLess(len(self.adam[:limit]), len(self.adam))
        self.assertListEqual(self.adam[:limit], self.child[:limit])

    def test_breed_dna_contains_right_sequence_from_eve(self):
        diff_len = len(self.child) - len(self.eve)
        diff_from_eve = [i for i in range(len(self.child)-1, -1, -1) if (i - diff_len) < 0 or self.child[i] != self.eve[i - diff_len]]
        limit = max(diff_from_eve) + 1
        self.assertGreater(len(self.child[limit:]), 0)
        self.assertLess(len(self.eve[:limit]), len(self.eve))
        self.assertListEqual(self.eve[limit-diff_len:], self.child[limit:])
