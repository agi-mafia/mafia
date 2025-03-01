from player.player import Player


class Mafia(Player):
    def __init__(self):
        super().__init__()

    def propose_victim(self) -> int:
        return 0

    def choose_victim(self) -> int:
        return 0
