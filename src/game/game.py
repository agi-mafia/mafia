from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.in_game_player import InGamePlayer, Survival
from src.game.outcome import GameStatus
from src.player.role import Role, role_mapping


class Game:

    def __init__(self, config: GameConfig):
        self._config = config
        self._id2player = {
            index: InGamePlayer(
                player=role_mapping[player_config.role](
                    index,
                    player_config.model_name,
                ),
                role=player_config.role,
                survival=Survival.REMAINING,
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
            if self._id2player[i].survival == Survival.REMAINING
        ]

    @property
    def _remaining_mafia_ids(self):
        return [
            i
            for i in self._id2player
            if self._id2player[i].role == Role.MAFIA
            and self._id2player[i].survival == Survival.REMAINING
        ]

    @property
    def _remaining_non_mafia_ids(self):
        return [
            i
            for i in self._id2player
            if self._id2player[i].role != Role.MAFIA
            and self._id2player[i].survival == Survival.REMAINING
        ]

    def has_ended(self) -> GameStatus:

        num_mafia_remaining = len(self._remaining_mafia_ids)
        num_non_mafia_remaining = len(self._remaining_non_mafia_ids)

        if num_mafia_remaining > num_non_mafia_remaining:
            return GameStatus.MAFIA_WIN
        elif num_mafia_remaining == 0:
            return GameStatus.TOWN_WIN
        else:
            return GameStatus.IN_PROGRESS

    def start(self):

        # Introduce the mafia team to each other
        for mafia_id in self._remaining_mafia_ids:
            other_mafias = [i for i in self._remaining_mafia_ids if i != mafia_id]
            self._id2player[mafia_id].player.see_teammates(other_mafias)
