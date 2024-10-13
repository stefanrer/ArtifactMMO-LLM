from typing import List, Dict, Optional, AnyStr
from dataclasses import dataclass
from collections.abc import Callable
import models
from models import Map
from interfaces import maps, MyCharacterAPI


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


@dataclass
class Action:
    name: str
    description: str
    function: Callable[..., None]


class AllActions:
    def __init__(self, character: MyCharacterAPI):
        self.character = character

    def get_perception(self):
        perception = Perception()
        matrix = maps.get_3x3_matrix(self.character.character_data.x, self.character.character_data.y)
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

    def get_possible_actions(self, perception: Perception) -> List[Action]:
        actions = [
            Action("Quit", "Quit the game", lambda: exit(0)),
            Action("Move", "Move character 1 map", lambda: self.move(perception))
        ]
        if perception.current_map.content:
            if perception.current_map.content.type == "monster":
                actions.append(
                    Action("Fight", "Start a fight against a monster on the character's map", lambda: self.character.fight()))
            if perception.current_map.content.type == "resource":
                actions.append(Action("Gathering", "Harvest a resource on the character's map", lambda: self.character.gather()))
            # Action("Crafting", "Crafting an item", self.character.craft),
            # Action("Equip_item", "Equip an item on your character", self.character.equip)
        return actions

    def start(self):
        while True:
            perception = self.get_perception()
            print(f"Current Map: {perception.current_map}")
            print("Select Action: ")
            actions = self.get_possible_actions(perception)
            for i, action in enumerate(actions):
                print(f"{i}){action.name}")
            action_number = int(input("Enter action number:"))
            if action_number > len(actions) or action_number < 0:
                print("Invalid action number")
                continue
            action = actions[action_number]
            print(f"You chose {action.name}")
            action.function()

    def move(self, perception: Perception):
        print(f"Current Map: {perception.current_map}")
        actions = [Action("Back", "Go back", lambda *args: None)]
        if perception.up_map:
            actions.append(Action(f"Move_UP: {perception.up_map}", "Move character 1 map up", lambda: self.character.move(perception.up_map)))
        if perception.down_map:
            actions.append(Action(f"Move_DOWN: {perception.down_map}", "Move character 1 map down", lambda: self.character.move(perception.down_map)))
        if perception.left_map:
            actions.append(Action(f"Move_LEFT: {perception.left_map}", "Move character 1 map left", lambda: self.character.move(perception.left_map)))
        if perception.right_map:
            actions.append(Action(f"Move_RIGHT: {perception.right_map}", "Move character 1 map right", lambda: self.character.move(perception.right_map)))
        if perception.up_right_map:
            actions.append(Action(f"Move_UP_RIGHT: {perception.up_right_map}", "Move character 1 map up-right", lambda: self.character.move(perception.up_right_map)))
        if perception.up_left_map:
            actions.append(Action(f"Move_UP_LEFT: {perception.up_left_map}", "Move character 1 map up-left", lambda: self.character.move(perception.up_left_map)))
        if perception.down_right_map:
            actions.append(Action(f"Move_DOWN_RIGHT: {perception.down_right_map}", "Move character 1 map down-right", lambda: self.character.move(perception.down_right_map)))
        if perception.down_left_map:
            actions.append(Action(f"Move_DOWN_LEFT: {perception.down_left_map}", "Move character 1 map down-left", lambda: self.character.move(perception.down_left_map)))
        while True:
            print("Select Map:")
            for i, action in enumerate(actions):
                print(f"{i}){action.name}")
            action_number = int(input("Enter Map number:"))
            if action_number > len(actions) or action_number < 0:
                print("Invalid action number")
                continue
            if action_number == 0:
                break
            else:
                action = actions[action_number]
                print(f"You chose {action.name}")
                return action.function()
