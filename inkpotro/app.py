# Import QApplication to create the main application loop
from PyQt6.QtWidgets import QApplication

# Import Manager class for loading the GitHub token
from inkpotro.auth import Manager

# Import command-line arguments and exit function
from sys import argv, exit

# Import the authentication window UI class
from inkpotro.controllers import AuthenticationWindow

# Function to start and run the application
def run_app():
    # Try to load a previously saved GitHub token
    token = Manager().load_token()
    
    # If a token exists, the user is already authenticated
    if token:
        # TODO: Add logic for authenticated users
        return
    
    # Create the Qt application with command-line arguments
    app = QApplication(argv)

    # Set the name of the application
    app.setApplicationName("Inkpotro")

    # Create an instance of the authentication window
    window = AuthenticationWindow()

    # Show the authentication window
    window.show()

    # Execute the application event loop and exit on close
    exit(app.exec())