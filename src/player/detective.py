from textwrap import dedent
from typing import List

from langchain.chains import LLMChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from src.player.base_player import BasePlayer
from src.player.role import Role


class Detective(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Detective"
        self.parser = JsonOutputParser()
        self.context += dedent(
            """\
            You are a detective. You can choose a player to verify their identity each day. You can only choose one player from the valid candidates.
            Your goal is to help all the town people to find the mafia players and eliminate them.
            In each day, You will be given a list of players who are still alive. You can choose one of them to verify their identity.
            If the player is a mafia player, you will be given a message that the player is a mafia player.
            If the player is not a mafia player, you will be given a message that the player is a town person.
            """
        )

    def choose_target(self, candidates: List[int]) -> int:

        # Initialize the prompt template for target selection
        self.target_prompt = PromptTemplate(
            template=self.context
            + dedent(
                """\
            You can choose a player to verify their identity. The valid candidates are: {candidates}.
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
                target_id = int(parsed_output["chosen_player"])
                self.context += f"I chose player {parsed_output['chosen_player']} to verify its identity."
                self.logger.log(
                    self.index,
                    self.is_live,
                    "choose_target",
                    int(parsed_output["chosen_player"]),
                    f"Detective {self.index} has chosen target {target_id} to verify its identity",
                )
                return int(parsed_output["chosen_player"])
            else:
                print("Invalid response format from model")
                self.logger.log(
                    self.index,
                    self.is_live,
                    "choose_target",
                    -1,
                    f"Detective {self.index} has given up choosing a target to verify its identity",
                )
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            self.logger.log(
                self.index,
                self.is_live,
                "choose_target",
                -1,
                f"Detective {self.index} has given up choosing a target to verify its identity",
            )
            return -1

    def receive_info(self, target_id: int, target_role: Role):
        self.context += f"""
            Player {target_id} is a {target_role.name}.
        """
        return
