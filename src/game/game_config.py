from typing import List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from src.player.role import Role


class PlayerConfig(BaseModel):
    model_name: str
    role: Role


class GameConfig(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    players: List[PlayerConfig]
    max_turns: Annotated[int, Field(strict=True, gt=0)]
