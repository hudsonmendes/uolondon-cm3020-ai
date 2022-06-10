from typing import List, Optional

import unittest
import random

from dna import Dna
from gene import Gene
from creature import Creature


class CreatureTest(unittest.TestCase):

    def setUp(self) -> None:
        dna_code = (
            CreatureTest.create_gene_code(connected_with_index=None, all_parts_count=0) +
            CreatureTest.create_gene_code(connected_with_index=0, all_parts_count=1) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=2) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=3) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=4) +
            [1, 1, 1, 1, 0]
        )
        self.dna = Dna.parse_dna(data=dna_code)
        self.creature = Creature.develop_from(name="lab-rat", dna=self.dna)

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

    def test_creature_atavistic_behavior_only_2_parts_expressed_because_last_is_disabled(self):
        self.assertEqual(2, len(self.creature.body.children[0].children))

    def test_creature_atavistic_behavior_all_3_parts_expressed_because_last_is_enabled(self):
        dna_code = (
            CreatureTest.create_gene_code(connected_with_index=None, all_parts_count=0) +
            CreatureTest.create_gene_code(connected_with_index=0, all_parts_count=1) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=2) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=3) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=4) +
            [1, 1, 1, 1, 1]
        )
        dna = Dna.parse_dna(data=dna_code)
        creature = Creature.develop_from(name="other-lab-rat", dna=dna)
        self.assertEqual(3, len(creature.body.children[0].children))

    @staticmethod
    def create_gene_code(connected_with_index: Optional[int], all_parts_count: int) -> List[float]:
        gene_code = [random.random() for _ in range(Gene.length())]
        if connected_with_index and all_parts_count > 0:
            gene_code[5] = (connected_with_index * (1. / float(all_parts_count))) + pow(10, -6)
        return gene_code
