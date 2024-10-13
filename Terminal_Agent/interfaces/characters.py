from interfaces import BaseAPI
from models import Character

from typing import AnyStr, List
import random


class MyCharactersAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()

    def get_all_characters(self) -> List[Character]:
        code, response = self.get(method="/my/characters")

        all_characters = []
        for character in response["data"]:
            all_characters.append(Character.from_dict(character))
        return all_characters

    def delete(self, character_name: str) -> None:
        response_code, response_data = self.post(method="/characters/delete", body={"name": character_name})
        print(response_code, response_data)

    def create(self, character_name: str) -> None:
        skin = random.choice(["men1", "men2", "men3", "women1", "women2", "women3"])
        response_code, response_data = self.post(method="/characters/create", body={"name": character_name, "skin": skin})
        print(response_code, response_data)

    def reset(self) -> List[Character]:
        # Remove all characters from token
        all_characters = self.get_all()
        for character in all_characters:
            self.delete(character.name)
        # Create 5 characters on token
        for i in range(1, 6):
            self.create(f"character_{i}")
            print(f"character_{i}")
        return self.get_all_characters()
