from src.player.base_player import BasePlayer


class Jailor(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Jailor"

    def choose_target(self) -> int:
        self.context += """
            You are the jailor. You can protect one player from being killed.
        """
        protected_player = self.model_provider.inference(self.context)
        return int(protected_player)
