import json
from datetime import datetime

from pydantic import BaseModel, Field


# Define the log entry model using Pydantic with an extra timestamp field
class LogEntry(BaseModel):
    user: int  # User ID
    status: bool  # Indicates whether the user is alive (True) or not (False)
    action: str  # Describes what the user is doing
    target_user: int  # The ID of the target user on which the action is performed
    string: str  # Message or comment from the user
    timestamp: datetime = Field(
        default_factory=datetime.now
    )  # Automatically set to current time


# Logger class to handle log entries
class Logger:
    def __init__(self):
        self.entries = []  # In-memory storage for log entries

    def log(
        self, user: int, status: bool, action: str, target_user: int, string: str
    ) -> None:
        """
        Creates a LogEntry, validates the input data, and logs it.
        """
        entry = LogEntry(
            user=user,
            status=status,
            action=action,
            target_user=target_user,
            string=string,
        )
        self.entries.append(entry)
        print(entry.model_dump_json())

    def get_logs(self):
        """
        Returns the list of all log entries.
        """
        return self.entries

    def write_logs(self, filename: str = "logs.json") -> None:
        """
        Writes the current log entries to a JSON file.
        """
        # Convert each log entry to a dict (including the timestamp)
        log_dicts = [entry.model_dump() for entry in self.entries]
        # Write the list of log entries to a JSON file with pretty printing
        with open(filename, mode="w") as jsonfile:
            json.dump(log_dicts, jsonfile, indent=4, default=str)
