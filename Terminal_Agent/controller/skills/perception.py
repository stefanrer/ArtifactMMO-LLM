from dataclasses import dataclass
from typing import Optional
from models import Map
from interfaces import maps


@dataclass()
class Perception:
    current_map: Optional[Map] = None
    right_map: Optional[Map] = None
    left_map: Optional[Map] = None
    up_map: Optional[Map] = None
    down_map: Optional[Map] = None
    up_right_map: Optional[Map] = None
    up_left_map: Optional[Map] = None
    down_right_map: Optional[Map] = None
    down_left_map: Optional[Map] = None


def get_perception(character_x, character_y):
    perception = Perception()
    matrix = maps.get_3x3_matrix(character_x, character_y)
    perception.current_map = matrix[1][1]
    perception.up_map = matrix[0][1]
    perception.down_map = matrix[2][1]
    perception.left_map = matrix[1][0]
    perception.right_map = matrix[1][2]
    perception.up_right_map = matrix[0][2]
    perception.up_left_map = matrix[0][0]
    perception.down_right_map = matrix[2][2]
    perception.down_left_map = matrix[2][0]
    return perception
