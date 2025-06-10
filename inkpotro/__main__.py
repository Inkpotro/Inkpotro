# Import the Manager class for handling GitHub token
from inkpotro.auth import Manager

# Import GetToken (token input UI) and Dashboard (main application UI)
from inkpotro.ui import GetToken, Dashboard

# Create an instance of the Manager class
token_manager =  Manager()

# Try to load the existing GitHub token
token =  token_manager.load_token()

# Check if a valid token was loaded
if token:
    # If token exists, launch the main Dashboard window
    Dashboard()
else:
    # Launch token input window if no token is found
    GetToken()