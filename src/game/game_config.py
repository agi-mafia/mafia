from pydantic import BaseModel, ConfigDict
from typing import Dict
from src.player.role import Role


class GameConfig(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    players: Dict[str, Role]
