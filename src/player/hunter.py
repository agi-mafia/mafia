from src.player.base_player import BasePlayer


class Hunter(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Hunter"

    def shoot(self) -> int:
        self.context += """
            You can choose to shoot one player and that player will be eliminated from the game.
        """
        killed_player = self.model_provider.inference(self.context)
        return int(killed_player)
