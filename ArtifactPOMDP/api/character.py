from .map import MapAPI
from ArtifactPOMDP.models.character import Character
from ArtifactPOMDP.models.map import Map

from typing import AnyStr


class MyCharacterAPI(MapAPI):
    def __init__(self, character: Character) -> None:
        super().__init__()
        self.character_data = character

    def move(self, target: Map) -> None:
        if (self.character_data.x, self.character_data.y) == (target.x, target.y):
            return

        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": target.x, "y": target.y})

        self._update_character()

    def move_up(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x, "y": self.character_data.y - 1})

        self._update_character()

    def move_down(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x, "y": self.character_data.y + 1})

        self._update_character()

    def move_left(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x - 1, "y": self.character_data.y})

        self._update_character()

    def move_right(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x + 1, "y": self.character_data.y})

        self._update_character()

    def move_up_right(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x + 1, "y": self.character_data.y - 1})

        self._update_character()

    def move_up_left(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x - 1, "y": self.character_data.y - 1})

        self._update_character()

    def move_down_right(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x + 1, "y": self.character_data.y + 1})

        self._update_character()

    def move_down_left(self) -> None:
        method = f"/my/{self.character_data.name}/action/move"
        self.post(method=method, body={"x": self.character_data.x - 1, "y": self.character_data.y + 1})

        self._update_character()

    def fight(self):
        method = f"/my/{self.character_data.name}/action/fight"
        response_code, response_data = self.post(method=method)
        self._update_character()
        if response_code == 200:
            if response_data["data"]["fight"]["result"] == "win":
                print("Fight Won, ")
                print(f"Drops: {response_data['data']['fight']['drops']}")
            else:
                print("Fight Lost")
        else:
            print("Unknown Error")

    def gather(self):
        method = f"/my/{self.character_data.name}/action/gathering"
        response_code, response_data = self.post(method=method)
        self._update_character()
        if response_code == 200:
            print(f"Gathered: {response_data['data']['details']['items']}")
        elif response_code == 493:
            print("Not skill level required.")
        else:
            print("Unknown Error")


    def craft(self, code: AnyStr):
        method = f"/my/{self.character_data.name}/action/crafting"

        response_code, response_data = self.post(method=method, body={"code": code})

        self._update_character()

        return response_code == 200

    def unequip(self, slot: AnyStr) -> bool:
        method = f"/my/{self.character_data.name}/action/unequip"

        response_code, response_data = self.post(method=method, body={"slot": slot})

        self._update_character()

        return response_code == 200

    def equip(self, code: AnyStr, slot: AnyStr, quantity: int = 1) -> bool:
        method = f"/my/{self.character_data.name}/action/equip"

        response_code, response_data = self.post(
            method=method, body={"slot": slot, "code": code, "quantity": quantity}
        )

        self._update_character()

        return response_code == 200

    def _update_character(self) -> None:
        method = f"/characters/{self.character_data.name}"
        code, response = self.get(method=method)

        self.character_data = Character.from_dict(response["data"])
