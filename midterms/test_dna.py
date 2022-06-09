import unittest
import random

from hypothesis import given
from hypothesis.strategies import integers, floats

from dna import Dna
from gene import Gene
from phenotype import Phenotype


class DnaTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(Dna)

    def test_parse_code_str(self):
        given = [random.random() for _ in range(Gene.length())]
        actual = Dna.parse_dna(",".join([str(base) for base in given]))
        self.assertListEqual(given, actual.code)

    @given(integers(1, 10))
    def test_parse_for_n_gene_without_control(self, n: int):
        given = [random.random() for _ in range(Gene.length() * n)]
        actual = Dna.parse_dna(given)
        self.assertEqual(0, len(actual.genes_control))
        self.assertEqual(n, len(actual.genes_features))
        for i in range(n):
            start = Gene.length()*i
            stop = Gene.length()*(i+1)
            self.assertEqual(given[start:stop], actual.genes_features[i].code)

    @given(integers(1, Gene.length()), floats(0.51, 1))
    def test_parse_for_n_gene_with_control_on(self, n: int, control: float):
        given = [random.random() for _ in range(Gene.length() * n)] + [control] * n
        actual = Dna.parse_dna(given)
        if len(given) % Gene.length() == 0:
            self.assertEqual(0, len(actual.genes_control))
            self.assertEqual(n+1, len(actual.genes_features))
        else:
            self.assertEqual(n, len(actual.genes_control))
            self.assertEqual(n, len(actual.genes_features))
            self.assertTrue(all(actual.genes_control))
        for i in range(n):
            start = Gene.length()*i
            stop = Gene.length()*(i+1)
            self.assertEqual(given[start:stop], actual.genes_features[i].code)

    @given(integers(1, Gene.length()), floats(0, 0.5))
    def test_parse_for_n_gene_with_control_off(self, n: int, control: float):
        given = [random.random() for _ in range(Gene.length() * n)] + [control] * n
        actual = Dna.parse_dna(given)
        actual = Dna.parse_dna(given)
        if len(given) % Gene.length() == 0:
            self.assertEqual(0, len(actual.genes_control))
            self.assertEqual(n+1, len(actual.genes_features))
        else:
            self.assertEqual(n, len(actual.genes_control))
            self.assertEqual(n, len(actual.genes_features))
            self.assertTrue(not any(actual.genes_control))
        for i in range(n):
            start = Gene.length()*i
            stop = Gene.length()*(i+1)
            self.assertEqual(given[start:stop], actual.genes_features[i].code)

    def test_express_no_phenotypes_all_control_genes_off(self):
        gene_count = random.randint(1, 100)
        all_controls_off = [0. for _ in range(gene_count)]
        dna_len = (Gene.length() * gene_count)
        dna_code = [random.random() for _ in range(dna_len)] + all_controls_off
        actual = Dna.parse_dna(dna_code)
        self.assertEqual(0, len(actual.express()))

    def test_express_phenotypes_joint_parent_all_pointing_to_previous_index(self):
        gene_count = random.randint(1, 100)
        all_controls_on = [1. for _ in range(gene_count)]
        dna_len = (Gene.length() * gene_count)
        dna_code = [random.random() for _ in range(dna_len)] + all_controls_on
        dna = Dna.parse_dna(dna_code)
        actual = dna.express()
        self.assertGreater(len(actual), 0)
        for i, phenotype in enumerate(actual):
            self.assertTrue(phenotype.joint_parent is None or phenotype.joint_parent < i)
