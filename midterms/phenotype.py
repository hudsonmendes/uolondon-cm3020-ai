from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

from numpy import pi


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
    joint_parent: float
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
    def gen_len() -> int:
        return 17

    @staticmethod
    def parse_dna(gene_dna: List[float]) -> "Phenotype":
        assert len(gene_dna) >= Phenotype.gen_len()
        return Phenotype(
            link_shape=PhenotypeLinkShape.parse_float(gene_dna[0]),
            link_length=gene_dna[1] * 2.,
            link_radius=gene_dna[2],
            link_recurrence=int(gene_dna[3] * 3),
            link_mass=gene_dna[4],
            joint_parent=gene_dna[5],
            joint_type=PhenotypeJointType.parse_float(gene_dna[6]),
            joint_axis_xyz=PhenotypeJointXYZ.parse_float(gene_dna[7]),
            joint_origin_rpy_1=gene_dna[8] * 2*pi,
            joint_origin_rpy_2=gene_dna[9] * 2*pi,
            joint_origin_rpy_3=gene_dna[10] * 2*pi,
            joint_origin_xyz_1=PhenotypeJointXYZ.parse_float(gene_dna[11]),
            joint_origin_xyz_2=PhenotypeJointXYZ.parse_float(gene_dna[12]),
            joint_origin_xyz_3=PhenotypeJointXYZ.parse_float(gene_dna[13]),
            control_waveform=PhenotypeWaveForm.parse_float(gene_dna[14]),
            control_amp=gene_dna[15] * 0.25,
            control_freq=gene_dna[16],
        )


class PhenotypeLinkShape(Enum):
    BOX: str = "box"
    CYLINDER: str = "cylinder"
    SPHERE: str = "sphere"

    @staticmethod
    def parse_float(number: float) -> "PhenotypeLinkShape":
        if number <= 0.33:
            return PhenotypeLinkShape.BOX
        elif number <= 0.66:
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
