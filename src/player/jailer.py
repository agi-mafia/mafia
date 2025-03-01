from src.player.player import Player


<<<<<<< HEAD
class Jailor(Player):
    def __init__(self, index):
=======
class Jailer(Player):
    def __init__(self, index, model_name):
>>>>>>> LLMSetup
        super().__init__(index=index)
        self.role = "Jailor"

    def choose_target(self) -> int:
        context = """
            You are the jailor. You can protect one player from being killed.
        """
        protected_player = self.model_provider.inference(context)
        return int(protected_player)
