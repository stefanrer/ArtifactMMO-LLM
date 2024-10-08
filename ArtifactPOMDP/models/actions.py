from dataclasses import dataclass, field
from typing import List, Dict, Optional, AnyStr
from collections.abc import Callable

from ArtifactPOMDP.api.character import MyCharacterAPI
from ArtifactPOMDP.api.map import MapAPI
from ArtifactPOMDP.models.map import Map

from .character import Character
from .resource import AllResources
from .monster import AllMonsters
from .map import AllMaps


@dataclass
class Action:
    name: str
    description: str
    function: Callable[..., None]


@dataclass()
class Perception:
    current_map: Optional[Map] = None
    right_map: Optional[Map] = None
    left_map: Optional[Map] = None
    up_map: Optional[Map] = None
    down_map: Optional[Map] = None
    up_right_map: Optional[Map] = None
    up_left_map: Optional[Map] = None
    down_right_map: Optional[Map] = None
    down_left_map: Optional[Map] = None


class AllActions:
    def __init__(self, character: MyCharacterAPI, maps: AllMaps) -> None:
        self.character = character
        self.all_maps = maps
        self.perception = self.get_perception()

    def get_current_map(self) -> Map:
        return self.character.get_map(x=self.character.character_data.x, y=self.character.character_data.y)

    def get_possible_actions(self) -> List[Action]:
        actions = []
        if self.perception.up_map:
            actions.append(Action(f"Move_UP: {self.perception.up_map}", "Move character 1 map up", self.character.move_up))
        if self.perception.down_map:
            actions.append(Action(f"Move_DOWN: {self.perception.down_map}", "Move character 1 map down", self.character.move_down))
        if self.perception.left_map:
            actions.append(Action(f"Move_LEFT: {self.perception.left_map}", "Move character 1 map left", self.character.move_left))
        if self.perception.right_map:
            actions.append(Action(f"Move_RIGHT: {self.perception.right_map}", "Move character 1 map right", self.character.move_right))
        if self.perception.up_right_map:
            actions.append(Action(f"Move_UP_RIGHT: {self.perception.up_right_map}", "Move character 1 map up-right", self.character.move_up_right))
        if self.perception.up_left_map:
            actions.append(Action(f"Move_UP_LEFT: {self.perception.up_left_map}", "Move character 1 map up-left", self.character.move_up_left))
        if self.perception.down_right_map:
            actions.append(Action(f"Move_DOWN_RIGHT: {self.perception.down_right_map}", "Move character 1 map down-right", self.character.move_down_right))
        if self.perception.down_left_map:
            actions.append(Action(f"Move_DOWN_LEFT: {self.perception.down_left_map}", "Move character 1 map down-left", self.character.move_down_left))
        if self.perception.current_map.content:
            if self.perception.current_map.content.type == "monster":
                actions.append(
                    Action("Fight", "Start a fight against a monster on the character's map", self.character.fight))
            if self.perception.current_map.content.type == "resource":
                actions.append(Action("Gathering", "Harvest a resource on the character's map", self.character.gather))
            # Action("Crafting", "Crafting an item", self.character.craft),
            # Action("Equip_item", "Equip an item on your character", self.character.equip)
        return actions

    def get_perception(self):
        perception = Perception()
        matrix = self.all_maps.get_3x3_matrix(self.character.character_data.x, self.character.character_data.y)
        perception.current_map = matrix[1][1]
        perception.up_map = matrix[0][1]
        perception.down_map = matrix[2][1]
        perception.left_map = matrix[1][0]
        perception.right_map = matrix[1][2]
        perception.up_right_map = matrix[0][2]
        perception.up_left_map = matrix[0][0]
        perception.down_right_map = matrix[2][2]
        perception.down_left_map = matrix[2][0]
        return perception
