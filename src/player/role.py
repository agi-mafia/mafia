from enum import Enum, auto
from pydantic import BaseModel


class Role(Enum):
    villager = auto()
    mafia = auto()
    detective = auto()
    jailor = auto()
    hunter = auto()
