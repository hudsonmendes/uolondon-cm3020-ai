from typing import List

import xml.dom.minidom as xml
import copy

from creature import Creature, CreaturePart


class CreatureRenderer:
    """
    Responsible for rendering the creature into URDF XML Format.
    """

    def __init__(self, creature: Creature) -> None:
        self.creature = creature
        self.dom = xml.getDOMImplementation()
        assert self.dom
        self.adom = self.dom.createDocument(None, "start", None)

    def render(self) -> str:
        robot_tag = self._tag_robot(name=self.creature.name)
        for link_tag in self._tags_link_recursive(part=self.creature.body):
            robot_tag.appendChild(link_tag)
        return ('<?xml version="1.0"?>' + robot_tag.toprettyxml()).strip()

    def _tags_link_recursive(self, part: CreaturePart, link_hierarchy: List[int] = None) -> List[xml.Element]:
        if not link_hierarchy:
            link_hierarchy = [0]
        tags: List[xml.Element] = []
        tags.append(self._tag_link(part=part,link_hierarchy=link_hierarchy))
        for child_i, child_part in enumerate(part.children):
            child_hierarchy = copy.copy(link_hierarchy) + [child_i]
            tags.extend(self._tags_link_recursive(part=child_part, link_hierarchy=child_hierarchy))
        return tags

    def _tag_robot(self, name: str) -> xml.Element:
        tag = self.adom.createElement("robot")
        tag.setAttribute("name", name)
        return tag

    def _tag_link(self, part: CreaturePart, link_hierarchy: List[int]) -> xml.Element:
        link_tag = self.adom.createElement("link")
        link_name = f"part-{'-'.join([str(i) for i in link_hierarchy])}"
        link_tag.setAttribute("name", link_name)
        return link_tag
