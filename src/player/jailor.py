from src.player.player import BasePlayer


class Jailor(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Jailor"

    def choose_target(self) -> int:
        context = """
            You are the jailor. You can protect one player from being killed.
        """
        protected_player = self.model_provider.inference(context)
        return int(protected_player)
