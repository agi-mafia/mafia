from textwrap import dedent
from typing import List

from langchain.chains import LLMChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.player.base_player import BasePlayer


class Hunter(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Hunter"
        self.parser = JsonOutputParser()
        self.context += dedent(
            """\
            You are a hunter. You are a role that, upon being eliminated, has the ability to take one other player to be eliminated as well.
            You can only choose one player from the valid candidates.
            Your goal is to help all the town people to find the mafia players and eliminate them.\
            """
        )

    def shoot(self, candidates: List[int]) -> int:
        self.target_prompt = PromptTemplate(
            template=self.context
            + dedent(
                """\
            Now you are eliminated, based on your hunter role, you can choose to eliminate one player from the following available candidates: {candidates}.
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
            print(f"Raw output from model: {output}")

            # Parse the output into a dict
            parsed_output = self.parser.parse(output)
            if isinstance(parsed_output, dict) and "chosen_player" in parsed_output:
                player_index = int(parsed_output["chosen_player"])
                self.context += f"I chose player {player_index} to be eliminated."
                self.logger.log(
                    self.index,
                    self.role,
                    self.is_live,
                    "eliminate",
                    player_index,
                    f"""
                        Player {self.index} is a hunter and he chose to eliminate player {player_index} when he's elimianted.
                    """,
                )
                return player_index
            else:
                print("Invalid response format from model")
                self.logger.log(
                    self.index,
                    self.role,
                    self.is_live,
                    "eliminate",
                    -1,
                    f"""
                        Player {self.index} is a hunter but he gives up eliminating anyone when he's eliminated.
                    """,
                )
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            self.logger.log(
                self.index,
                self.role,
                self.is_live,
                "eliminate",
                -1,
                f"""
                    Player {self.index} is a hunter but he gives up eliminating anyone when he's eliminated.
                """,
            )
            print(f"Error in choose_target: {e}")
            return -1
