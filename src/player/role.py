from enum import auto, Enum

from pydantic import BaseModel


class Role(Enum):
    villager = auto()
    mafia = auto()
    detective = auto()
    jailor = auto()
    hunter = auto()
