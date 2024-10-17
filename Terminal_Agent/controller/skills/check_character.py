from controller.skills.action import Action
from interfaces import MyCharacterAPI


def possible_actions(character: MyCharacterAPI):
    actions = [
        Action("Back", "Go back", lambda *args: None),
        Action("Check Stats", "Get Character Stats", lambda *args: character.character_data.get_stats()),
        Action("Check Skills", "Get Character Skills", lambda *args: character.character_data.get_skills()),
        Action("Check Inventory", "Get Character Inventory", lambda *args: get_inventory(character)),
        Action("Delete Item", "Delete Item from Character Inventory", lambda *args: delete_menu(character)),
    ]
    return actions


def get_inventory(character: MyCharacterAPI):
    inventory = character.character_data.get_inventory()
    print(f"{character.character_data.name} Inventory:")
    for i, item in enumerate(inventory):
        print(f"{i+1}){item.code}, quantity: {item.quantity}")


def delete_menu(character: MyCharacterAPI):
    while True:
        print("Select Item to Delete:")
        items = character.character_data.get_inventory()
        print(f"0)Back")
        for i, item in enumerate(items):
            print(f"{i+1}){item.code}, quantity: {item.quantity}")
        item_number = int(input("Enter Item number:"))
        if item_number > len(items) or item_number < 0:
            print("Invalid action number")
            continue
        if item_number == 0:
            break
        quantity = int(input("Enter quantity:"))
        if quantity < 0 or quantity >= 100:
            quantity = 0
        character.delete_item(items[item_number-1].code, quantity)
        print(f"Deleted {quantity} {items[item_number-1].code}")


def character_menu(character: MyCharacterAPI):
    while True:
        print(f"Current character: {character.character_data.name}, Level: {character.character_data.level}")
        actions = possible_actions(character)
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