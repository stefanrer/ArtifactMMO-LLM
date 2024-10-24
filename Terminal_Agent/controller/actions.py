from typing import List
from interfaces import MyCharacterAPI
from controller.skills.action import Action
from controller.skills.perception import Perception, get_perception
from controller.skills.move import move_menu
from controller.skills.gather import gather_menu
from controller.skills.fight import fight_menu
from controller.skills.check_character import character_menu
from controller.skills.craft import craft_menu
from controller.skills.bank import bank_menu


class AllActions:
    def __init__(self, character: MyCharacterAPI):
        self.character = character

    def get_possible_actions(self, perception: Perception) -> List[Action]:
        actions = [
            Action("Quit", "Quit the game", lambda: exit(0)),
            Action("Move Menu", "Open Move Menu", lambda: move_menu(self.character)),
            Action("Character Menu", "Open Character Menu", lambda: character_menu(self.character))
        ]
        if perception.current_map.content:
            if perception.current_map.content.type == "monster":
                actions.append(
                    Action("Fight Menu", "Open Fight Menu",
                           lambda: fight_menu(self.character, perception.current_map.content)))
            if perception.current_map.content.type == "resource":
                actions.append(
                    Action("Gathering Menu", "Open Gathering Menu", lambda: gather_menu(self.character, perception.current_map.content)))
            if perception.current_map.content.type == "workshop":
                actions.append(Action("Crafting Menu", "Open Crafting Menu", lambda: craft_menu(self.character, perception.current_map.content)))
            if perception.current_map.content.type == "bank":
                actions.append(Action("Bank Menu", "Open Bank Menu", lambda: bank_menu(self.character)))
        return actions

    def start(self):
        while True:
            print("Main Menu")
            perception = get_perception(self.character.character_data.x, self.character.character_data.y)
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
