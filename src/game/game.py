from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.player_status import PlayerStatus, Survival


class Game:

    def __init__(self, config: GameConfig):

        self._config = config

        self._player2status = {
            player: PlayerStatus(
                role=config.players[player],
                survival=Survival.remaining,
            )
            for player in config.players
        }

    @property
    def _role2players(self):
        role2players = defaultdict(list)
        for player, status in self._player2status.items():
            role2players[status.role].append(player)
        return role2players
