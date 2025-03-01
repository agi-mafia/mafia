from src.player.player import Player
from src.model.model import Model


class Mafia(Player):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Mafia"

    def know_teammate(self, teammates: list):
        teammates_str = ", ".join([str(i) for i in teammates])
        context = f"""
            The following players are your teammates: {teammates_str}
        """
        self.model_provider.inference(context)
        return

    def propose_victim(self) -> str:
        context = """
            It's night now. You should propose a victim. You should communicate with the other werewolves to decide who to propose.
        """
        return self.model_provider.inference(context)

    def choose_victim(self) -> int:
        context = """
            It's time to choose a victim now. You should choose a victim.
        """
        victim = self.model_provider.inference(context)
        return int(victim)
