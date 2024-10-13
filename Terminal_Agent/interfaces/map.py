from interfaces import BaseAPI
from typing import Optional
from models import AllMaps, Map


class MapAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()

    def get_all_maps(self) -> AllMaps:
        all_data = self.get_all(method="/maps")
        return AllMaps(maps=all_data)

    def get_map(self, x: int, y: int) -> Optional[Map]:
        response_code, response_data = self.get(method=f"/maps/{x}/{y}")
        if response_code == 200:
            return Map.from_dict(response_data.get("data"))
        else:
            return None

    def get_event_maps(self) -> AllMaps:
        try:
            all_data = self.get_all(method="/events")
            event_maps = [event["map"] for event in all_data]
            return AllMaps(maps=event_maps)
        except KeyError:
            return AllMaps(maps=[])

    @property
    def has_events(self) -> bool:
        events = self.get_event_maps()
        has_monster_event = False
        for event in events.maps:
            if event.content.type == "monster":
                has_monster_event = True
        return has_monster_event
