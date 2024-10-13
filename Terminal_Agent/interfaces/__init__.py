from .base import BaseAPI
from .item import ItemAPI
from .monster import MonsterAPI
from .resource import ResourceAPI
from .map import MapAPI
from .bank import BankAPI
from .characters import MyCharactersAPI
from .character import MyCharacterAPI

map_api = MapAPI()
maps = map_api.get_all_maps()

item_api = ItemAPI()
items = item_api.get_all_items()

monster_api = MonsterAPI()
monsters = monster_api.get_all_monsters()

resource_api = ResourceAPI()
resources = resource_api.get_all_resources()

bank = BankAPI()


