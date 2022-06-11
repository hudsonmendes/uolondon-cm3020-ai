import unittest


class EvolutionTest(unittest.TestCase):

    def test_class_exists(self):
        from evolution import Evolution
        self.assertIsNotNone(Evolution)
