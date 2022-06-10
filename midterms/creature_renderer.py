from typing import List

import xml.dom.minidom as xml
import copy

from creature import Creature, CreaturePart
from phenotype import PhenotypeLinkShape


class CreatureRenderer:
    """
    Responsible for rendering the creature into URDF XML Format.
    """

    def __init__(self, creature: Creature) -> None:
        dom = xml.getDOMImplementation()
        assert dom and creature
        self.creature = creature
        self.adom = dom.createDocument(None, "start", None)
        self.renderer_links = ClassLinksRenderer(self.adom)
        self.renderer_joints = ClassJointsRenderer(self.adom)

    def render(self) -> str:
        robot_tag = self._tag_robot(name=self.creature.name)
        for link_tag in self.renderer_links.render_all(part=self.creature.body):
            robot_tag.appendChild(link_tag)
        for joint_tag in self.renderer_joints.render_all(part=self.creature.body):
            robot_tag.appendChild(joint_tag)
        return ('<?xml version="1.0"?>' + robot_tag.toprettyxml()).strip()

    def _tag_robot(self, name: str) -> xml.Element:
        tag = self.adom.createElement("robot")
        tag.setAttribute("name", name)
        return tag


class ClassLinksRenderer:
    """Responsible for rendering the creature links (body parts)"""

    def __init__(self, adom: xml.Document) -> None:
        self.adom = adom

    def render_all(self, part: CreaturePart, link_hierarchy: List[int] = None) -> List[xml.Element]:
        if not link_hierarchy:
            link_hierarchy = [0]
        tags: List[xml.Element] = []
        tags.append(self._tag_link(part=part, link_hierarchy=link_hierarchy))
        for child_i, child_part in enumerate(part.children):
            child_hierarchy = copy.copy(link_hierarchy) + [child_i]
            tags.extend(self.render_all(part=child_part, link_hierarchy=child_hierarchy))
        return tags

    def _tag_link(self, part: CreaturePart, link_hierarchy: List[int]) -> xml.Element:
        tag = self.adom.createElement("link")
        tag.setAttribute("name", f"part-{'-'.join([str(i) for i in link_hierarchy])}")
        tag.appendChild(self._tag_visual(part=part))
        tag.appendChild(self._tag_collision(part=part))
        tag.appendChild(self._tag_inertial(part=part))
        return tag

    def _tag_visual(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("visual")
        tag.appendChild(self._tag_geometry(part=part))
        return tag

    def _tag_collision(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("collision")
        tag.appendChild(self._tag_geometry(part=part))
        return tag

    def _tag_geometry(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("geometry")
        tag.appendChild(self._tag_shape(part=part))
        return tag

    def _tag_shape(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement(part.phenotype.link_shape.value)
        tag.setAttribute("radius", str(part.phenotype.link_radius))
        if part.phenotype.link_shape == PhenotypeLinkShape.CYLINDER:
            tag.setAttribute("length", str(part.phenotype.link_length))
        return tag

    def _tag_inertial(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("inertial")
        tag.appendChild(self._tag_mass(part))
        tag.appendChild(self._tag_inertia(part))
        return tag

    def _tag_mass(self, part: CreaturePart) -> xml.Element:
        import numpy as np
        mass = np.pi * (part.phenotype.link_radius * part.phenotype.link_radius) * part.phenotype.link_length
        tag = self.adom.createElement("mass")
        tag.setAttribute("value", str(mass))
        return tag

    def _tag_inertia(self, _: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("inertia")
        tag.setAttribute("ixx", "0.03")
        tag.setAttribute("iyy", "0.03")
        tag.setAttribute("izz", "0.03")
        tag.setAttribute("ixy", "0")
        tag.setAttribute("ixz", "0")
        tag.setAttribute("iyx", "0")
        return tag


class ClassJointsRenderer:
    """Responsible for rendering the creature joints (connectors)"""

    def __init__(self, adom: xml.Document) -> None:
        self.adom = adom

    def render_all(self, part: CreaturePart, joint_hierarchy: List[int] = None) -> List[xml.Element]:
        if not joint_hierarchy:
            joint_hierarchy = [0]
        tags: List[xml.Element] = []
        if part.phenotype.joint_parent is not None:
            tags.append(self._tag_joint(part=part, joint_hierarchy=joint_hierarchy))
        for child_i, child_part in enumerate(part.children):
            child_hierarchy = copy.copy(joint_hierarchy) + [child_i]
            tags.extend(self.render_all(part=child_part, joint_hierarchy=child_hierarchy))
        return tags

    def _tag_joint(self, part: CreaturePart, joint_hierarchy: List[int]) -> xml.Element:
        tag = self.adom.createElement("joint")
        tag.setAttribute("name", f"joint-{'-'.join([str(i) for i in joint_hierarchy])}-to-{part.phenotype.joint_parent}")
        tag.setAttribute("type", part.phenotype.joint_type.value)
        tag.appendChild(self._tag_parent(link_hierarchy=joint_hierarchy))
        tag.appendChild(self._tag_child(link_hierarchy=joint_hierarchy))
        tag.appendChild(self._tag_axis(part=part))
        return tag

    def _tag_parent(self, link_hierarchy: List[int]) -> xml.Element:
        tag = self.adom.createElement("parent")
        tag.setAttribute("link", f"link-{'-'.join([str(i) for i in link_hierarchy[:-1]])}")
        return tag

    def _tag_child(self, link_hierarchy: List[int]) -> xml.Element:
        tag = self.adom.createElement("child")
        tag.setAttribute("link", f"link-{'-'.join([str(i) for i in link_hierarchy])}")
        return tag

    def _tag_axis(self, part: CreaturePart) -> xml.Element:
        tag = self.adom.createElement("axis")
        tag.setAttribute("xyz", str(part.phenotype.joint_axis_xyz))
        return tag
