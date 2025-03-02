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
        self.parser = JsonOutputParser()
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
            template=self.context
            + dedent(
                """\
                It's night now. You should propose a victim. You should communicate with the other mafia to decide who to propose.
                You can choose a player to propose as a victim from the following candidates: {candidates} and the reason why you propose this player to be eliminated.

                Example response:
                I propose player 2 to be eliminated.
            """
            ),
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
            return ""

    def receive_victim_proposal(
        self,
        proposer: int,
        proposal: str,
    ) -> str:
        self.context += (
            f"\nTonight, Mafia {proposer}'s propsal statement is: {proposal}."
        )
        return self.context

    def choose_victim(self, candidates: List[int]) -> int:

        self.target_prompt = PromptTemplate(
            template=self.context
            + dedent(
                """\
            Tonight, you can vote a player to be eliminated from the following candidates: {candidates}.
            Respond with a JSON object containing the chosen player index.

            {format_instructions}

            Example response:
            {{"chosen_player": 2}}
            """
            ),
            input_variables=[],
            partial_variables={
                "candidates": candidates,
                "format_instructions": self.parser.get_format_instructions(),
            },
        )
        try:
            # Create the chain using LLMChain instead of pipe chaining
            chain = LLMChain(llm=self.model_provider.model, prompt=self.target_prompt)

            # Run the chain with empty input (since there are no input variables)
            output = chain.run({})

            # Parse the output into a dict
            parsed_output = self.parser.parse(output)
            if isinstance(parsed_output, dict) and "chosen_player" in parsed_output:
                res = int(parsed_output["chosen_player"])
                self.context += f"I chose player {res} to be eliminated tonight."
                self.logger.log(
                    self.index,
                    self.is_live,
                    "eliminate",
                    res,
                    f"""
                    Player {self.index} is a mafia and he chooses to eliminate {res} tonight.
                """,
                )
                return res
            else:
                print("Invalid response format from model")
                self.logger.log(
                    self.index,
                    self.is_live,
                    "eliminate",
                    -1,
                    f"""
                    Player {self.index} is a mafia but he chooses not to eliminate anyone tonight.
                """,
                )
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            self.logger.log(
                self.index,
                self.is_live,
                "eliminate",
                -1,
                f"""
                    Player {self.index} is a mafia but he chooses not to eliminate anyone tonight.
                """,
            )
            return -1
