import unittest

from gene import Gene


class GeneTest(unittest.TestCase):

    def test_gene_len(self):
        self.assertEqual(18, Gene.length())

    def test_threshold_for_expression(self):
        self.assertEqual(0.5, Gene.threshold_for_expression())
