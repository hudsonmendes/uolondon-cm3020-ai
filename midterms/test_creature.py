import unittest

import random

from dna import Dna
from phenotype import Phenotype
from creature import Creature, CreatureBody


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
        self.assertIsNotNone(actual.root)
        self.assertIsNone(actual.root.parent)
