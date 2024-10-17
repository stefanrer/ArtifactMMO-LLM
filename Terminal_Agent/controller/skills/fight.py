from controller.skills.action import Action
from interfaces import MyCharacterAPI
from interfaces import resources
from interfaces import monsters
from models.map import Content


def possible_actions(character: MyCharacterAPI, map_content: Content):
    actions = [
        Action("Back", "Go back", lambda *args: None),
        # Action("Check drops", "Check Resource Drops", lambda: get_monster_drops(map_content)),
        Action("Fight 1 time", "Fight 1 time", lambda: character.fight()),
    ]
    return actions


def get_monster_drops(map_content: Content):
    drops = monsters.check_drops(monster_code=map_content.code)
    print(drops)


def fight_menu(character: MyCharacterAPI, map_content: Content):
    monster = monsters.get(map_content.code)
    print(monster)
    while True:
        actions = possible_actions(character, map_content)
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