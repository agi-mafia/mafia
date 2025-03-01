from enum import Enum, auto

from pydantic import BaseModel, ConfigDict

from src.player.base_player import BasePlayer
from src.player.role import Role


class Survival(Enum):
    remaining = auto()
    eliminated = auto()


class InGamePlayer(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    player: BasePlayer
    role: Role
    survival: Survival
