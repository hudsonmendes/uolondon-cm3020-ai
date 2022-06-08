from argparse import ArgumentError
import unittest

import random
import dna
import genome


class DnaTest(unittest.TestCase):

    def setUp(self) -> None:
        self.gene_len = genome.Genome.get_gene_len()
        self.dna_code = [random.random() for _ in range((self.gene_len * 3) + 3)]
        self.subject = dna.Dna(code=self.dna_code, gene_len=self.gene_len)

    def test_exists(self):
        self.assertIsNotNone(dna.Dna)

    def test_has_gene_len(self):
        self.assertEquals(self.gene_len, self.subject.gene_len)

    def test_has_code(self):
        self.assertEqual(self.dna_code, self.subject.code)

    def test_ensures_code_not_empty_for_any_length(self):
        dna_code = []
        for gene_len in [0, 1, random.randint(2, 100)]:
            with self.assertRaises(dna.DnaCodeVoid):
                dna.Dna(code=dna_code, gene_len=gene_len)

    def test_ensures_code_gene_len_aligned(self):
        for gene_count in range(1, 10):
            dna_code = [random.random() for _ in range((self.gene_len * gene_count) + gene_count)]
            self.assertIsNotNone(dna.Dna(code=dna_code, gene_len=self.gene_len))
            with self.assertRaises(dna.DnaCodeMisalignedException):
                dna.Dna(code=dna_code[:-1], gene_len=self.gene_len)
            with self.assertRaises(dna.DnaCodeMisalignedException):
                dna.Dna(code=dna_code[-1:], gene_len=self.gene_len)
