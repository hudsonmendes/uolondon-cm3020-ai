import unittest

from hypothesis import given
from hypothesis.strategies import integers

from primordial_soup import PrimordialSoup
from gene import Gene

class PrimordialSoupTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(PrimordialSoup)

    @given(integers(0, 1000))
    def test_spark_life_generate_random_creature_with_correct_gene_count(self, n):
        dna_code = PrimordialSoup.spark_life(gene_count=n)
        self.assertGreaterEqual(len(dna_code) // Gene.length(), n)