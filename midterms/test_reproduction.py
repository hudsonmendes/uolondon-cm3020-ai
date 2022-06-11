import unittest

from hypothesis import given
from hypothesis.strategies import integers

import random

from reproduction import Reproduction, ReproductiveSettings
from gene import Gene


class ReproductionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.adam = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.eve = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        self.reproduction = Reproduction()

    def test_class_exists(self):
        self.assertIsNotNone(Reproduction)

    def test_reproduce_generates_new_dna(self):
        child = self.reproduction.reproduce()
        self.assertNotEqual(child, self.adam)
        self.assertNotEqual(child, self.eve)

    def test_reproduce_generates_dna_not_empty(self):
        child = self.reproduction.reproduce()
        self.assertGreater(len(child), 0)

    def test_crossover_dna_contains_left_sequence_from_adam(self):
        child = self.reproduction._crossover()
        diff_from_adam = [i for i in range(len(child)) if i >= len(self.adam) or child[i] != self.adam[i]]
        limit = min(diff_from_adam) - 1
        self.assertGreater(len(self.adam[:limit]), 0)
        self.assertLess(len(self.adam[:limit]), len(self.adam))
        self.assertListEqual(self.adam[:limit], child[:limit])

    def test_reproduce_applies_point_mutation_when_enabled(self):
        reproduction_pme = Reproduction(settings=ReproductiveSettings(point_mutation_rate=1., point_mutation_amount=1.))
        reproduction_pmd = Reproduction(settings=ReproductiveSettings(point_mutation_enabled=False, point_mutation_rate=1., point_mutation_amount=1.))
        actual_pme = reproduction_pme.reproduce(a=self.adam, b=self.eve)
        actual_pmd = reproduction_pmd.reproduce(a=self.adam, b=self.eve)
        self.assertNotEqual(actual_pme, actual_pmd)
        self.assertTrue(all([base == 0.99999 for base in actual_pme]))
        self.assertTrue(not any([base == 0.99999 for base in actual_pmd]))

    def test_crossover_dna_contains_right_sequence_from_eve(self):
        child = self.reproduction._crossover()
        diff_len = len(child) - len(self.eve)
        diff_from_eve = [i for i in range(len(child)-1, -1, -1) if (i - diff_len) < 0 or child[i] != self.eve[i - diff_len]]
        limit = max(diff_from_eve) + 1
        self.assertGreater(len(child[limit:]), 0)
        self.assertLess(len(self.eve[limit-diff_len:]), len(self.eve))
        self.assertListEqual(self.eve[limit-diff_len:],child[limit:])

    def test_point_mutation_adds_1_to_all_bases_with_rate_1(self):
        reproduction = Reproduction(settings=ReproductiveSettings(point_mutation_rate=1., point_mutation_amount=1.))
        before = [0.1 for _ in range(Gene.length() * random.randint(1, 15))]
        after = reproduction._point_mutate(before)
        self.assertTrue(all([base == 0.99999 for base in after]))

    def test_point_mutation_affects_no_gene_to_all_bases_with_rate_0(self):
        reproduction = Reproduction(settings=ReproductiveSettings(point_mutation_rate=0., point_mutation_amount=1.))
        before = [0.1 for _ in range(Gene.length() * random.randint(1, 15))]
        after = reproduction._point_mutate(before)
        self.assertTrue(not any([base == 0.99999 for base in after]))

    def test_shrink_mutation_never_removes_more_than_gen_len(self):
        reproduction = Reproduction(settings=ReproductiveSettings(shrink_mutation_rate=1.))
        before = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        after = reproduction._shrink_mutate(before)
        self.assertLess(len(after), Gene.length())
    
    def test_shrink_mutation_removes_some_genetic_code_when_half(self):
        reproduction = Reproduction(settings=ReproductiveSettings(shrink_mutation_rate=0.5))
        before = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        after = reproduction._shrink_mutate(before)
        self.assertLess(len(after), int(len(before)))

    def test_shrink_mutation_does_not_remove_genetic_code_when_zero(self):
        reproduction = Reproduction(settings=ReproductiveSettings(shrink_mutation_rate=0.))
        before = [random.random() for _ in range(Gene.length() * random.randint(1, 15))]
        after = reproduction._shrink_mutate(before)
        self.assertEqual(len(after), len(before))
        