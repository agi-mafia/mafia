from textwrap import dedent
from typing import List

from langchain.chains import LLMChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from mafia.game.game_config import GameConfig
from mafia.game.game_log import Logger
from mafia.model.model import Model


class BasePlayer:
    def __init__(self, index: int, model_name: str):
        self.index = index
        self.model_provider = Model(model_name)
        self.role = "Player"
        self.parser = JsonOutputParser()
        self.context = ""
        self.logger = Logger()
        self.is_live = True

    def listen(self, speech: str) -> None:
        self.context += speech

    def listen_vote(self, votes_dict: dict):
        for key, value in votes_dict.items():
            self.context += f"""
                Player {key} has voted to eliminate player {value}.
            """
            vote_str = ""
            for key, value in votes_dict.items():
                vote_str += f"""
                    Player {self.index} know that player {key} has voted to eliminate player {value}.
                """
            self.logger.log(
                self.index,
                self.role,
                self.is_live,
                "listen_vote",
                self.index,
                vote_str,
            )
        return

    def listen_death(self, death_index: int):
        if (death_index) == -1:
            self.context += """
                No one was eliminated last night.
            """
            self.logger.log(
                self.index,
                self.role,
                self.is_live,
                "listen",
                death_index,
                f"Player {death_index} was eliminated last night.",
            )
            return

        self.context += f"""
            Player {death_index} was eliminated last night.
        """
        self.logger.log(
            self.index,
            self.role,
            self.is_live,
            "listen",
            death_index,
            f"Player {death_index} was eliminated last night.",
        )
        return

    def listen_talk(self, talk_index, talk_content):
        self.context += f"""
            Player {talk_index} has spoken: {talk_content}.
        """
        self.logger.log(
            self.index,
            self.role,
            self.is_live,
            "listen_talk",
            talk_index,
            f"Player {self.index} listened to talk from {talk_index}. The content is {talk_content}.",
        )
        return

    def speak(self) -> str:
        self.context += """
            You should now express your perspective on the matter.
        """
        words = self.model_provider.inference(self.context)
        self.logger.log(
            self.index,
            self.role,
            self.is_live,
            "speak",
            self.index,
            f"Player {self.index} spoke: {words}",
        )
        return words

    def vote(self, candidates: List[int]) -> int:
        self.target_prompt = PromptTemplate(
            template=self.context
            + dedent(
                """\
            You can now vote off a player. Again, if you are a townpeople, you should try to vote off a mafia,
            but if you are a mafia, you should try to vote off a non mafia. Please choose a player by typing
            their number. You should only provide a number meaning the player that you want to vote off.
            Vote from the following candidates: {candidates}."

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
                self.context += f"I chose player {res} to be eliminated today."
                print(self.context)
                self.logger.log(
                    self.index,
                    self.role,
                    self.is_live,
                    "vote",
                    res,
                    f"Player {self.index} voted {res} off this round.",
                )
                return res
            else:
                print("Invalid response format from model")
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            return -1

    def speak_last_words(self) -> str:
        self.context += """
            You can now speak your last words.
        """
        last_words = self.model_provider.inference(self.context)
        self.logger.log(
            self.index,
            self.role,
            self.is_live,
            "speak",
            self.index,
            f"""
                Player {self.index} spoke his last words: {last_words}
            """,
        )
        return last_words
