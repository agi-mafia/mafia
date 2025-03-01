from player.player import Player


class Hunter(Player):
    def __init__(self, index):
        super().__init__(index=index)
        self.role = "Hunter"

    def shoot(self) -> int:
        context = "You can choose to shoot one player and that player will be eliminated from the game."
        killed_player = self.model_provider.inference(context)
        return int(killed_player)
