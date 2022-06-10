from typing import List, Dict, Optional

import unittest
from xmltest import XMLAssertions
import random

from creature_renderer import CreatureRenderer
from creature import Creature
from dna import Dna
from gene import Gene


class CreatureRendererTest(unittest.TestCase, XMLAssertions):

    def test_class_exists(self):
        self.assertIsNotNone(CreatureRenderer)

    def test_render_creature_with_single_part(self):
        creature = CreatureRendererTest._create_creature(connections={})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link')

    def test_render_creature_with_two_parts_interconected(self):
        creature = CreatureRendererTest._create_creature(connections={1:0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 2, 'link')

    def test_render_creature_with_three_parts_interconected(self):
        creature = CreatureRendererTest._create_creature(connections={1:0, 2:0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 3, 'link')

    @staticmethod
    def _create_creature(connections: Dict[int, int]) -> Optional[Creature]:
        dna_code: List[float] = CreatureRendererTest._create_gene(connected_with_index=None, all_parts_count=0)
        for part_ix, connecting_with_ix in connections.items():
            part_dna = CreatureRendererTest._create_gene(connected_with_index=connecting_with_ix, all_parts_count=part_ix)
            dna_code.extend(part_dna)
        dna_code += [ 1. ] * (len(connections.items()) + 1)
        return Creature.develop_from(name="lab-rat", dna=Dna.parse_dna(dna_code))

    @ staticmethod
    def _create_gene(connected_with_index: Optional[int], all_parts_count: int) -> List[float]:
        gene_code = [random.random() for _ in range(Gene.length())]
        if connected_with_index and all_parts_count > 0:
            gene_code[5] = (connected_with_index * (1. / float(all_parts_count))) + pow(10, -6)
        return gene_code
