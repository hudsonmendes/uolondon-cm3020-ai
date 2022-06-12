import unittest
import random
import itertools

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

    def test_parse_code_float(self):
        given = [random.random() for _ in range(Gene.length())]
        actual = Dna.parse_dna(given)
        self.assertListEqual(given, actual.code)

    @given(integers(Gene.length(), Gene.length() * 2))
    def test_parse_code_different_sizes(self, n):
        given = [random.random() for _ in range(n)]
        actual = Dna.parse_dna(given)
        self.assertListEqual(given[:Gene.length()], actual.code[:Gene.length()])

    @given(integers(1, 100), floats(0.51, 1))
    def test_parse_code_results_in_n_genes(self, n: int, expressability: float):
        given = []
        for _ in range(n):
            given.extend([random.random() for _ in range(Gene.length()-1)])
            given.append(expressability)
        actual = Dna.parse_dna(given)
        self.assertEqual(n, len(actual.genes))

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

    def test_as_str_csv(self):
        given = [random.random() for _ in range(Gene.length())]
        dna = Dna.parse_dna(given)
        self.assertEqual(",".join([str(base) for base in given]), str(dna))
