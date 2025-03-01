from player.player import Player


class Detective(Player):
    def __init__(self):
        super().__init__()

    def choose_target(self) -> int:
        return 0

    def receive_info(self) -> int:
        return 0
