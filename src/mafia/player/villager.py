from mafia.model.model import Model
from mafia.player.base_player import BasePlayer


class Villager(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
