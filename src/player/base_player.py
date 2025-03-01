from src.model.model import Model


class BasePlayer:
    def __init__(self, index: int, model_name: str):
        self.index = index
        self.model_provider = Model(model_name)
        self.role = "Player"
        self.context = ""

    def listen(self, context: str) -> None:
        self.context += context
        self.model_provider.inference(self.context)
        return

    def speak(self) -> str:
        self.context += """
            You should speak your opinion about the situation now
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
                You are now dead because you were lynched
            """
        elif dead_reason == 1:
            self.context += """
                You are now dead because you were voted out
            """
        else:
            self.context += """
                You are now dead because you were killed by the werewolves
            """

        self.context += """
            You can now speak your last words
        """
        last_words = self.model_provider.inference(self.context)
        return last_words
