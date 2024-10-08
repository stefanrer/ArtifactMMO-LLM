from ArtifactPOMDP.api.map import MapAPI
from ArtifactPOMDP.api.item import ItemAPI
from ArtifactPOMDP.api.monster import MonsterAPI
from ArtifactPOMDP.api.characters import MyCharactersAPI
from ArtifactPOMDP.api.character import MyCharacterAPI
from ArtifactPOMDP.api.resource import ResourceAPI


map_api = MapAPI()
MAPS = map_api.get_all_maps()

item_api = ItemAPI()
ITEMS = item_api.get_all_items()

monster_api = MonsterAPI()
MONSTERS = monster_api.get_all_monsters()

resource_api = ResourceAPI()
RESOURCES = resource_api.get_all_resources()

characters_api = MyCharactersAPI()

CHARACTERS = []
for character in characters_api.get_all_characters():
    CHARACTERS.append(MyCharacterAPI(character))