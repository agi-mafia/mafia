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
            {
                "chosen_player": 2
            }
            """,
            input_variables=[],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def choose_target(self) -> int:
        try:
            # Create and run the chain
            chain = self.target_prompt | self.model_provider.model | self.parser
            
            # Get the result
            result = chain.invoke({})
            
            # Extract the chosen player index from the JSON response
            if isinstance(result['text'], dict) and "chosen_player" in result['text']:
                return int(result['text']["chosen_player"])
            else:
                print("Invalid response format from model")
                return 22222
        except Exception as e:
            print(f"Error in choose_target: {e}")
            return 1111

    def receive_info(self, player_index: int, role: str) -> None:
        try:
            # Create a prompt template for receiving information
            info_prompt = PromptTemplate(
                template="""
                You have learned new information about a player.
                Player {player_index} is a {role}.
                
                Provide your analysis in JSON format.
                {format_instructions}
                
                Example response:
                {
                    "acknowledged": true,
                    "analysis": "This information reveals that player X is the Y role",
                    "implications": "This means we should..."
                }
                """,
                input_variables=["player_index", "role"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}
            )
            
            # Create and run the chain
            chain = info_prompt | self.model_provider.model | self.parser
            
            # Get the result
            result = chain.invoke({
                "player_index": player_index,
                "role": role
            })
            
            return result
        except Exception as e:
            print(f"Error in receive_info: {e}")
            return {"error": str(e)}
