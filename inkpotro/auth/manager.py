# Access system-level functions and arguments
import sys

# Handle filesystem paths
from pathlib import Path

# Function to check if a file exists
from os.path import exists

# Functions to read/write JSON data
from json import load, dump

# Get a path for storing the token, writable in all OS
def get_token_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller bundled mode: use user home directory
        config_dir = Path.home() / ".inkpotro" / "config"
    else:
        # Development mode: use project-relative config dir
        config_dir = Path(__file__).resolve().parent.parent / "config"
    
    # Create dir if doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "token.json"

# Get the path to the token.json file inside the config resource directory
token_path = get_token_path()

# Class responsible for managing the GitHub token
class Manager:
    # Method to load a GitHub token from the token.json file
    def load_token(self):
        # Check if token.json file exists
        if exists(token_path):
            # Open the file in read mode
            with open(token_path, "r") as file:
                # Load JSON data from the file
                github_config = load(file)

                # Return the value of 'git_token' if it exists
                return github_config.get("git_token")
        
        # If file doesn't exist, return None
        return None
    
    # Method to save a GitHub token to the token.json file
    def save_token(self, token):
        # Open the file in write mode
        with open(token_path, "w") as file:
            # Save the token in JSON format with the key 'git_token'
            dump({"git_token": token}, file)