from typing import List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from mafia.player.role import Role


class PlayerConfig(BaseModel):
    model_name: str
    role: Role


class GameConfig(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    players: List[PlayerConfig]
    max_rounds: Annotated[int, Field(strict=True, gt=0)]
