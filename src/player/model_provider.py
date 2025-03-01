class ModelProvider:
    def __init__(self, model_name: str):
        self.model = some model initialization
        self.model_name = model_name

    def inference(self, prompt: str) -> str:
        return model.predict(prompt)
