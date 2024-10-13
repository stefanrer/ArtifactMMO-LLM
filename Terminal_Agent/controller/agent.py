from controller import AllActions
from models import Character
from interfaces import MyCharacterAPI


class Agent:
    def __init__(self, character: Character):
        self.character = MyCharacterAPI(character)
        self.actions = AllActions(self.character)

    def run(self):
        print(f"running agent: {self.character.character_data.name}")
        self.actions.start()
