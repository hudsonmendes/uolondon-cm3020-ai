from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

from numpy import pi

from gene import Gene


@dataclass
class Phenotype:
    """
    Represents the physical expression of the Genetic data
    of a Single Gene in the DNA, which will be rendered as
    a part of the robot with its joints.
    """
    link_shape: "PhenotypeLinkShape"
    link_length: float
    link_radius: float
    link_recurrence: int
    link_mass: float
    joint_parent: Optional[int]
    joint_type: "PhenotypeJointType"
    joint_axis_xyz: "PhenotypeJointXYZ"
    joint_origin_rpy_1: float
    joint_origin_rpy_2: float
    joint_origin_rpy_3: float
    joint_origin_xyz_1: "PhenotypeJointXYZ"
    joint_origin_xyz_2: "PhenotypeJointXYZ"
    joint_origin_xyz_3: "PhenotypeJointXYZ"
    control_waveform: "PhenotypeWaveForm"
    control_amp: float
    control_freq: float

    @staticmethod
    def parse_dna(gene: Gene, gene_count: int) -> "Phenotype":
        return Phenotype(
            link_shape=PhenotypeLinkShape.parse_float(gene.link_shape),
            link_length=gene.link_length * 2.,
            link_radius=gene.link_radius,
            link_recurrence=int(gene.link_recurrence * 3),
            link_mass=gene.link_mass,
            joint_parent=int(max(0, min(gene.joint_parent, 0.99) * (gene_count-1))) if gene_count > 1 else None,
            joint_type=PhenotypeJointType.parse_float(gene.joint_type),
            joint_axis_xyz=PhenotypeJointXYZ.parse_float(gene.joint_axis_xyz),
            joint_origin_rpy_1=gene.joint_origin_rpy_1 * 2*pi,
            joint_origin_rpy_2=gene.joint_origin_rpy_2 * 2*pi,
            joint_origin_rpy_3=gene.joint_origin_rpy_3 * 2*pi,
            joint_origin_xyz_1=PhenotypeJointXYZ.parse_float(gene.joint_origin_xyz_1),
            joint_origin_xyz_2=PhenotypeJointXYZ.parse_float(gene.joint_origin_xyz_2),
            joint_origin_xyz_3=PhenotypeJointXYZ.parse_float(gene.joint_origin_xyz_3),
            control_waveform=PhenotypeWaveForm.parse_float(gene.control_waveform),
            control_amp=gene.control_amp * 0.25,
            control_freq=gene.control_freq,
        )


class PhenotypeLinkShape(Enum):
    CYLINDER: str = "cylinder"
    SPHERE: str = "sphere"

    @staticmethod
    def parse_float(number: float) -> "PhenotypeLinkShape":
        if number <= 0.5:
            return PhenotypeLinkShape.CYLINDER
        else:
            return PhenotypeLinkShape.SPHERE


class PhenotypeJointType(Enum):
    FIXED: str = "fixed"
    REVOLUTE: str = "revolute"
    PRISMATIC: str = "prismatic"

    @staticmethod
    def parse_float(number: float) -> "PhenotypeJointType":
        if number <= 0.33:
            return PhenotypeJointType.FIXED
        elif number <= 0.66:
            return PhenotypeJointType.REVOLUTE
        else:
            return PhenotypeJointType.PRISMATIC


class PhenotypeWaveForm(Enum):
    PULSE: str = "pulse"
    SINE: str = "sine"

    @staticmethod
    def parse_float(number: float) -> "PhenotypeWaveForm":
        if number <= 0.5:
            return PhenotypeWaveForm.PULSE
        else:
            return PhenotypeWaveForm.SINE


@dataclass
class PhenotypeJointXYZ:
    x: int
    y: int
    z: int

    @staticmethod
    def parse_float(number: float) -> "PhenotypeJointXYZ":
        if number <= 0.33:
            return PhenotypeJointXYZ(x=1, y=0, z=0)
        elif number <= 0.66:
            return PhenotypeJointXYZ(x=0, y=1, z=0)
        else:
            return PhenotypeJointXYZ(x=0, y=0, z=1)
