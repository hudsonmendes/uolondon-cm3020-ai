import unittest
from src.domain.gene import Gene


class GeneTest(unittest.TestCase):

    def test_gene_class_exists(self):
        self.assertIsNotNone(Gene)
