import unittest


class EvolutionTest(unittest.TestCase):

    def test_lass_exists(self):
        from evolution import Evolution
        self.assertIsNotNone(Evolution)