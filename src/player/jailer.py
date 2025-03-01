from src.player.player import Player


class Jailer(Player):
    def __init__(self, index, model_name):
        super().__init__(index=index)
        self.role = "Jailer"

    def choose_target(self) -> int:
        context = """
            You are the jailer. You can protect one player from being killed.
        """
        protected_player = self.model_provider.inference(context)
        return int(protected_player)
