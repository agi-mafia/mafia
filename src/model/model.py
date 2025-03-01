from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage
import os

# Check if OpenAI API key exists in environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set your OpenAI API key.")
os.environ["OPENAI_API_KEY"] = api_key


class Model:
    def __init__(self, model_name: str):
        self.model = model_name

    def inference(self, prompt: str) -> str:
        
        # return self.model.predict(prompt)
        messages = [
            HumanMessage(
                content=prompt
            )
        ]
        chat = ChatLiteLLM(model=self.model)
        response = chat(messages)
        return response.content

    
    
