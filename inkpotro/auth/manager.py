# Used to access package resources (e.g., file paths)
from importlib.resources import files

# Importing the resource directory from the 'inkpotro' package
from inkpotro import config

# Function to check if a file exists
from os.path import exists

# Functions to read/write JSON data
from json import load, dump

# Get the path to the token.json file inside the config resource directory
token_path = files(config).joinpath("token.json")

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