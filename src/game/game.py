from collections import defaultdict

from src.game.game_config import GameConfig
from src.game.game_log import Logger
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
        self._victim_id = -1
        self._lynch_id = -1
        self._jailor_protections = dict()
        self._logger = Logger()

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
    def _remaining_jailor_ids(self):
        return [
            i
            for i in self._players
            if self._players[i].role == Role.JAILOR
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
        if len(self._remaining_mafia_ids) <= 0:
            return

        # Each mafia proposes a victim
        for mafia_id in self._remaining_mafia_ids:
            other_mafia_ids = [i for i in self._remaining_mafia_ids if i != mafia_id]
            victim_proposal = self._players[mafia_id].player.propose_victim(
                self._remaining_player_ids
            )
            for other_mafia_id in other_mafia_ids:
                self._players[other_mafia_id].player.receive_victim_proposal(
                    proposer=mafia_id,
                    proposal=victim_proposal,
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
            self._players[mafia_id].player.listen_vote_night(other_mafia_votes)

        self._victim_id = most_frequent_random(victim_votes.values())
        self._logger.log(
            user=mafia_id,
            role="system",
            status=True,
            action="Voted victim",
            target_user=self._victim_id,
            string=f"Player {self._victim_id} decided to eliminate {self._victim_id} at night. Its role is {self._players[self._victim_id].role}",
        )

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
            if target_id in remaining_others:
                self._players[detective_id].player.receive_info(
                    target_id, self._players[target_id].role
                )
            # self._logger.log(
            #     user=detective_id,
            #     status=True,
            #     action="Verified player",
            #     target_user=target_id,
            #     string=f"Player {target_id} is a verified by detective {detective_id}, its role is {self._players[target_id].role}"
            # )

    def _jailor_round(self):
        if len(self._remaining_jailor_ids) <= 0:
            return

        for jailor_id in self._remaining_jailor_ids:
            remaining_others = [i for i in self._remaining_player_ids if i != jailor_id]
            target_id = self._players[jailor_id].player.choose_target(remaining_others)
            if target_id in remaining_others:
                self._jailor_protections[jailor_id] = target_id

    def _night(self):
        self._mafia_round()
        self._detective_round()
        self._jailor_round()

    def _eliminate_victim(self):
        if self._victim_id in self._jailor_protections.values():
            self._victim_id = -1
            self._logger.log(
                user=-1,
                role="system",
                status=True,
                action="Protected victim",
                target_user=self._victim_id,
                string=f"Player {self._victim_id} was eliminated failed because it was protected by jailor.",
            )
        if self._victim_id != -1:
            self._players[self._victim_id].survival = Survival.ELIMINATED
            self._logger.log(
                user=-1,
                role="system",
                status=False,
                action="Eliminated victim",
                target_user=self._victim_id,
                string=f"Player {self._victim_id} was eliminated bt mafia.",
            )
        for player_id in self._remaining_player_ids:
            self._players[player_id].player.listen_death(self._victim_id)

    def _decide_lynch(self):

        # Each player speaks
        for player_id in self._remaining_player_ids:
            other_player_ids = [i for i in self._remaining_player_ids if i != player_id]
            speech = self._players[player_id].player.speak()
            for other_player_id in other_player_ids:
                self._players[other_player_id].player.listen_talk(
                    talk_index=player_id,
                    talk_content=speech,
                )

        # A final suspect is chosen via mafia vote
        suspect_votes = {
            i: self._players[i].player.vote(self._remaining_player_ids)
            for i in self._remaining_player_ids
        }
        for player_id in self._remaining_player_ids:
            other_player_ids = [i for i in self._remaining_player_ids if i != player_id]
            other_player_votes = {
                other_player_id: suspect_votes[other_player_id]
                for other_player_id in other_player_ids
            }
            self._players[player_id].player.listen_vote(other_player_votes)

        self._lynch_id = most_frequent_random(suspect_votes.values())

    def _execute_lynch(self):
        if self._lynch_id not in self._remaining_player_ids:
            return

        last_words = self._players[self._lynch_id].player.speak_last_words()
        self._players[self._lynch_id].survival = Survival.LYNCHED

        for player_id in self._remaining_player_ids:
            self._players[player_id].player.listen_talk(
                talk_index=self._lynch_id,
                talk_content=last_words,
            )

        self._logger.log(
            user=self._lynch_id,
            role="system",
            status=False,
            action="Voted lynch",
            target_user=-1,
            string=f"Player {self._lynch_id} was voted off.",
        )  # TODO: log the vote info and broadcast it.

        if self._players[self._lynch_id].role == Role.HUNTER:
            hunter_target = self._players[self._lynch_id].player.shoot(
                candidates=self._remaining_player_ids
            )
            self.hunter_retaliate(hunter_target)
            self._logger.log(
                user=self._lynch_id,
                role="system",
                status=False,
                action="Shoot",
                target_user=hunter_target,
                string=f"Player {hunter_target} was shot by hunter {self._lynch_id}.",
            )

    def hunter_retaliate(self, target_id):
        if target_id not in self._remaining_player_ids:
            return

        last_words = self._players[target_id].player.speak_last_words()
        self._players[target_id].survival = Survival.RETALIATED

        for player_id in self._remaining_player_ids:
            self._players[player_id].player.listen_talk(
                talk_index=target_id,
                talk_content=last_words,
            )

        if self._players[target_id].role == Role.HUNTER:
            hunter_target = self._players[target_id].player.shoot(
                candidates=self._remaining_players
            )
            self.hunter_retaliate(hunter_target)

    def _day(self):
        self._eliminate_victim()
        self._decide_lynch()
        self._execute_lynch()

        self._victim_id = -1
        self._jailor_protections = dict()
