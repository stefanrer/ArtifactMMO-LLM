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
class Resource:
    name: str
    code: str
    skill: str
    level: int
    drops: List[Drop] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict) -> "Resource":
        drops = [Drop(**drop) for drop in data.get("drops", [])]
        return Resource(
            name=data.get("name", ""),
            code=data.get("code", ""),
            skill=data.get("skill", ""),
            level=data.get("level", 0),
            drops=drops,
        )

    def __repr__(self):
        return (
            f"Resource: name={self.name}, code={self.code}, skill={self.skill}, skill_level={self.level}\n"
            f"drops: {self.drops}"
        )


class AllResources:
    def __init__(self, resources: List[Dict]) -> None:
        self.resources = [Resource.from_dict(resource) for resource in resources]

    def filter(
            self, drop: AnyStr = None, max_level: int = None, min_level: int = None
    ) -> List[Resource]:

        filtered_drop = []
        if drop:
            for resource in self.resources:
                if resource.drops:
                    for dr_resource in resource.drops:
                        if dr_resource.code == drop:
                            filtered_drop += [resource]
        else:
            filtered_drop = self.resources

        filtered_max_level = []
        if max_level:
            for resource in filtered_drop:
                if resource.level <= max_level:
                    filtered_max_level += [resource]
        else:
            filtered_max_level = filtered_drop

        filtered_min_level = []
        if min_level:
            for resource in filtered_max_level:
                if resource.level >= min_level:
                    filtered_min_level += [resource]
        else:
            filtered_min_level = filtered_max_level

        return filtered_min_level

    def get_drops(self, drop: AnyStr = None) -> Resource | None:

        filtered_drops = self.filter(drop=drop)

        try:
            picked_resource = filtered_drops[0]
        except IndexError:
            return None

        for resource in filtered_drops:
            for drops in resource.drops:
                if drops.code == drop and drops.rate > 1000:
                    return None
            if resource.level < picked_resource.level:
                picked_resource = resource

        return picked_resource

    def get(self, code: AnyStr) -> Resource | None:
        for monster in self.resources:
            if monster.code == code:
                return monster
        return None

    def check_drops(self, resource_code: AnyStr) -> List[Drop]:
        for resource in self.resources:
            if resource.code == resource_code:
                drops = resource.drops
                # drops = [drop for drop in drops if drop.rate == 1]
                return drops
        return []

