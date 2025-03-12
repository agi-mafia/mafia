from textwrap import dedent
from typing import List

from langchain.chains import LLMChain

from langchain_core.output_parsers.json import JsonOutputParser

from langchain_core.prompts import PromptTemplate
from mafia.player.base_player import BasePlayer


class Jailor(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Jailor"
        self.parser = JsonOutputParser()
        self.context += dedent(
            """\
            You are a Jailor, a role that allows you to choose one player each night to protect from elimination.
            You can only choose one player from the valid candidates.
            Your goal is to help all the town people to find the mafia players and eliminate them.
            In each day, You will be given a list of players who are still alive. You can choose one of them to protect from elimination.\
        """
        )

    def choose_target(self, candidates: List[int]) -> int:
        self.target_prompt = PromptTemplate(
            template=self.context
            + """
            It is now nighttime. As the Jailor, you can choose to protect one player from the following list of candidates:
            {candidates}
            Respond with a JSON object containing the chosen player index.

            {format_instructions}

            Example response:
            {{"chosen_player": 2}}
            """,
            input_variables=[],
            partial_variables={
                "candidates": "[" + ", ".join([str(x) for x in candidates]) + "]",
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
                player_index = int(parsed_output["chosen_player"])
                self.context += (
                    f"I chose player {player_index} to be protected from elimination."
                )
                self.logger.log(
                    self.index,
                    self.role,
                    self.is_live,
                    "shoot",
                    player_index,
                    f"""
                        Player {self.index} is a jailor but he chooses to protect {player_index} tonight.
                    """,
                )
                return player_index
            else:
                print("Invalid response format from model")
                self.logger.log(
                    self.index,
                    self.role,
                    self.is_live,
                    "shoot",
                    -1,
                    f"""
                        Player {self.index} is a jailor but he chooses not to protect anyone tonight.
                    """,
                )
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            self.logger.log(
                self.index,
                self.role,
                self.is_live,
                "shoot",
                -1,
                f"""
                    Player {self.index} is a jailor but he chooses not to protect anyone tonight.
                """,
            )
            return -1
