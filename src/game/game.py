from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.in_game_player import InGamePlayer, Survival
from src.player.role import Role, role_mapping


class Game:

    def __init__(self, config: GameConfig):
        self._config = config
        self._id2player = {
            index: InGamePlayer(
                player=role_mapping[player_config.role](
                    index,
                    player_config.modelname,
                ),
                role=player_config.role,
                survival=Survival.remaining,
            )
            for index, player_config in enumerate(config.players)
        }

    @property
    def _role2ids(self):
        role2ids = defaultdict(list)
        for index, status in self._id2player.items():
            role2ids[status.role].append(index)
        return role2ids

    @property
    def _remaining_ids(self):
        return [
            i
            for i in self._id2player
            if self._id2player[i].survival == Survival.remaining
        ]

    @property
    def _remaining_mafia_ids(self):
        return [
            i
            for i in self._id2player
            if self._id2player[i].role == Role.MAFIA
            and self._id2player[i].survival == Survival.remaining
        ]

    def start(self):

        # Make the mafia team know each other
        for mafia_id in self._remaining_mafia_ids:
            other_mafias = [i for i in self._remaining_mafia_ids if i != mafia_id]
            self._id2player[mafia_id].player.see_teammates(other_mafias)

    def has_ended(self):
        num_mafia_remaining = len(self._remaining_mafia_ids)
        num_total_players = len(self._remaining_ids)
