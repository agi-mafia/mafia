from src.model.model import Model


class BasePlayer:
    def __init__(self, index: int, model_name: str):
        self.index = index
        self.model_provider = Model(model_name)
        self.role = "Player"
        self.context = ""

    def listen(self, speech: str) -> None:
        self.context += speech

    def listen_vote(self, votes_dict: dict):
        for key, value in votes_dict.items():
            self.context += f"""
                Player {key} has voted to eliminate player {value}.
            """
        return

    def listen_death(self, death_index: int):
        self.context += f"""
            Player {death_index} has been eliminated.
        """
        return

    def listen_talk(self, talk_index, talk_content):
        self.context += f"""
            Player {talk_index} has spoken: {talk_content}.
        """
        return

    def speak(self) -> str:
        self.context += """
            You should now express your perspective on the matter.
        """
        words = self.model_provider.inference(self.context)
        return words

    def vote(self) -> int:
        self.context += """
            You can now vote off a player. Again, if you are a villager, you should try to vote off a werewolf,
            but if you are a werewolf, you should try to vote off a non wereworlf. Please choose a player by typing
            their number. You should only provide a number meaning the player that you want to vote off."
        """
        vote = self.model_provider.inference(self.context)
        return int(vote)

    def speak_last_words(self, dead_reason: int) -> str:
        if dead_reason == 0:
            self.context += """
                You have been eliminated because you were voted out.
            """
        elif dead_reason == 1:
            self.context += """
                You have been eliminated because the Mafias selected you as their target during the night.
            """
        else:
            self.context += """
                You have been eliminated because the hunter chose to eliminate you at the moment of his own elimination.
            """

        self.context += """
            You can now speak your last words.
        """
        last_words = self.model_provider.inference(self.context)
        return last_words
