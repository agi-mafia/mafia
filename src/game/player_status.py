from enum import Enum, auto

from pydantic import BaseModel

from src.player.role import Role


class Survival(Enum):
    remaining = auto()
    eliminated = auto()


class PlayerStatus(BaseModel):
    modelname: str
    role: Role
    survival: Survival
