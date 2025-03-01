from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.in_game_player import InGamePlayer, Survival
from src.game.outcome import GameStatus
from src.player.role import Role, role_mapping


class Game:

    def __init__(self, config: GameConfig):
        self._config = config
        self._players = {
            i: InGamePlayer(
                player=role_mapping[player_config.role](
                    i,
                    player_config.model_name,
                ),
                role=player_config.role,
                survival=Survival.REMAINING,
            )
            for i, player_config in enumerate(config.players)
        }
        self._n_turns = 0

    @property
    def _role2ids(self):
        role2ids = defaultdict(list)
        for index, status in self._players.items():
            role2ids[status.role].append(index)
        return role2ids

    @property
    def _remaining_player_ids(self):
        return [
            i for i in self._players if self._players[i].survival == Survival.REMAINING
        ]

    @property
    def _remaining_mafia_ids(self):
        return [
            i
            for i in self._players
            if self._players[i].role == Role.MAFIA
            and self._players[i].survival == Survival.REMAINING
        ]

    @property
    def _remaining_town_ids(self):
        return [
            i
            for i in self._players
            if self._players[i].role != Role.MAFIA
            and self._players[i].survival == Survival.REMAINING
        ]

    @property
    def status(self) -> GameStatus:
        if self._n_turns > self._config.max_turns:
            return GameStatus.DRAW
        n_mafia_remaining = len(self._remaining_mafia_ids)
        n_town_remaining = len(self._remaining_town_ids)
        if n_mafia_remaining > n_town_remaining:
            return GameStatus.MAFIA_WIN
        elif n_mafia_remaining == 0:
            return GameStatus.TOWN_WIN
        else:
            return GameStatus.IN_PROGRESS

    def start(self):

        # Introduce the mafia team to each other
        for mafia_id in self._remaining_mafia_ids:
            other_mafias = [i for i in self._remaining_mafia_ids if i != mafia_id]
            self._players[mafia_id].player.see_teammates(other_mafias)

        while self.status == GameStatus.IN_PROGRESS:
            self.night()
            if self.status == GameStatus.IN_PROGRESS:
                self.day()
            self._n_turns += 1

    def night(self):

        # Let mafia choose victim
        for mafia_id in self._remaining_mafia_ids:
            other_mafia_ids = [i for i in self._remaining_mafia_ids if i != mafia_id]

            proposed_victim_id, proposed_reason = self._players[
                mafia_id
            ].player.propose_victim(self._remaining_player_ids)

            for other_mafia_id in other_mafia_ids:
                self._players[other_mafia_id].player.receive_victim_proposal(
                    self._remaining_player_ids,
                    mafia_id,
                    proposed_victim_id,
                    proposed_reason,
                )

    def day(self):
        pass
