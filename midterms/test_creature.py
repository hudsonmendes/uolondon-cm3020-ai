import unittest

import random

from dna import Dna
from phenotype import Phenotype
from creature import Creature


class CreatureTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dna = Dna.parse_dna(data=[1.] * Phenotype.gen_len(), gene_len=Phenotype.gen_len())

    def test_class_exists(self):
        self.assertIsNotNone(Creature)

    def test_creature_dna(self):
        actual = Creature.develop_from(dna=self.dna)
        self.assertEqual(self.dna, actual.dna)

    def test_creature_parts_root(self):
        actual = Creature.develop_from(dna=self.dna)
        self.assertIsNotNone(actual.body)
        self.assertIsNone(actual.body.parent)
