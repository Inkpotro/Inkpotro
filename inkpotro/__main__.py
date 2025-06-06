# Import the Manager class for handling GitHub token
from inkpotro.auth import Manager

# Import the GetToken class to prompt the user for token input
from inkpotro.ui import GetToken

# Create an instance of the Manager class
token_manager =  Manager()

# Try to load the existing GitHub token
token =  token_manager.load_token()

if token:
    # TODO: Add logic for authenticated users
    pass
else:
    # Launch token input window if no token is found
    GetToken()