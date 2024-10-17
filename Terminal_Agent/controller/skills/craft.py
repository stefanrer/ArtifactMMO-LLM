from typing import AnyStr

from controller.skills.action import Action
from interfaces import MyCharacterAPI, items
from models.map import Content


def possible_actions(character: MyCharacterAPI, crafts):
    actions = [
        Action("Back", "Go back", lambda *args: None),
        Action("Craft", "Craft", lambda: craft_item(character, crafts)),
        Action("Recycle", "Recycle", lambda: recycle_item(character)),
    ]
    return actions


def check_recyclable(character: MyCharacterAPI, inventory):
    recyclable_items = []
    for item in inventory:
        item_full = items.get_one(item.code)
        if item_full.craft:
            if item_full.craft.skill == "gearcrafting" or item_full.craft.skill == "weaponcrafting":
                recyclable_items.append(item)
    return recyclable_items


def recycle_item(character: MyCharacterAPI):
    while True:
        print("Recycle Item Menu")
        print("Select Item to Recycle:")
        inventory = character.character_data.get_inventory()
        recyclable_items = check_recyclable(character, inventory)
        print(f"0)Back")
        for i, item in enumerate(recyclable_items):
            print(f"{i + 1}){item.code}, quantity: {item.quantity}")
        item_number = int(input("Enter Item number:"))
        if item_number > len(recyclable_items) or item_number < 0:
            print("Invalid Item number")
            continue
        if item_number == 0:
            break
        quantity = int(input("Enter quantity:"))
        if quantity < 0 or quantity >= 100:
            quantity = 0
        character.recycle_item(recyclable_items[item_number - 1].code, quantity)


def craft_item(character: MyCharacterAPI, crafts):
    while True:
        print("Craft Item Menu")
        print("Select Craft:")
        print(f"0)Back")
        for i, craft in enumerate(crafts):
            print(f"{i + 1}){craft.craft.quantity} {craft.type}, {craft.name}, Needs: {craft.craft.items}")
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
        print(f"{i + 1}){craft.craft.quantity} {craft.type}, {craft.name}, Needs: {craft.craft.items}")
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
