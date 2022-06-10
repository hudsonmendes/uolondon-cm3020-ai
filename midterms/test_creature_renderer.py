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

    def test_render_creature_link_contains_visual_geometry_cylinder(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.01])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/visual/geometry/cylinder')

    def test_render_creature_link_contains_visual_geometry_sphere(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.51])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/visual/geometry/sphere')

    def test_render_creature_link_contains_collision_geometry_cylinder(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.00])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/collision/geometry/cylinder')

    def test_render_creature_link_contains_collision_geometry_sphere(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.51])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/collision/geometry/sphere')

    def test_render_creature_link_contains_visual_geometry_cylinder_length(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.00])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'length': str(creature.body.phenotype.link_length)}, 'link/visual/geometry/cylinder')

    def test_render_creature_link_contains_visual_geometry_cylinder_radius(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.00])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'radius': str(creature.body.phenotype.link_radius)}, 'link/visual/geometry/cylinder')

    def test_render_creature_link_contains_visual_geometry_sphere_no_length(self):
        from xml.etree import ElementTree
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.51])
        actual = CreatureRenderer(creature).render()
        doc = ElementTree.fromstring(actual)
        ele = doc.find('link/visual/geometry/sphere')
        self.assertFalse('length' in ele.attrib)
        self.assertTrue('radius' in ele.attrib)

    def test_render_creature_link_contains_visual_geometry_sphere_radius(self):
        creature = CreatureRendererTest._create_creature(connections={}, link_shape=[0.51])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'radius': str(creature.body.phenotype.link_radius)}, 'link/visual/geometry/sphere')

    def test_render_creature_link_contains_inertial_mass(self):
        creature = CreatureRendererTest._create_creature(connections={})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/inertial/mass')

    def test_render_creature_link_contains_inertial_inertia(self):
        creature = CreatureRendererTest._create_creature(connections={})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'link/inertial/inertia')

    def test_render_creature_no_joint(self):
        creature = CreatureRendererTest._create_creature(connections={})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 0, 'joint')

    def test_render_creature_one_joint(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'joint')

    def test_render_creature_two_joint(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0, 2: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 2, 'joint')

    def test_render_creature_three_joint(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0, 2: 1, 3: 1})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 3, 'joint')

    def test_render_creature_joint_contains_parent(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'joint/parent')

    def test_render_creature_joint_contains_parent_link(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'link': 'link-0'}, 'joint/parent')

    def test_render_creature_joint_contains_child(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'joint/child')

    def test_render_creature_joint_contains_child_link(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'link': 'link-0-0'}, 'joint/child')

    def test_render_creature_joint_contains_axis(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'joint/axis')

    def test_render_creature_joint_contains_axis_xyz_x(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0}, joint_axis_xyz=[0.00])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'xyz': '1 0 0'}, 'joint/axis')

    def test_render_creature_joint_contains_axis_xyz_y(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0}, joint_axis_xyz=[0.34])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'xyz': '0 1 0'}, 'joint/axis')

    def test_render_creature_joint_contains_axis_xyz_z(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0}, joint_axis_xyz=[0.67])
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeAttributes(actual, {'xyz': '0 0 1'}, 'joint/axis')

    def test_render_creature_joint_contains_limit(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0}, joint_axis_xyz=[0.67])
        actual = CreatureRenderer(creature).render()
        expected = {'effort': '1', 'upper': '-3.1415', 'lower': '3.1415', 'velocity': '1'}
        self.assertXPathNodeAttributes(actual, expected, 'joint/limit')

    def test_render_creature_joint_contains_origin(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0})
        actual = CreatureRenderer(creature).render()
        self.assertXPathNodeCount(actual, 1, 'joint/origin')

    def test_render_creature_joint_contains_origin_rpy(self):
        creature = CreatureRendererTest._create_creature(connections={1: 0}, joint_axis_xyz=[0.67])
        actual = CreatureRenderer(creature).render()
        p = creature.body.children[0].phenotype
        expected = {
            'rpy': f'{p.joint_origin_rpy_r} {p.joint_origin_rpy_p} {p.joint_origin_rpy_y}',
            'xyz': f'{p.joint_origin_xyz_x} {p.joint_origin_xyz_y} {p.joint_origin_xyz_z}'
        }
        self.assertXPathNodeAttributes(actual, expected, 'joint/origin')

    @staticmethod
    def _create_creature(
            connections: Dict[int, int],
            link_shape: List[float] = None,
            joint_axis_xyz: List[float] = None) -> Optional[Creature]:

        dna_code: List[float] = CreatureRendererTest._create_gene(connected_with_index=None, all_parts_count=0)
        for part_ix, connecting_with_ix in connections.items():
            part_dna = CreatureRendererTest._create_gene(connected_with_index=connecting_with_ix, all_parts_count=part_ix)
            dna_code.extend(part_dna)

        if link_shape:
            for i in range(len(link_shape)):
                dna_code[i * Gene.length()] = link_shape[i]

        if joint_axis_xyz:
            for i in range(len(joint_axis_xyz)):
                dna_code[(i+1) * Gene.length() + 7] = joint_axis_xyz[i]

        dna_code += [1.] * (len(connections.items()) + 1)
        return Creature.develop_from(name="lab-rat", dna=Dna.parse_dna(dna_code))

    @ staticmethod
    def _create_gene(connected_with_index: Optional[int], all_parts_count: int) -> List[float]:
        gene_code = [random.random() for _ in range(Gene.length())]
        if connected_with_index and all_parts_count > 0:
            gene_code[5] = (connected_with_index * (1. / float(all_parts_count))) + pow(10, -6)
        return gene_code
