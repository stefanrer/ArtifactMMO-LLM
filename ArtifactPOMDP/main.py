from interfaces import (
    MAPS,
    ITEMS,
    MONSTERS,
    RESOURCES,
    CHARACTERS,
)

from models.actions import AllActions

current_character = CHARACTERS[0]
print(f"Current character: {current_character.character_data.name}")

while True:
    actions = AllActions(current_character, MAPS)
    print(f"Current map: {actions.perception.current_map}")
    print("Available actions:")
    for i, action in enumerate(actions.get_possible_actions()):
        print(f"{i+1}){action.name}")
    action_number = int(input("Enter action number: "))
    if action_number > len(actions.get_possible_actions()) or action_number == 0:
        print("Invalid action number")
        continue
    action = actions.get_possible_actions()[action_number - 1]
    print(f"You chose {action.name}")
    if action.name == "Quit":
        break
    action.function()
