from player.player import Player


class Jailer(Player):
    def __init__(self):
        super().__init__()

    def choose_target(self) -> int:
        return 0
