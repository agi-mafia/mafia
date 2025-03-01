from src.player.player import BasePlayer


class Hunter(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index)
        self.role = "Hunter"

    def shoot(self) -> int:
        context = "You can choose to shoot one player and that player will be eliminated from the game."
        killed_player = self.model_provider.inference(context)
        return int(killed_player)
