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
    
    def save_log(self, json_data: Dict[str, Any], log_id: Union[str, int]) -> str:
        """
        Save JSON data to a file named after the provided ID.
        
        Args:
            json_data (Dict[str, Any]): The JSON data to save
            log_id (Union[str, int]): The ID to use as the filename
            
        Returns:
            str: The path to the saved file
        """
        # Ensure the log_id is a string
        log_id = str(log_id)
        
        # Create the log file path
        log_file_path: Path = Path(self.logging_dir) / f"{log_id}.json"
        
        # Write the JSON data to the file
        with open(log_file_path, 'w') as f:
            json.dump(json_data, f, indent=2)
            
        return str(log_file_path)
    
    def read_log(self, log_id: Union[str, int]) -> Dict[str, Any]:
        """
        Read JSON data from a file named after the provided ID.
        
        Args:
            log_id (Union[str, int]): The ID to use to find the file
            
        Returns:
            Dict[str, Any]: The JSON data from the file
            
        Raises:
            FileNotFoundError: If the log file does not exist
        """
        # Ensure the log_id is a string
        log_id = str(log_id)
        
        # Create the log file path
        log_file_path: Path = Path(self.logging_dir) / f"{log_id}.json"
        
        # Check if the file exists
        if not log_file_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_file_path}")
        
        # Read the JSON data from the file
        with open(log_file_path, 'r') as f:
            return json.load(f) 