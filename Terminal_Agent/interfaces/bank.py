from typing import AnyStr

from interfaces import BaseAPI
from models import (
    Item,
    AllBankItems,
    AllGreatExchange
)


class BankAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()

    def get_gold(self):
        code, response = self.get(method="/my/bank")
        return response["data"]["gold"]

    def get_bank_slots(self):
        total_slots = 0
        for page in range(1, 5):
            _, response = self.get(
                method="/my/bank/items",
                params={"page": page, "size": 100}
            )
            if "data" in response and isinstance(response["data"], list):
                total_slots += len(response["data"])
            if len(response["data"]) < 100:
                break
        return total_slots

    def get_bank_max_slots(self):
        _, response = self.get(method="/my/bank")
        return response["data"]["slots"]

    @property
    def needs_expansion(self):
        bank_slots = self.get_bank_slots()
        max_slots = self.get_bank_max_slots()

        return bank_slots / max_slots >= 2 / 3

    def get_ge_sell_price(self, item: Item):
        code, response = self.get(method=f"/ge/{item.code}")
        return response["data"]["sell_price"]

    def get_ge_sell_quantity(self, item: Item):
        code, response = self.get(method=f"/ge/{item.code}")
        if code == 200:
            return response["data"]["max_quantity"]
        else:
            return 0

    def get_ge_buy_price(self, item: Item):
        code, response = self.get(method=f"/ge/{item.code}")
        return response["data"]["buy_price"]

    def get_ge_items(self):
        all_data = self.get_all(method="/ge/")
        return AllGreatExchange(items=all_data)

    def get_bank_expansion_price(self):
        _, response = self.get(method="/my/bank")
        return response["data"]["next_expansion_cost"]

    def get_quantity(self, item_code: AnyStr) -> int:
        params = {"item_code": item_code}

        code, response = self.get(method="/my/bank/items", params=params)

        if not response["data"]:
            return 0

        return max(response["data"][0]["quantity"], 0)

    def get_all_items(self) -> AllBankItems:
        all_data = self.get_all(method="/my/bank/items")
        return AllBankItems(items=all_data)

    def has_item(self, item: Item) -> bool:
        code, response = self.get(method="/my/bank/items", params={"item_code": item.code})
        if not response["data"]:
            return False
        else:
            return True

