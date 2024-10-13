from dataclasses import dataclass
from typing import List, Dict, Optional, AnyStr


@dataclass
class Content:
    type: str
    code: str


@dataclass
class Map:
    name: str
    skin: str
    x: int
    y: int
    content: Optional[Content] = None

    @staticmethod
    def from_dict(data: Dict) -> "Map":
        content_data = data.get("content")
        content = None
        if content_data:
            content = Content(
                type=content_data.get("type", ""), code=content_data.get("code", "")
            )
        return Map(
            name=data.get("name", ""),
            skin=data.get("skin", ""),
            x=data.get("x", 0),
            y=data.get("y", 0),
            content=content,
        )

    def __str__(self):
        return f"{self.name}({self.x}, {self.y}): {self.content}"


class AllMaps:
    def __init__(self, maps: List[Dict]) -> None:
        self.maps = [Map.from_dict(map_tile) for map_tile in maps]

    def filter(self, content_code: AnyStr = None, content_type: AnyStr = None) -> List[Map]:

        filtered_code = []

        if content_code:
            for map in self.maps:
                if map.content:
                    if map.content.code == content_code:
                        filtered_code += [map]
        else:
            filtered_code = self.maps

        filtered_type = []

        if content_type:
            for map in filtered_code:
                if map.content:
                    if map.content.type == content_type:
                        filtered_type += [map]
        else:
            filtered_type = filtered_code

        return filtered_type

    def get_map_by_coordinates(self, x: int, y: int) -> Optional[Map]:
        for map_tile in self.maps:
            if map_tile.x == x and map_tile.y == y:
                return map_tile
        return None

    def get_map_by_name(self, name: str) -> Optional[Map]:
        for map in self.maps:
            if map.name == name:
                return map
        return None

    def get_map_by_skin(self, skin: str) -> Optional[Map]:
        for map in self.maps:
            if map.skin == skin:
                return map
        return None

    def get_3x3_matrix(self, center_x: int, center_y: int) -> List[List[Optional[Map]]]:
        matrix = []
        for dy in range(-1, 2):
            row = []
            for dx in range(-1, 2):
                row.append(self.get_map_by_coordinates(center_x + dx, center_y + dy))
            matrix.append(row)
        return matrix

