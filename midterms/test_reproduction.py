import unittest
from unittest.mock import patch

from hypothesis import given
from hypothesis.strategies import integers

import random

from hyperparams import Hyperparams
from reproduction import Reproduction
from gene import Gene


class ReproductionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_hyperparams = patch("reproduction.Hyperparams").start()
        self.mock_hyperparams.point_mutation_rate = 0.1
        self.mock_hyperparams.point_mutation_amount = 0.1
        self.mock_hyperparams.shrink_mutation_rate = 0.1

        self.adam = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.eve = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.reproduction = Reproduction(self.mock_hyperparams)

    def tearDown(self) -> None:
        patch.stopall()

    def test_class_exists(self):
        self.assertIsNotNone(Reproduction)

    def test_reproduce_generates_new_dna(self):
        child = self.reproduction.reproduce(a=self.adam, b=self.eve)
        self.assertNotEqual(child, self.adam)
        self.assertNotEqual(child, self.eve)

    def test_reproduce_generates_dna_not_empty(self):
        child = self.reproduction.reproduce(a=self.adam, b=self.eve)
        self.assertGreater(len(child), 0)

    def test_crossover_dna_contains_left_sequence_from_adam(self):
        child = self.reproduction._crossover(a=self.adam, b=self.eve).tolist()
        diff_from_adam = [i for i in range(len(child)) if i >= len(self.adam) or child[i] != self.adam[i]]
        limit = min(diff_from_adam) - 1
        self.assertGreater(len(self.adam[:limit]), 0)
        self.assertLess(len(self.adam[:limit]), len(self.adam))
        self.assertListEqual(self.adam[:limit], child[:limit])

    def test_crossover_dna_contains_right_sequence_from_eve(self):
        child = self.reproduction._crossover(a=self.adam, b=self.eve).tolist()
        diff_len = len(child) - len(self.eve)
        diff_from_eve = [i for i in range(len(child)-1, -1, -1) if (i - diff_len) < 0 or child[i] != self.eve[i - diff_len]]
        limit = max(diff_from_eve) + 1
        self.assertGreater(len(child[limit:]), 0)
        self.assertLess(len(self.eve[limit-diff_len:]), len(self.eve))
        self.assertListEqual(self.eve[limit-diff_len:],child[limit:])

    def test_point_mutation_adds_1_to_all_bases_with_rate_1(self):
        self.mock_hyperparams.point_mutation_rate = 1.
        self.mock_hyperparams.point_mutation_amount = 1.
        before = [0.1 for _ in range(Gene.length() * random.randint(1, 15))]
        after = self.reproduction._point_mutate(before)
        self.assertTrue(all([base == 0.99999 for base in after]))

    def test_point_mutation_affects_no_gene_to_all_bases_with_rate_0(self):
        self.mock_hyperparams.point_mutation_rate = 0.
        self.mock_hyperparams.point_mutation_amount = 1.
        before = [0.1 for _ in range(Gene.length() * random.randint(1, 15))]
        after = self.reproduction._point_mutate(before)
        self.assertTrue(not any([base == 0.99999 for base in after]))

    def test_shrink_mutation_never_removes_more_than_gen_len(self):
        self.mock_hyperparams.shrink_mutation_rate=1.
        before = [random.random() for _ in range(Gene.length() * random.randint(5, 15))]
        after = self.reproduction._mutate_shrink(before)
        self.assertEqual(len(after), Gene.length())
    
    def test_shrink_mutation_removes_some_genetic_code_when_half(self):
        self.mock_hyperparams.shrink_mutation_rate=0.5
        before = [random.random() for _ in range(Gene.length() * random.randint(5, 15))]
        after = self.reproduction._mutate_shrink(before)
        self.assertLess(len(after), int(len(before)))

    def test_shrink_mutation_does_not_remove_genetic_code_when_zero(self):
        self.mock_hyperparams.shrink_mutation_rate=0.
        before = [random.random() for _ in range(Gene.length() * random.randint(5, 15))]
        after = self.reproduction._mutate_shrink(before)
        self.assertEqual(len(after), len(before))

    def test_grow_mutation_adds_some_genetic_material_when_rate_greater_than_zero(self):
        self.mock_hyperparams.grow_mutation_rate=0.1
        before = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        after = self.reproduction._mutate_grow(before)
        self.assertGreater(len(after), len(before))

    def test_grow_mutation_does_not_add_genetic_material_when_rate_smaller_than_zero(self):
        self.mock_hyperparams.grow_mutation_rate=0.
        before = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        after = self.reproduction._mutate_grow(before)
        self.assertEqual(len(after), len(before))
        