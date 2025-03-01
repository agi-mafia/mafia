from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.player_status import InGamePlayer, Survival
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
    def _remaining_mafia_ids(self):
        return [
            i
            for i in self._id2player
            if self._id2player[i].role == Role.mafia
            and self._id2player[i].survival == Survival.remaining
        ]

    def start(self):

        # Make the mafia team know each other
        mafia_ids = self._role2ids[Role.mafia]
        for mafia_id in mafia_ids:
            other_mafias = [i for i in mafia_ids if i != mafia_id]
            self._id2player[mafia_id].player.see_teammates(other_mafias)

    def ended(self):
        num_mafia = len(self._role2ids[Role.mafia])
