from enum import Enum, auto

from pydantic import BaseModel

from src.player.role import Role


class Survival(Enum):
    remaining = auto()
    eliminated = auto()


class PlayerStatus(BaseModel):
    role: Role
    survival: Survival
