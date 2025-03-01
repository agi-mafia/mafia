from enum import Enum, auto

from pydantic import BaseModel, ConfigDict

from src.player.base_player import BasePlayer
from src.player.role import Role


class Survival(Enum):
    REMAINING = auto()
    ELIMINATED = auto()


class InGamePlayer(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    player: BasePlayer
    role: Role
    survival: Survival
