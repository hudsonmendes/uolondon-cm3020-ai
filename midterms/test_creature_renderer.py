from typing import List, Dict, Any, Optional, Union

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

    def test_render_creature_with_single_link(self):
        creature = CreatureRendererTest._create_creature(connections={})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link')

    def test_render_creature_with_two_links(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 2, 'link')

    def test_render_creature_with_three_links(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0, 2: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 3, 'link')

    def test_render_creature_link_contains_visual_geometry_box(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shapes=[0.01])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/visual/geometry/box')

    def test_render_creature_link_contains_visual_geometry_cylinder(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shapes=[0.34])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/visual/geometry/cylinder')

    def test_render_creature_link_contains_visual_geometry_cylinder_length(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shapes=[0.34])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'length': str(creature.body.phenotype.link_length)}, 'link/visual/geometry/cylinder')

    def test_render_creature_link_contains_visual_geometry_sphere(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shapes=[0.67])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/visual/geometry/sphere')

    @staticmethod
    def _create_creature(
            connections: Dict[int, int],
            link_shapes: List[float] = None) -> Optional[Creature]:
        dna_code: List[float] = CreatureRendererTest._create_gene(connected_with_index=None, all_parts_count=0)
        if link_shapes and link_shapes[0] is not None:
            dna_code[0] = link_shapes[0]
        for part_ix, connecting_with_ix in connections.items():
            part_dna = CreatureRendererTest._create_gene(connected_with_index=connecting_with_ix, all_parts_count=part_ix)
            if link_shapes and len(link_shapes) > part_ix + 1:
                dna_code[part_ix] = link_shapes[part_ix + 1]
            dna_code.extend(part_dna)
        dna_code += [1.] * (len(connections.items()) + 1)
        return Creature.develop_from(name="lab-rat", dna=Dna.parse_dna(dna_code))

    @ staticmethod
    def _create_gene(connected_with_index: Optional[int], all_parts_count: int) -> List[float]:
        gene_code = [random.random() for _ in range(Gene.length())]
        if connected_with_index and all_parts_count > 0:
            gene_code[5] = (connected_with_index * (1. / float(all_parts_count))) + pow(10, -6)
        return gene_code
