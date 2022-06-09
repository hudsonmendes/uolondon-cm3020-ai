from typing import List
import unittest
import random

from numpy import pi
from hypothesis import given
from hypothesis.strategies import lists, floats

from phenotype import (Phenotype, PhenotypeLinkShape, PhenotypeJointType, PhenotypeWaveForm, PhenotypeJointXYZ)


class PhenotypeTest(unittest.TestCase):

    @given(floats(0, 0.33))
    def test_parse_link_shape_box(self, number: float):
        self.assertEqual(
            PhenotypeLinkShape.BOX,
            PhenotypeLinkShape.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_link_shape_cylinder(self, number: float):
        self.assertEqual(
            PhenotypeLinkShape.CYLINDER,
            PhenotypeLinkShape.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_link_shape_sphere(self, number: float):
        self.assertEqual(
            PhenotypeLinkShape.SPHERE,
            PhenotypeLinkShape.parse_float(number))

    @given(floats(0, 0.33))
    def test_parse_joint_type_fixed(self, number: float):
        self.assertEqual(
            PhenotypeJointType.FIXED,
            PhenotypeJointType.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_joint_type_revolute(self, number: float):
        self.assertEqual(
            PhenotypeJointType.REVOLUTE,
            PhenotypeJointType.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_joint_type_prismatic(self, number: float):
        self.assertEqual(
            PhenotypeJointType.PRISMATIC,
            PhenotypeJointType.parse_float(number))

    @given(floats(0, 0.5))
    def test_parse_wave_form_pulse(self, number: float):
        self.assertEqual(
            PhenotypeWaveForm.PULSE,
            PhenotypeWaveForm.parse_float(number))

    @given(floats(0.51, 1))
    def test_parse_wave_form_sine(self, number: float):
        self.assertEqual(
            PhenotypeWaveForm.SINE,
            PhenotypeWaveForm.parse_float(number))

    @given(floats(0, 0.33))
    def test_parse_xyz_100(self, number: float):
        self.assertEqual(
            PhenotypeJointXYZ(1, 0, 0),
            PhenotypeJointXYZ.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_xyz_010(self, number: float):
        self.assertEqual(
            PhenotypeJointXYZ(0, 1, 0),
            PhenotypeJointXYZ.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_xyz_001(self, number: float):
        self.assertEqual(
            PhenotypeJointXYZ(0, 0, 1),
            PhenotypeJointXYZ.parse_float(number))

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_link_length(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertAlmostEqual(numbers[1] * 2, actual.link_length)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_link_radius(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertAlmostEqual(numbers[2], actual.link_radius)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_link_recurrence(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(int(numbers[3] * 3), actual.link_recurrence)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_link_mass(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[4], actual.link_mass)
        
    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_none_for_single_gene(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertIsNone(actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_zero_for_2_genes(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=2)
        self.assertEqual(0, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_zero_for_3_genes_and_low_joint_parent(self, numbers: List[float]):
        numbers[5] = 0.01
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=3)
        self.assertEqual(0, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_one_for_3_genes_and_high_joint_parent(self, numbers: List[float]):
        numbers[5] = 0.51
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=3)
        self.assertEqual(1, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_zero_for_4_genes_and_low_joint_parent(self, numbers: List[float]):
        numbers[5] = 0.01
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=4)
        self.assertEqual(0, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_one_for_4_genes_and_mid_joint_parent(self, numbers: List[float]):
        numbers[5] = 0.34
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=4)
        self.assertEqual(1, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_parent_two_for_4_genes_and_high_joint_parent(self, numbers: List[float]):
        numbers[5] = 0.67
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=4)
        self.assertEqual(2, actual.joint_parent)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_origin_rpy_1(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[8] * 2*pi, actual.joint_origin_rpy_1)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_origin_rpy_2(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[9] * 2*pi, actual.joint_origin_rpy_2)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_joint_origin_rpy_3(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[10] * 2*pi, actual.joint_origin_rpy_3)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_control_amp(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[15] * 0.25, actual.control_amp)

    @given(lists(floats(0, 1), min_size=17, max_size=17))
    def test_control_freq(self, numbers: List[float]):
        actual = Phenotype.parse_dna(gene_dna=numbers, gene_count=1)
        self.assertEqual(numbers[16], actual.control_freq)
