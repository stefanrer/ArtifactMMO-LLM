from dataclasses import dataclass, field
from math import floor, ceil
from typing import List, Dict, Optional, AnyStr

from models import Item, AllItems
from models import Monster


@dataclass
class InventoryItem:
    slot: int
    code: str
    quantity: int


@dataclass
class Character:
    name: str
    skin: str
    level: int
    xp: int
    max_xp: int
    achievements_points: int
    gold: int
    speed: int
    mining_level: int
    mining_xp: int
    mining_max_xp: int
    woodcutting_level: int
    woodcutting_xp: int
    woodcutting_max_xp: int
    fishing_level: int
    fishing_xp: int
    fishing_max_xp: int
    weaponcrafting_level: int
    weaponcrafting_xp: int
    weaponcrafting_max_xp: int
    gearcrafting_level: int
    gearcrafting_xp: int
    gearcrafting_max_xp: int
    jewelrycrafting_level: int
    jewelrycrafting_xp: int
    jewelrycrafting_max_xp: int
    cooking_level: int
    cooking_xp: int
    cooking_max_xp: int
    hp: int
    haste: int
    critical_strike: int
    stamina: int
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    dmg_fire: int
    dmg_earth: int
    dmg_water: int
    dmg_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    x: int
    y: int
    cooldown: int
    cooldown_expiration: str
    weapon_slot: str
    shield_slot: str
    helmet_slot: str
    body_armor_slot: str
    leg_armor_slot: str
    boots_slot: str
    ring1_slot: str
    ring2_slot: str
    amulet_slot: str
    artifact1_slot: str
    artifact2_slot: str
    artifact3_slot: str
    consumable1_slot: str
    consumable1_slot_quantity: int
    consumable2_slot: str
    consumable2_slot_quantity: int
    task: str
    task_type: str
    task_progress: int
    task_total: int
    inventory_max_items: int
    account: Optional[str] = None
    inventory: List[InventoryItem] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict) -> "Character":
        inventory_items = [InventoryItem(**item) for item in data.get("inventory", [])]

        character_data = {
            key: value
            for key, value in data.items()
            if key != "inventory" and key.find("inventory_slot") == -1
        }

        character = Character(**character_data)
        character.inventory = inventory_items

        return character

    def get_slot(self, slot: AnyStr) -> AnyStr | None:
        try:
            return eval(f"self.{slot}_slot")
        except AttributeError:
            return None

    def get_slot_item(self, slot: AnyStr, items: AllItems) -> Item | None:
        try:
            item_code = eval(f"self.{slot}_slot")
            item = items.get_one(item_code)
            return item
        except AttributeError:
            if slot == "ring":
                try:
                    item_code_1 = eval(f"self.{slot}1_slot")
                    item_1 = items.get_one(item_code_1)
                    item_code_2 = eval(f"self.{slot}2_slot")
                    item_2 = items.get_one(item_code_2)
                    return item_1 if item_1.level < item_2.level else item_2
                except AttributeError:
                    if item_1:
                        return item_1
                    else:
                        return None
            elif slot == "artifact":
                try:
                    item_code_1 = eval(f"self.{slot}1_slot")
                    item_1 = items.get_one(item_code_1)
                    item_code_2 = eval(f"self.{slot}2_slot")
                    item_2 = items.get_one(item_code_2)
                    item_code_3 = eval(f"self.{slot}3_slot")
                    item_3 = items.get_one(item_code_3)
                    if item_1.level <= item_2.level and item_1.level <= item_3.level:
                        return item_1
                    if item_2.level <= item_3.level and item_2.level <= item_1.level:
                        return item_2
                    if item_3.level <= item_2.level and item_3.level <= item_1.level:
                        return item_1
                    return item_1
                except AttributeError:
                    if item_1:
                        return item_1
                    else:
                        return None

    def get_resource_quantity(self, code: AnyStr):
        for item in self.inventory:
            if item.code == code:
                return item.quantity
        return 0

    def get_skill_level(self, skill: AnyStr):
        try:
            skill_level = eval(f"self.{skill}_level")
            return skill_level
        except AttributeError:
            return 0

    def can_beat(self, monster: Monster) -> bool:
        players_hp = self.hp
        mobs_hp = monster.hp

        for i in range(1, 101):
            if i % 2 == 1:
                # player
                player_attack = floor(
                    self.attack_air
                    * (1 + self.dmg_air / 100)
                    * (1 - monster.res_air / 100)
                )
                mobs_hp -= player_attack
                if mobs_hp <= 0:
                    return True

                player_attack = floor(
                    self.attack_earth
                    * (1 + self.dmg_earth / 100)
                    * (1 - monster.res_earth / 100)
                )
                mobs_hp -= player_attack
                if mobs_hp <= 0:
                    return True

                player_attack = floor(
                    self.attack_fire
                    * (1 + self.dmg_fire / 100)
                    * (1 - monster.res_fire / 100)
                )
                mobs_hp -= player_attack
                if mobs_hp <= 0:
                    return True

                player_attack = floor(
                    self.attack_water
                    * (1 + self.dmg_water / 100)
                    * (1 - monster.res_water / 100)
                )
                mobs_hp -= player_attack
                if mobs_hp <= 0:
                    return True
            else:
                # mob
                mob_attack = ceil(monster.attack_air * (1 - self.res_air / 100))
                players_hp -= mob_attack
                if players_hp <= 0:
                    return False

                mob_attack = ceil(monster.attack_earth * (1 - self.res_earth / 100))
                players_hp -= mob_attack
                if players_hp <= 0:
                    return False

                mob_attack = ceil(monster.attack_fire * (1 - self.res_fire / 100))
                players_hp -= mob_attack
                if players_hp <= 0:
                    return False

                mob_attack = ceil(monster.attack_water * (1 - self.res_water / 100))
                players_hp -= mob_attack
                if players_hp <= 0:
                    return False

        return False