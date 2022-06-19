from typing import List, Optional

import unittest
import random

from dna import Dna
from gene import Gene
from creature import Creature, CreatureMovement


class CreatureTest(unittest.TestCase):

    def setUp(self) -> None:
        dna_code = (
            CreatureTest.create_gene_code(connected_with_index=None, all_parts_count=0, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=0, all_parts_count=1, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=2, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=3, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=4, expressable=False)
        )
        self.dna = Dna.parse_dna(data=dna_code)
        self.creature = Creature.develop_from(dna=self.dna, threshold_for_expression=0.5)

    def test_class_exists(self):
        self.assertIsNotNone(Creature)

    def test_creature_dna(self):
        self.assertEqual(self.dna, self.creature.dna)

    def test_creature_phenotypes_is_not_none(self):
        self.assertIsNotNone(self.creature.phenotypes)

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
            CreatureTest.create_gene_code(connected_with_index=None, all_parts_count=0, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=0, all_parts_count=1, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=2, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=3, expressable=True) +
            CreatureTest.create_gene_code(connected_with_index=1, all_parts_count=4, expressable=True)
        )
        dna = Dna.parse_dna(data=dna_code)
        creature = Creature.develop_from(dna=dna, threshold_for_expression=0.5)
        self.assertEqual(3, len(creature.body.children[0].children))

    def test_lethality_too_high(self):
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 1)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 2)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 3)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 4)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 5)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 6)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (0, 0, 7)))

    def test_lethality_too_quick(self):
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (1, 1, 1)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (2, 2, 1)))
        self.assertFalse(CreatureMovement.check_lethality((0, 0, 0), (3, 3, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (4, 4, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (5, 5, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (6, 6, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (7, 7, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (6, 8, 1)))
        self.assertTrue(CreatureMovement.check_lethality((0, 0, 0), (8, 8, 1)))

    @staticmethod
    def create_gene_code(
            connected_with_index: Optional[int],
            all_parts_count: int,
            expressable: bool) -> List[float]:
        gene_code = [random.random() for _ in range(Gene.length()-1)]
        if connected_with_index and all_parts_count > 0:
            gene_code[5] = (connected_with_index * (1. / float(all_parts_count))) + pow(10, -6)
        gene_code.append(1. if expressable else 0.)
        return gene_code
