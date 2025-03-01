from pydantic import BaseModel


class GameConfig(BaseModel, frozen=True):
    
