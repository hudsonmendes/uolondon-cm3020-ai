from typing import List

import unittest
import random

from dna import Dna
from gene import Gene
from creature import Creature


class CreatureTest(unittest.TestCase):

    def setUp(self) -> None:
        dna_code = (
            [1.] * Gene.length() + # trunk
            [0.] * Gene.length() + # limb-1
            [0.] * Gene.length() + # limb-2
            [1, 1]
        )
        self.dna = Dna.parse_dna(data=dna_code)
        self.creature = Creature.develop_from(dna=self.dna)

    def test_class_exists(self):
        self.assertIsNotNone(Creature)

    def test_creature_dna(self):
        self.assertEqual(self.dna, self.creature.dna)

    def test_creature_body_is_not_none(self):
        self.assertIsNotNone(self.creature.body)

    def test_creature_body_children_is_not_none(self):
        self.assertIsNotNone(self.creature.body.children)

    def test_creature_body_children_has_size_1(self):
        self.assertEqual(1, len(self.creature.body.children))


    @staticmethod
    def create_gene_dna_connected_to(
            part_index: int = 0,
            gene_count: int = 1) -> List[float]:
        gene_dna = [random.random() for _ in range(Phenotype.gen_len())]