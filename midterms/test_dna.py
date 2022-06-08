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

    def test_read_genes_for_1_gene_len_1(self):
        self.assertEqual([[0.5]], dna.Dna.read("0.5, 1", gene_len=1).genes)

    def test_read_genes_for_2_gene_len_1(self):
        self.assertEqual([[0.1], [0.2]], dna.Dna.read("0.1, 0.2, 1, 1", gene_len=1).genes)

    def test_read_genes_for_3_gene_len_1(self):
        self.assertEqual([[0.1], [0.2], [0.3]], dna.Dna.read("0.1, 0.2, 0.3, 1, 1, 1", gene_len=1).genes)

    def test_read_genes_for_1_gene_len_2(self):
        self.assertEqual([[0.1, 0.2]], dna.Dna.read("0.1, 0.2, 1", gene_len=2).genes)

    def test_read_genes_for_1_gene_len_3(self):
        self.assertEqual([[0.1, 0.2, 0.3]], dna.Dna.read("0.1, 0.2, 0.3, 1", gene_len=3).genes)

    def test_read_genes_for_2_gene_len_2(self):
        self.assertEqual([[0.1, 0.2], [0.3, 0.4]], dna.Dna.read("0.1, 0.2, 0.3, 0.4, 1, 1", gene_len=2).genes)
