from typing import List, Optional
import xml.dom.minidom as xml

from creature import Creature


class CreatureRenderer:
    def __init__(self, creature: Creature) -> None:
        self.creature = creature

    def render(self) -> Optional[str]:
        domimpl = xml.getDOMImplementation()
        if domimpl:
            adom = domimpl.createDocument(None, "start", None)
            tag_robot = CreatureRenderer._tag_robot(adom, name=self.creature.name)
            tag_robot.appendChild(CreatureRenderer._tag_robot_link(adom, tree_indexes=[0]))
            return ('<?xml version="1.0"?>' + tag_robot.toprettyxml()).strip()
        else:
            return None

    @staticmethod
    def _tag_robot(adom: xml.Document, name: str) -> xml.Element:
        tag = adom.createElement("robot")
        tag.setAttribute("name", name)
        return tag

    @staticmethod
    def _tag_robot_link(adom: xml.Document, tree_indexes: List[int]) -> xml.Element:
        link_tag = adom.createElement("link")
        link_name = f"part-{'-'.join([str(i) for i in tree_indexes])}"
        link_tag.setAttribute("name", link_name)
        return link_tag
