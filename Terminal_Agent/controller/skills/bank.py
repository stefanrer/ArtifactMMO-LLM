from controller.skills.action import Action
from interfaces import MyCharacterAPI
from interfaces import bank


def possible_actions(character: MyCharacterAPI):
    actions = [
        Action("Back", "Go back", lambda *args: None),
        Action("Deposit item", "Deposit Item", lambda: deposit_item(character)),
        Action("Withdraw item", "Withdraw Item", lambda: withdraw_item(character)),
    ]
    return actions


def deposit_item(character: MyCharacterAPI):
    while True:
        print("Deposit Item Menu")
        print("Select Item to Deposit:")
        items = character.character_data.get_inventory()
        print(f"0)Back")
        for i, item in enumerate(items):
            print(f"{i+1}){item.code}, quantity: {item.quantity}")
        item_number = int(input("Enter Item number:"))
        if item_number > len(items) or item_number < 0:
            print("Invalid Item number")
            continue
        if item_number == 0:
            break
        quantity = int(input("Enter quantity:"))
        if quantity < 0 or quantity >= 100:
            quantity = 0
        print(quantity)
        character.deposit_bank(items[item_number-1].code, quantity)


def withdraw_item(character: MyCharacterAPI):
    while True:
        bank_items = bank.get_all_items().items
        print("Withdraw Item Menu")
        print(f"0)Back")
        for i, item in enumerate(bank_items):
            print(f"{i+1}){item.code}, quantity: {item.quantity}")
        item_number = int(input("Enter Item number:"))
        if item_number > len(bank_items) or item_number < 0:
            print("Invalid Item number")
            continue
        if item_number == 0:
            break
        quantity = int(input("Enter quantity:"))
        if quantity < 0 or quantity >= 100:
            quantity = 0
        character.withdraw_bank(bank_items[item_number-1].code, quantity)


def bank_menu(character: MyCharacterAPI):
    while True:
        bank_items = bank.get_all_items().items
        print("Bank Menu")
        print(f"Bank gold: {bank.get_gold()}")
        print(f"Bank Items: {bank_items}")
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