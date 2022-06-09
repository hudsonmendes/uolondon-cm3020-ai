import unittest
import random

from dna import Dna
from phenotype import Phenotype


class DnaTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(Dna)

    def test_parse_code_str(self):
        given = [random.random() for _ in range(random.randint(1, 100))]
        actual = Dna.parse_dna(",".join([str(gene) for gene in given]))
        self.assertListEqual(given, actual.code)

    def test_parse_for_1_gene_len_1_without_control(self):
        actual = Dna.parse_dna("0.5", gene_len=1)
        self.assertEqual([[0.5]], actual.genes_features)
        self.assertEqual([], actual.genes_control)

    def test_parse_for_1_gene_len_1(self):
        actual = Dna.parse_dna("0.5, 1", gene_len=1)
        self.assertEqual([[0.5]], actual.genes_features)
        self.assertEqual([True], actual.genes_control)

    def test_parse_for_2_gene_len_1(self):
        actual = Dna.parse_dna("0.1, 0.2, 0, 1", gene_len=1)
        self.assertEqual([[0.1], [0.2]], actual.genes_features)
        self.assertEqual([False, True], actual.genes_control)

    def test_parse_for_3_gene_len_1(self):
        actual = Dna.parse_dna("0.1, 0.2, 0.3, 0.5, 0.8, 0.2", gene_len=1)
        self.assertEqual([[0.1], [0.2], [0.3]], actual.genes_features)
        self.assertEqual([False, True, False], actual.genes_control)

    def test_parse_for_1_gene_len_2(self):
        actual = Dna.parse_dna("0.1, 0.2, 0.3", gene_len=2)
        self.assertEqual([[0.1, 0.2]], actual.genes_features)
        self.assertEqual([False], actual.genes_control)

    def test_parse_for_1_gene_len_3(self):
        actual = Dna.parse_dna("0.1, 0.2, 0.3, 0.51", gene_len=3)
        self.assertEqual([[0.1, 0.2, 0.3]], actual.genes_features)
        self.assertEqual([True], actual.genes_control)

    def test_parse_for_2_gene_len_2(self):
        actual = Dna.parse_dna("0.1, 0.2, 0.3, 0.4, 0, 1", gene_len=2)
        self.assertEqual([[0.1, 0.2], [0.3, 0.4]], actual.genes_features)
        self.assertEqual([False, True], actual.genes_control)

    def test_express_phenotypes_all_control_genes_on(self):
        gene_count = random.randint(1, 100)
        all_controls_on = [1. for _ in range(gene_count)]
        gene_len = Phenotype.gen_len()
        dna_len = (gene_len * gene_count)
        dna_code = [random.random() for _ in range(dna_len)] + all_controls_on
        actual = Dna.parse_dna(dna_code, gene_len=gene_len)
        self.assertEqual(gene_count, len(actual.express()))

    def test_express_no_phenotypes_all_control_genes_off(self):
        gene_count = random.randint(1, 100)
        all_controls_off = [0. for _ in range(gene_count)]
        gene_len = Phenotype.gen_len()
        dna_len = (gene_len * gene_count)
        dna_code = [random.random() for _ in range(dna_len)] + all_controls_off
        actual = Dna.parse_dna(dna_code, gene_len=gene_len)
        self.assertEqual(0, len(actual.express()))

    def test_express_phenotypes_joint_parent_all_pointing_to_previous_index(self):
        gene_count = random.randint(1, 100)
        all_controls_on = [1. for _ in range(gene_count)]
        gene_len = Phenotype.gen_len()
        dna_len = (gene_len * gene_count)
        dna_code = [random.random() for _ in range(dna_len)] + all_controls_on
        dna = Dna.parse_dna(dna_code, gene_len=gene_len)
        actual = dna.express()
        self.assertGreater(len(actual), 0)
        for i, phenotype in enumerate(actual):
            self.assertTrue(phenotype.joint_parent is None or phenotype.joint_parent < i)
