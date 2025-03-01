from langchain.chains import LLMChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.player.base_player import BasePlayer


class Hunter(BasePlayer):
    def __init__(self, index, model_name):
        super().__init__(index=index, model_name=model_name)
        self.role = "Hunter"
        self.parser = JsonOutputParser()
        # TODO: add hunter context to the context

    def shoot(self) -> int:
        self.target_prompt = PromptTemplate(
            template=self.context + """
            Now you are died, based on your hunter role, you can choose to eliminate one player from the game.
            Respond with a JSON object containing the chosen player index.

            {format_instructions}

            Example response:
            {{"chosen_player": 2}}
            """,
            input_variables=[],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        try:
            # Create the chain using LLMChain instead of pipe chaining
            chain = LLMChain(llm=self.model_provider.model, prompt=self.target_prompt)

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
    
