import unittest

from gene import Gene


class GeneTest(unittest.TestCase):

    def test_gene_len(self):
        self.assertEqual(17, Gene.length())