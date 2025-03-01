from pydantic import BaseModel, ConfigDict
from typing import Dict
from src.player.role import Role
from src.model.model import Model


class GameConfig(BaseModel):
    model_config = ConfigDict(strict=True)
    contestants: Dict[Model, Role]
