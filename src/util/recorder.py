import json
import os
from pathlib import Path
from typing import Dict, Any, Union, Optional


class Recorder:
    """
    Utility class for saving and reading JSON data to/from log files.
    Files are stored in a logging directory and named according to provided IDs.
    """
    
    def __init__(self, logging_dir: str = "logging") -> None:
        """
        Initialize the Recorder with the path to the logging directory.
        
        Args:
            logging_dir (str): Path to the logging directory (default: "logging")
        """
        self.logging_dir: str = logging_dir
        
        # Create logging directory if it doesn't exist
        Path(self.logging_dir).mkdir(exist_ok=True, parents=True)
    
    def save_log(self, json_data: Dict[str, Any], game_id: Union[str, int]) -> str:
        """
        Save JSON data to a file named after the provided ID.
        If the file already exists, append the new data on a new line.
        
        Args:
            json_data (Dict[str, Any]): The JSON data to save
            game_id (Union[str, int]): The ID to use as the filename
            
        Returns:
            str: The path to the saved file
        """
        # Ensure the game_id is a string
        game_id = str(game_id)
        
        # Create the log file path
        log_file_path: Path = Path(self.logging_dir) / f"{game_id}.json"
        
        # Check if file exists to determine if we should append
        if log_file_path.exists():
            # Append the JSON data to the file on a new line
            with open(log_file_path, 'a') as f:
                f.write('\n')
                json.dump(json_data, f)
        else:
            # Write the JSON data to a new file
            with open(log_file_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
        return str(log_file_path)
    
    def save_string(self, string_data: str, game_id: Union[str, int]) -> str:
        """
        Save a string to a file named after the provided ID.
        If the file already exists, append the new string on a new line.
        
        Args:
            string_data (str): The string data to save
            game_id (Union[str, int]): The ID to use as the filename
            
        Returns:
            str: The path to the saved file
        """
        # Remove all newlines from the string data
        string_data = string_data.replace('\n', '')
        string_data = string_data + "\n\n"
        
        # Ensure the game_id is a string
        game_id = str(game_id)
        
        # Create the log file path
        log_file_path: Path = Path(self.logging_dir) / f"{game_id}.txt"
        
        # Check if file exists to determine if we should append
        if log_file_path.exists():
            # Append the string data to the file on a new line
            with open(log_file_path, 'a') as f:
                f.write(f"\n{string_data}")
        else:
            # Write the string data to a new file
            with open(log_file_path, 'w') as f:
                f.write(string_data)
            
        return str(log_file_path)
    
    def read_log(self, game_id: Union[str, int]) -> Dict[str, Any]:
        """
        Read JSON data from a file named after the provided ID.
        
        Args:
            game_id (Union[str, int]): The ID to use to find the file
            
        Returns:
            Dict[str, Any]: The JSON data from the file
            
        Raises:
            FileNotFoundError: If the log file does not exist
        """
        # Ensure the game_id is a string
        game_id = str(game_id)
        
        # Create the log file path
        log_file_path: Path = Path(self.logging_dir) / f"{game_id}.json"
        
        # Check if the file exists
        if not log_file_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_file_path}")
        
        # Read the JSON data from the file
        with open(log_file_path, 'r') as f:
            return json.load(f) 