class Player:
    def __init__(self):
        self.context = ""
        pass

    def listen(self, new_context: str) -> None:
        self.context += new_context
        pass

    def speak(self) -> str:
        return ""

    def vote(self) -> int:
        return 0

    def speak_last_words(self) -> str:
        return ""
