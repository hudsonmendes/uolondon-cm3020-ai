import unittest


class GeneTest(unittest.TestCase):

    def test_gene_class_exists(self):
        from src.domain.gene import Gene
        self.assertIsNotNone(Gene)
