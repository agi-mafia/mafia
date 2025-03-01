from src.player.player import Player
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser
from langchain.chains import LLMChain


class Detective(Player):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Detective"
        self.parser = JsonOutputParser()
        
        # Initialize the prompt template for target selection
        self.target_prompt = PromptTemplate(
            template="""
            You should choose a player to verify their identity.
            Respond with a JSON object containing the chosen player index.
            
            {format_instructions}
            
            Example response:
            {{"chosen_player": 2}}
            """,
            input_variables=[],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def choose_target(self) -> int:
        try:
            # Create the chain using LLMChain instead of pipe chaining
            chain = LLMChain(
                llm=self.model_provider.model,
                prompt=self.target_prompt
            )
            
            # Run the chain with empty input (since there are no input variables)
            output = chain.run({})
            print(f"Raw output from model: {output}")
            
            # Parse the output into a dict
            parsed_output = self.parser.parse(output)
            if isinstance(parsed_output, dict) and "chosen_player" in parsed_output:
                return int(parsed_output["chosen_player"])
            else:
                print("Invalid response format from model")
                return -1
        except Exception as e:
            print(f"Error in choose_target: {e}")
            return -1

    def receive_info(self, prompt: str) -> str:
        return self.model_provider.inference(prompt)
