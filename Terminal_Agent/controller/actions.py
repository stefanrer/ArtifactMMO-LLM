from typing import List
from interfaces import MyCharacterAPI
from controller.skills.action import Action
from controller.skills.perception import Perception, get_perception
from controller.skills.move import move_character
from controller.skills.gather import gather_resource
from controller.skills.fight import fight_monster


class AllActions:
    def __init__(self, character: MyCharacterAPI):
        self.character = character

    def get_possible_actions(self, perception: Perception) -> List[Action]:
        actions = [
            Action("Quit", "Quit the game", lambda: exit(0)),
            Action("Move Menu", "Open Move Menu", lambda: move_character(self.character)),
            # Action("Inventory", "View your character's inventory", lambda: self.inventory())
        ]
        if perception.current_map.content:
            if perception.current_map.content.type == "monster":
                actions.append(
                    Action("Fight Menu", "Open Fight Menu",
                           lambda: fight_monster(self.character, perception.current_map.content)))
            if perception.current_map.content.type == "resource":
                actions.append(
                    Action("Gathering Menu", "Open Gathering Menu", lambda: gather_resource(self.character, perception.current_map.content)))
            # Action("Crafting", "Crafting an item", self.character.craft),
            # Action("Equip_item", "Equip an item on your character", self.character.equip)
        return actions

    def start(self):
        while True:
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

    def inventory(self):
        inventory = [inventory_item for inventory_item in self.character.character_data.inventory if
                     inventory_item.code != ""]
        print(f"Inventory: {inventory}")
        actions = [
            Action("Back", "Go back", lambda *args: None),
            Action("Delete Item", "Delete an item from your character's inventory",
                   lambda: self.character.delete_item()),
            Action("Recycle Item", "Recycle an item from your character's inventory",
                   lambda: self.character.recycle_item()),
            Action("Equip Item", "Equip an item on your character", lambda: self.character.equip_item()),
            Action("Unequip Item", "Unequip an item on your character", lambda: self.character.unequip_item())
        ]
        while True:
            print("Select Action:")
            for i, action in enumerate(actions):
                print(f"{i}){action.name}")
            action_number = int(input("Enter Action number:"))
            if action_number > len(actions) or action_number < 0:
                print("Invalid action number")
                continue
            if action_number == 0:
                break
            else:
                action = actions[action_number]
                print(f"You chose {action.name}")
                action.function()
