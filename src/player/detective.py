from player.player import Player


class Detective(Player):
    def __init__(self, index):
        super().__init__(index=index)
        self.role = "Detective"

    def choose_target(self) -> int:
        context = "You should choose a player to verify their identity."
        target = self.model_provider.inference(context)
        return int(target)

    def receive_info(self, player_index: int, role: str) -> None:
        context = f"You know that the player {player_index} is a {role}."
        self.model_provider.inference(context)
        return
