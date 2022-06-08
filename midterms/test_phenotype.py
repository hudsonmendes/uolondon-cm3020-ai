from typing import List
import unittest

from numpy import pi
from hypothesis import given
from hypothesis.strategies import lists, floats

import phenotype


class PhenotypeTest(unittest.TestCase):

    @given(floats(0, 0.33))
    def test_parse_link_shape_box(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeLinkShape.BOX,
            phenotype.PhenotypeLinkShape.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_link_shape_cylinder(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeLinkShape.CYLINDER,
            phenotype.PhenotypeLinkShape.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_link_shape_sphere(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeLinkShape.SPHERE,
            phenotype.PhenotypeLinkShape.parse_float(number))

    @given(floats(0, 0.33))
    def test_parse_joint_type_fixed(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointType.FIXED,
            phenotype.PhenotypeJointType.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_joint_type_revolute(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointType.REVOLUTE,
            phenotype.PhenotypeJointType.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_joint_type_prismatic(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointType.PRISMATIC,
            phenotype.PhenotypeJointType.parse_float(number))

    @given(floats(0, 0.5))
    def test_parse_wave_form_pulse(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeWaveForm.PULSE,
            phenotype.PhenotypeWaveForm.parse_float(number))

    @given(floats(0.51, 1))
    def test_parse_wave_form_sine(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeWaveForm.SINE,
            phenotype.PhenotypeWaveForm.parse_float(number))

    @given(floats(0, 0.33))
    def test_parse_xyz_100(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointXYZ(1, 0, 0),
            phenotype.PhenotypeJointXYZ.parse_float(number))

    @given(floats(0.34, 0.66))
    def test_parse_xyz_010(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointXYZ(0, 1, 0),
            phenotype.PhenotypeJointXYZ.parse_float(number))

    @given(floats(0.67, 1))
    def test_parse_xyz_001(self, number: float):
        self.assertEqual(
            phenotype.PhenotypeJointXYZ(0, 0, 1),
            phenotype.PhenotypeJointXYZ.parse_float(number))

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_link_length(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertAlmostEqual(numbers[1] * 2, actual.link_length)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_link_radius(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertAlmostEqual(numbers[2], actual.link_radius)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_link_recurrence(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(int(numbers[3] * 3), actual.link_recurrence)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_link_mass(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[4], actual.link_mass)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_joint_origin_rpy_1(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[7] * 2*pi, actual.joint_origin_rpy_1)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_joint_origin_rpy_2(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[8] * 2*pi, actual.joint_origin_rpy_2)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_joint_origin_rpy_3(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[9] * 2*pi, actual.joint_origin_rpy_3)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_control_amp(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[14] * 0.25, actual.control_amp)

    @given(lists(floats(0, 1), min_size=16, max_size=20))
    def test_control_freq(self, numbers: List[float]):
        actual = phenotype.Phenotype.parse_dna(gene_dna=numbers)
        self.assertEqual(numbers[15], actual.control_freq)
