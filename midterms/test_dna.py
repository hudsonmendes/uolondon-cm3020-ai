import unittest
import random

import dna


class DnaTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(dna.Dna)

    def test_read_code(self):
        given = [random.random() for _ in range(random.randint(1, 100))]
        actual = dna.Dna.read(",".join([str(gene) for gene in given]))
        self.assertListEqual(given, actual.code)

    def test_read_for_1_gene_len_1(self):
        actual = dna.Dna.read("0.5, 1", gene_len=1)
        self.assertEqual([[0.5]], actual.genes_features)
        self.assertEqual([True], actual.genes_control)

    def test_read_for_2_gene_len_1(self):
        actual = dna.Dna.read("0.1, 0.2, 0, 1", gene_len=1)
        self.assertEqual([[0.1], [0.2]], actual.genes_features)
        self.assertEqual([False, True], actual.genes_control)

    def test_read_for_3_gene_len_1(self):
        actual = dna.Dna.read("0.1, 0.2, 0.3, 0.5, 0.8, 0.2", gene_len=1)
        self.assertEqual([[0.1], [0.2], [0.3]], actual.genes_features)
        self.assertEqual([False, True, False], actual.genes_control)

    def test_read_for_1_gene_len_2(self):
        actual = dna.Dna.read("0.1, 0.2, 0.3", gene_len=2)
        self.assertEqual([[0.1, 0.2]], actual.genes_features)
        self.assertEqual([False], actual.genes_control)

    def test_read_for_1_gene_len_3(self):
        actual = dna.Dna.read("0.1, 0.2, 0.3, 0.51", gene_len=3)
        self.assertEqual([[0.1, 0.2, 0.3]], actual.genes_features)
        self.assertEqual([True], actual.genes_control)

    def test_read_for_2_gene_len_2(self):
        actual = dna.Dna.read("0.1, 0.2, 0.3, 0.4, 0, 1", gene_len=2)
        self.assertEqual([[0.1, 0.2], [0.3, 0.4]], actual.genes_features)
        self.assertEqual([False, True], actual.genes_control)
