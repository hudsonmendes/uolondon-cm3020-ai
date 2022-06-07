import unittest

import random
import dna


class DnaTest(unittest.TestCase):

    def test_exists(self):
        self.assertIsNotNone(dna.Dna)

    def test_dna_code(self):
        given = [random.random() for _ in range(12)]
        actual = dna.Dna(code=given)
        self.assertEqual(given, actual.code)


unittest.main()
