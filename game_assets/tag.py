from dataclasses import dataclass
from .game_constants import TagType


@dataclass
class Tag:
    """
    similar to the Tag Framework in BG3 (https://bg3.wiki/wiki/Tags) Tags identify things into specific categories, but
    with the flexibility of a string identifier, while the categories is a closed set, the strings identifying particular
    aspects of things need not be so closed off...
    """
    name: str
    category: TagType
    description: str
    dc: int | None
    hint: str | None
