from controller.skills.action import Action
from controller.skills.perception import get_perception
from interfaces import MyCharacterAPI


def possible_actions(character: MyCharacterAPI):
    actions = [Action("Back", "Go back", lambda *args: None)]
    perception = get_perception(character.character_data.x, character.character_data.y)
    if perception.up_map:
        actions.append(Action(f"Move_UP: {perception.up_map}", "Move character 1 map up",
                              lambda: character.move(perception.up_map)))
    if perception.down_map:
        actions.append(Action(f"Move_DOWN: {perception.down_map}", "Move character 1 map down",
                              lambda: character.move(perception.down_map)))
    if perception.left_map:
        actions.append(Action(f"Move_LEFT: {perception.left_map}", "Move character 1 map left",
                              lambda: character.move(perception.left_map)))
    if perception.right_map:
        actions.append(Action(f"Move_RIGHT: {perception.right_map}", "Move character 1 map right",
                              lambda: character.move(perception.right_map)))
    if perception.up_right_map:
        actions.append(Action(f"Move_UP_RIGHT: {perception.up_right_map}", "Move character 1 map up-right",
                              lambda: character.move(perception.up_right_map)))
    if perception.up_left_map:
        actions.append(Action(f"Move_UP_LEFT: {perception.up_left_map}", "Move character 1 map up-left",
                              lambda: character.move(perception.up_left_map)))
    if perception.down_right_map:
        actions.append(Action(f"Move_DOWN_RIGHT: {perception.down_right_map}", "Move character 1 map down-right",
                              lambda: character.move(perception.down_right_map)))
    if perception.down_left_map:
        actions.append(Action(f"Move_DOWN_LEFT: {perception.down_left_map}", "Move character 1 map down-left",
                              lambda: character.move(perception.down_left_map)))
    return perception, actions


def move_menu(character: MyCharacterAPI):
    while True:
        print("Move Menu")
        perception, actions = possible_actions(character)
        print(f"Current Map: {perception.current_map}")
        print("Select Map to move to:")
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
