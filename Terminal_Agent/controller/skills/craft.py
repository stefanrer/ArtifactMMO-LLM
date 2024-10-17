from typing import AnyStr

from controller.skills.action import Action
from interfaces import MyCharacterAPI, items
from models.map import Content


def possible_actions(character: MyCharacterAPI, crafts):
    actions = [
        Action("Back", "Go back", lambda *args: None),
        Action("Craft", "Craft", lambda : craft_item(character, crafts)),
    ]
    return actions


def craft_item(character: MyCharacterAPI, crafts):
    while True:
        print("Craft Item Menu")
        print("Select Craft:")
        print(f"0)Back")
        for i, craft in enumerate(crafts):
            print(f"{i+1}){craft.craft.quantity} {craft.type}, {craft.name}, Needs: {craft.craft.items}")
        craft_number = int(input("Enter Craft number:"))
        if craft_number > len(crafts) or craft_number < 0:
            print("Invalid craft number")
            continue
        if craft_number == 0:
            break
        character.craft(crafts[craft_number - 1].code)


def get_crafts(workshop: AnyStr, skill_level: int):
    print("Available crafts:")
    crafts = items.filter(craft_skill=workshop, max_level=skill_level)
    for i, craft in enumerate(crafts):
        print(f"{i+1}){craft.craft.quantity} {craft.type}, {craft.name}, Needs: {craft.craft.items}")
    return crafts


def craft_menu(character: MyCharacterAPI, workshop: Content):
    while True:
        print("Crafting Menu")
        level = character.character_data.get_skill_level(workshop.code)
        print(f"Workshop: {workshop.code}, Skill level: {level}")
        crafts = get_crafts(workshop.code, level)
        actions = possible_actions(character, crafts)
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
