from audioop import bias
import unittest

from hypothesis import given
from hypothesis.strategies import integers, floats

from primordial_soup import PrimordialSoup
from gene import Gene

class PrimordialSoupTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(PrimordialSoup)

    @given(integers(0, 1000))
    def test_spark_life_generate_random_creature_with_correct_gene_count(self, n):
        dna_code = PrimordialSoup.spark_life(gene_count=n)
        self.assertGreaterEqual(len(dna_code) // Gene.length(), n)

    @given(integers(1, 50))
    def test_spark_life_control_genes_at_least_one_activated(self, n: int):
        dna_code = PrimordialSoup.spark_life(gene_count=n, bias_to_expression=0.)
        expression_bases = [dna_code[i] for i in range(Gene.length()-1, len(dna_code), Gene.length())]
        expressable_genes = [expression_base > 0.5 for expression_base in expression_bases]
        self.assertGreaterEqual(len(expressable_genes), 1)

    @given(integers(10, 50), floats(0.7, 1))
    def test_spark_life_control_genes_activated_above_bias(self, n: int, b: float):
        dna_code = PrimordialSoup.spark_life(gene_count=n, bias_to_expression=b)
        expression_bases = [dna_code[i] for i in range(Gene.length()-1, len(dna_code), Gene.length())]
        expressable_genes = [expression_base > 0.5 for expression_base in expression_bases]
        self.assertGreaterEqual(len(expressable_genes) / n, b)