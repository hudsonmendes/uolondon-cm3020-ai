import unittest

import random

from dna import Dna
from phenotype import Phenotype
from creature import Creature


class CreatureTest(unittest.TestCase):

    def setUp(self) -> None:
        dna_code = (
            [1.] * Phenotype.gen_len() + # trunk
            [0.] * Phenotype.gen_len() + # limb-1
            [1, 1]
        )
        self.dna = Dna.parse_dna(data=dna_code, gene_len=Phenotype.gen_len())
        self.creature = Creature.develop_from(dna=self.dna)

    def test_class_exists(self):
        self.assertIsNotNone(Creature)

    def test_creature_dna(self):
        self.assertEqual(self.dna, self.creature.dna)

    def test_creature_body_is_not_none(self):
        self.assertIsNotNone(self.creature.body)

    def test_creature_body_parent_is_none(self):
        self.assertIsNone(self.creature.body.parent)

    def test_creature_body_children_is_not_none(self):
        self.assertIsNotNone(self.creature.body.children)

    def test_creature_body_children_has_size_1(self):
        self.assertEqual(1, len(self.creature.body.children))