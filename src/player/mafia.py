from textwrap import dedent
from typing import List, Tuple

from langchain.chains import LLMChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from src.model.model import Model
from src.player.base_player import BasePlayer


class Mafia(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Mafia"
        self.context += dedent(
            """\
            You are a mafia player. Your objective is to cooperate with your fellow mafia members to eliminate the innocent townspeople (villagers).
            During the night phase, you and your fellow Mafia members secretly choose a villager to eliminate.
            In the subsequent day phase, all players, including the Mafia, discuss and vote to identify and eliminate suspected Mafia members.
            Your goal is to deceive the villagers by blending in and deflecting suspicion, thereby ensuring the Mafia's dominance and survival.
            """
        )

    def listen_vote_night(self, votes_dict: dict):
        for key, value in votes_dict.items():
            self.context += f"""
                Mafia {key} has voted to eliminate player {value}.
            """
        return

    def see_teammates(self, teammates: list):
        teammates_str = ", ".join([str(i) for i in teammates])
        self.context += f"""
            The following players are your teammates: {teammates_str}
        """
        return

    def propose_victim(self, candidates: List[int]) -> str:
        self.target_prompt = PromptTemplate(
            template=self.context + dedent("""\
                It's night now. You should propose a victim. You should communicate with the other mafia to decide who to propose.
                You can choose a player to propose as a victim from the following candidates: {candidates}.

                Example response:
                I propose player 2 to be eliminated.
            """),
            input_variables=[],
            partial_variables={
                "candidates": candidates,
            },
        )
        try:
            # Create the chain using LLMChain instead of pipe chaining
            chain = LLMChain(llm=self.model_provider.model, prompt=self.target_prompt)

            # Run the chain with empty input (since there are no input variables)
            output = chain.run({})

            return output
        except Exception as e:
            print(f"Error in choose_target: {e}")
            return -1

    def receive_victim_proposal(
        self,
        candidates: List[int],
        proposer: int,
        proposed_victim_id: int,
        proposed_reason: str,
    ) -> None:
        # TODO FIX
        pass

    # TODO FIX
    def choose_victim(self, candidates: List[int]) -> int:
        self.context += """
            It's time to choose a victim now. You should choose a victim.
        """
        victim = self.model_provider.inference(self.context)
        return int(victim)
