import unittest


class DnaTest(unittest.TestCase):

    def test_exists(self):
        import dna
        self.assertIsNotNone(dna.Dna)


unittest.main()
