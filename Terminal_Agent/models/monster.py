from dataclasses import dataclass, field
from typing import List, Dict, AnyStr


@dataclass
class Drop:
    code: str
    rate: float
    min_quantity: int
    max_quantity: int

    def __str__(self):
        return f"Drop(code={self.code}, drop_rate={round(100/self.rate, 2)}%, min_quantity={self.min_quantity}, max_quantity={self.max_quantity})"

    def __repr__(self):
        return f"Drop(code={self.code}, drop_rate={round(100/self.rate, 2)}%, min_quantity={self.min_quantity}, max_quantity={self.max_quantity})"


@dataclass
class Monster:
    name: str
    code: str
    level: int
    hp: int
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    min_gold: int
    max_gold: int
    drops: List[Drop] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict) -> "Monster":
        drops = [Drop(**drop) for drop in data.get("drops", [])]
        return Monster(
            name=data.get("name", ""),
            code=data.get("code", ""),
            level=data.get("level", 0),
            hp=data.get("hp", 0),
            attack_fire=data.get("attack_fire", 0),
            attack_earth=data.get("attack_earth", 0),
            attack_water=data.get("attack_water", 0),
            attack_air=data.get("attack_air", 0),
            res_fire=data.get("res_fire", 0),
            res_earth=data.get("res_earth", 0),
            res_water=data.get("res_water", 0),
            res_air=data.get("res_air", 0),
            min_gold=data.get("min_gold", 0),
            max_gold=data.get("max_gold", 0),
            drops=drops,
        )

    def __repr__(self):
        return (
            f"Monster: name={self.name}, code={self.code}, level={self.level}\n"
            f"Stats: hp={self.hp}, attack_fire={self.attack_fire}, attack_earth={self.attack_earth}, attack_water={self.attack_water},"
            f" attack_air={self.attack_air}, res_fire={self.res_fire}, res_earth={self.res_earth},"
            f" res_water={self.res_water}, res_air={self.res_air}\n"
            f"Drops: min_gold={self.min_gold}, max_gold={self.max_gold}, items={self.drops}"
        )


class AllMonsters:
    def __init__(self, monsters: List[Dict]) -> None:
        self.monsters = [Monster.from_dict(monster) for monster in monsters]

    def filter(
        self, drop: AnyStr = None, max_level: int = None, min_level: int = None
    ) -> List[Monster]:

        filtered_drop = []
        if drop:
            for monster in self.monsters:
                if monster.drops:
                    for dr_item in monster.drops:
                        if dr_item.code == drop:
                            filtered_drop += [monster]
        else:
            filtered_drop = self.monsters

        filtered_max_level = []
        if max_level:
            for monster in filtered_drop:
                if monster.level <= max_level:
                    filtered_max_level += [monster]
        else:
            filtered_max_level = filtered_drop

        filtered_min_level = []
        if min_level:
            for monster in filtered_max_level:
                if monster.level >= min_level:
                    filtered_min_level += [monster]
        else:
            filtered_min_level = filtered_max_level

        return filtered_min_level

    def get_drops(self, drop: AnyStr = None) -> Monster:

        filtered_drops = self.filter(drop=drop)

        picked_monster = filtered_drops[0]
        for monster in filtered_drops:
            if monster.level < picked_monster.level:
                picked_monster = monster

        return picked_monster

    def get_drops_rate(self, drop: AnyStr = None) -> float:

        monster = self.get_drops(drop=drop)

        for item in monster.drops:
            if item.code == drop:
                return item.rate

    def get(self, code: AnyStr) -> Monster | None:
        for monster in self.monsters:
            if monster.code == code:
                return monster

        return None

    def check_drops(self, monster_code: AnyStr) -> List[Drop]:
        for resource in self.monsters:
            if resource.code == monster_code:
                drops = resource.drops
                # drops = [drop for drop in drops if drop.rate == 1]
                return drops
        return []
