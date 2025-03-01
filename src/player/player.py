from model.model_provider import ModelProvider


class Player:
    def __init__(self, index: int):
        self.index = 0
        self.model_provider = ModelProvider("deepseek")
        self.role = "Player"

    def listen(self, context: str) -> None:
        self.model_provider.inference(context)
        return

    def speak(self) -> str:
        context = "You should speak your opinion about the situation now"
        words = self.model_provider.inference(context)
        return words

    def vote(self) -> int:
        context = """
            You can now vote off a player. Again, if you are a villager, you should try to vote off a werewolf,
            but if you are a werewolf, you should try to vote off a non wereworlf. Please choose a player by typing
            their number. You should only provide a number meaning the player that you want to vote off."
        """
        vote = self.model_provider.inference(context)
        return int(vote)

    def speak_last_words(self, dead_reason: int) -> str:
        context = ""
        if dead_reason == 0:
            context += "You are now dead because you were lynched"
        elif dead_reason == 1:
            context += "You are now dead because you were voted out"
        else:
            context += "You are now dead because you were killed by the werewolves"

        context += "You can now speak your last words"
        last_words = self.model_provider.inference(context)
        return last_words
