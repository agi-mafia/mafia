from src.player.base_player import BasePlayer


class Jailor(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Jailor"
        self.context += """
            You are a Jailor, a role that allows you to choose one player each night to protect from elimination.
        """

    def choose_target(self) -> int:
        self.context += """
            It's time to select a target to protect. You need to make your choice now.
        """
        protected_player = self.model_provider.inference(self.context)
        return int(protected_player)
