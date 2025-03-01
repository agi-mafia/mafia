from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.in_game_player import InGamePlayer, Survival
from src.game.outcome import GameStatus
from src.player.role import Role
from src.player.role_mapping import role_mapping
from src.util.general import most_frequent_random


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
        self._n_rounds = 0
        self._victim_id = None

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
    def _remaining_detective_ids(self):
        return [
            i
            for i in self._players
            if self._players[i].role == Role.DETECTIVE
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
        if self._n_rounds > self._config.max_rounds:
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
            self._night()
            if self.status == GameStatus.IN_PROGRESS:
                self._day()
            self._n_rounds += 1

    def _mafia_round(self):

        # Each mafia proposes a victim
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

        # A final victim is chosen via mafia vote
        victim_votes = {
            i: self._players[i].player.choose_victim(self._remaining_player_ids)
            for i in self._remaining_mafia_ids
        }
        for mafia_id in self._remaining_mafia_ids:
            other_mafia_ids = [i for i in self._remaining_mafia_ids if i != mafia_id]
            other_mafia_votes = {
                other_mafia_id: victim_votes[other_mafia_id]
                for other_mafia_id in other_mafia_ids
            }
            self._players[mafia_id].listen_vote_night(other_mafia_votes)

        self._victim_id = most_frequent_random(victim_votes.values())

    def _detective_round(self):
        if len(self._remaining_detective_ids) <= 0:
            return

        for detective_id in self._remaining_detective_ids:
            remaining_others = [
                i for i in self._remaining_player_ids if i != detective_id
            ]
            target_id = self._players[detective_id].player.choose_target(
                remaining_others
            )
            if target_id in self._remaining_players:
                pass

    def _night(self):
        self._mafia_round()
        self._detective_round()

    def _day(self):
        self._victim_id = None
