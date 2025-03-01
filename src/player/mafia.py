from typing import List, Tuple
from src.model.model import Model
from src.player.base_player import BasePlayer


class Mafia(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Mafia"

    def see_teammates(self, teammates: list):
        teammates_str = ", ".join([str(i) for i in teammates])
        self.context += f"""
            The following players are your teammates: {teammates_str}
        """
        self.model_provider.inference(self.context)
        return

    # TODO FIX
    def propose_victim(self, candidates: List[int]) -> Tuple[int, str]:
        self.context += """
            It's night now. You should propose a victim. You should communicate with the other werewolves to decide who to propose.
        """
        return candidates[-1], self.model_provider.inference(self.context)

    def receive_victim_proposal(
        self,
        candidates: List[int],
        proposer: int,
        proposed_victim_id: int,
        proposed_reason: str,
    ) -> None:
        pass
        # TODO FIX

    # TODO FIX
    def choose_victim(self, candidates: List[int]) -> int:
        self.context += """
            It's time to choose a victim now. You should choose a victim.
        """
        victim = self.model_provider.inference(self.context)
        return int(victim)
