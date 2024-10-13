from interfaces import MapAPI
from models import Map
from models import Character

from typing import AnyStr


class MyCharacterAPI(MapAPI):
    def __init__(self, character: Character) -> None:
        super().__init__()
        self.character_data = character

    def move(self, target: Map) -> None:
        """
        Moves a character on the map using the provided map's X and Y position.
        :param Map target: Target Map.
        """
        print(f"The character is moving to {target}")
        method = f"/my/{self.character_data.name}/action/move"
        response_code, _ = self.post(method=method, body={"x": target.x, "y": target.y})
        if response_code == 200:  # Success
            print(f"The character has moved successfully: {target}")
        elif response_code == 404:
            print("Map not found")
        elif response_code == 490:
            print("Character already at destination")
        else:
            print("Unknown Error")
        self._update_character()

    def fight(self) -> None:
        """
        Start a fight against a monster on the character's map.
        """
        method = f"/my/{self.character_data.name}/action/fight"
        response_code, response_data = self.post(method=method)
        if response_code == 200:  # Success
            if response_data["data"]["fight"]["result"] == "win":
                print("Fight Won")
                print(f"Drops: {response_data['data']['fight']['drops']}")
            else:
                print("Fight Lost")
        elif response_code == 497:
            print("Character inventory is full")
        elif response_code == 598:
            print("Monster not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def gather(self) -> None:
        """
        Harvest a resource on the character's map.
        """
        method = f"/my/{self.character_data.name}/action/gathering"
        response_code, response_data = self.post(method=method)
        if response_code == 200:  # Success
            print(f"Gathered: {response_data['data']['details']['items']}")
        elif response_code == 493:
            print("Not skill level required")
        elif response_code == 497:
            print("Character inventory is full")
        elif response_code == 598:
            print("Resource not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def craft(self, code: AnyStr) -> None:
        """
        Crafting an item. The character must be on a map with a workshop.
        :param str code: Craft code. Match pattern: ^[a-zA-Z0-9_-]+$
        """
        method = f"/my/{self.character_data.name}/action/crafting"
        response_code, _ = self.post(method=method, body={"code": code})
        if response_code == 200:  # Success
            print("The item was successfully crafted.")
        elif response_code == 404:
            print("Craft not found")
        elif response_code == 478:
            print("Missing item or insufficient quantity")
        elif response_code == 493:
            print("Not skill level required")
        elif response_code == 497:
            print("Character inventory is full")
        elif response_code == 598:
            print("Workshop not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def unequip_item(self, slot: AnyStr, quantity: int = 1) -> None:
        """
        Unequip an item on your character.
        :param int quantity: Item quantity. Applicable to consumables only. >= 1 <= 100 Default: 1
        :param str slot: Item slot. Allowed values: weapon, shield, helmet, body_armor, leg_armor, boots, ring1,
         ring2, amulet, artifact1, artifact2, artifact3, consumable1, consumable2
        """
        if self.character_data.get_slot(slot):
            method = f"/my/{self.character_data.name}/action/unequip"
            response_code, _ = self.post(method=method, body={"slot": slot, "quantity": quantity})
            if response_code == 200:  # Success
                print("The item has been successfully unequipped and added to inventory")
            elif response_code == 404:
                print("Item not found")
            elif response_code == 478:
                print("Missing item or insufficient quantity")
            elif response_code == 491:
                print("Slot is empty")
            elif response_code == 497:
                print("Character inventory is full")
            else:
                print("Unknown Error")
        else:
            print("Slot not found")
        self._update_character()

    def equip_item(self, code: AnyStr, slot: AnyStr, quantity: int = 1) -> None:
        """
        Equip an item on your character.
        :param str code: Item code. Match pattern: ^[a-zA-Z0-9_-]+$
        :param str slot: Item slot. Allowed values: weapon, shield, helmet, body_armor, leg_armor, boots, ring1,
         ring2, amulet, artifact1, artifact2, artifact3, consumable1, consumable2
        :param int quantity: Item quantity. Applicable to consumables only. >= 1 <= 100
        """
        if self.character_data.get_slot(slot):
            method = f"/my/{self.character_data.name}/action/equip"
            response_code, _ = self.post(
                method=method, body={"slot": slot, "code": code, "quantity": quantity}
            )
            if response_code == 200:  # Success
                print("The item has been successfully equipped on your character")
            elif response_code == 404:
                print("Item not found")
            elif response_code == 478:
                print("Missing item or insufficient quantity")
            elif response_code == 484:
                print("Character can't equip more than 100 consumables in the same slot")
            elif response_code == 485:
                print("This item is already equipped")
            elif response_code == 491:
                print("Slot is not empty")
            elif response_code == 496:
                print("Character level is insufficient")
            elif response_code == 497:
                print("Character inventory is full")
            else:
                print("Unknown Error")
        else:
            print("Slot not found")
        self._update_character()

    def deposit_bank(self, code: AnyStr, quantity: int = 1) -> None:
        """
        Deposit an item in a bank on the character's map.
        :param str code: Item code. Match pattern: ^[a-zA-Z0-9_-]+$
        :param int quantity: Item quantity. >= 1
        """
        method = f"/my/{self.character_data.name}/action/bank/deposit"
        response_code, _ = self.post(
            method=method, body={"code": code, "quantity": quantity}
        )
        if response_code == 200:  # Success
            print("Item successfully deposited in your bank")
        elif response_code == 404:
            print("Item not found")
        elif response_code == 462:
            print("Your bank if full")
        elif response_code == 478:
            print("Missing item or insufficient quantity")
        elif response_code == 598:
            print("Bank not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def withdraw_bank(self, code: AnyStr, quantity: int = 1) -> None:
        """
        Take an item from your bank and put it in the character's inventory.
        :param str code: Item code. Match pattern: ^[a-zA-Z0-9_-]+$
        :param int quantity: Item quantity. >= 1
        """
        method = f"/my/{self.character_data.name}/action/bank/withdraw"
        response_code, _ = self.post(
            method=method, body={"code": code, "quantity": quantity}
        )
        if response_code == 200:  # Success
            print("Item successfully withdraw from your bank")
        elif response_code == 404:
            print("Item not found")
        elif response_code == 478:
            print("Missing item or insufficient quantity")
        elif response_code == 497:
            print("Character inventory is full")
        elif response_code == 598:
            print("Bank not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def deposit_bank_gold(self, quantity: int = 1) -> None:
        """
        Deposit golds in a bank on the character's map.
        :param int quantity: Quantity of gold. >= 1
        """
        method = f"/my/{self.character_data.name}/action/bank/deposit/gold"
        response_code, _ = self.post(
            method=method, body={"quantity": quantity}
        )
        if response_code == 200:  # Success
            print("Golds successfully deposited in your bank")
        elif response_code == 492:
            print("Insufficient golds on your character")
        elif response_code == 598:
            print("Bank not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def withdraw_bank_gold(self, quantity: int = 1) -> None:
        """
        Withdraw gold from your bank.
        :param int quantity: Quantity of gold. >= 1
        """
        method = f"/my/{self.character_data.name}/action/bank/withdraw/gold"
        response_code, _ = self.post(
            method=method, body={"quantity": quantity}
        )
        if response_code == 200:  # Success
            print("Golds successfully withdraw from your bank")
        elif response_code == 460:
            print("Insufficient golds in your bank")
        elif response_code == 598:
            print("Bank not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def buy_bank_expansion(self) -> None:
        """
        Buy a 20 slots bank expansion.
        """
        method = f"/my/{self.character_data.name}/action/bank/buy_expansion"
        response_code, _ = self.post(method=method)
        if response_code == 200:  # Success
            print("Bank expansion successfully bought")
        elif response_code == 492:
            print("Insufficient golds on your character")
        elif response_code == 598:
            print("Bank not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def recycle(self, code: AnyStr, quantity: int = 1) -> None:
        """
        Recycling an item. The character must be on a map with a workshop (only for equipments and weapons)
        :param str code: Item code. Match pattern: ^[a-zA-Z0-9_-]+$
        :param int quantity: Quantity of items to recycle. >= 1
        """
        method = f"/my/{self.character_data.name}/action/recycling"
        response_code, response_data = self.post(
            method=method, body={"code": code, "quantity": quantity}
        )
        if response_code == 200:  # Success
            print("The items were successfully recycled")
            print(f"Objects received: {response_data['data']['details']['items']}")
        elif response_code == 404:
            print("Item not found")
        elif response_code == 473:
            print("This item cannot be recycled")
        elif response_code == 478:
            print("Missing item or insufficient quantity")
        elif response_code == 493:
            print("Not skill level required")
        elif response_code == 497:
            print("Character inventory is full")
        elif response_code == 598:
            print("Workshop not found on this map")
        else:
            print("Unknown Error")
        self._update_character()

    def delete_item(self, code: AnyStr, quantity: int = 1) -> None:
        """
        Delete an item from your character's inventory.
        :param str code: Item code. Match pattern: ^[a-zA-Z0-9_-]+$
        :param int quantity: Item quantity. >= 1
        """
        method = f"/my/{self.character_data.name}/action/recycling"
        response_code, response_data = self.post(
            method=method, body={"code": code, "quantity": quantity}
        )
        if response_code == 200:  # Success
            print("Item successfully deleted from your character")
        elif response_code == 478:
            print("Missing item or insufficient quantity")
        else:
            print("Unknown Error")
        self._update_character()

    def _update_character(self) -> None:
        """
        Update character data.
        """
        method = f"/characters/{self.character_data.name}"
        code, response = self.get(method=method)

        self.character_data = Character.from_dict(response["data"])
