from dataclasses import dataclass
from collections.abc import Callable


@dataclass
class Action:
    name: str
    description: str
    function: Callable[..., None]