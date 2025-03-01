from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.player_status import PlayerStatus, Survival
from src.player.role import Role


class Game:

    def __init__(self, config: GameConfig):
        self._config = config
        self._id2status = {
            index: PlayerStatus(
                modelname=player.modelname,
                role=player.role,
                survival=Survival.remaining,
            )
            for index, player in enumerate(config.players)
        }

    @property
    def _role2ids(self):
        role2ids = defaultdict(list)
        for index, status in self._id2status.items():
            role2ids[status.role].append(index)
        return role2ids

    def start(self):
        for mafia_id in self._role2ids[Role.mafia]:
            pass
