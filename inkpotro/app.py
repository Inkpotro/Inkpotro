# Import QApplication to create the main application loop
from PyQt6.QtWidgets import QApplication

# Import Manager class for loading the GitHub token
from inkpotro.auth import Manager

# Import command-line arguments and exit function
from sys import argv, exit

# Import the authentication and dashboard window UI classes
from inkpotro.controllers import AuthenticationWindow, DashboardWindow

# Function to start and run the application
def run_app():
    # Create the Qt application
    app = QApplication(argv)
    app.setApplicationName("Inkpotro")

    # Try to load a previously saved GitHub token
    token = Manager().load_token()

    # If a token exists, the user is already authenticated
    if token:
        window = DashboardWindow()
    else:
        window = AuthenticationWindow()

    # Show the appropriate window
    window.show()

    # Execute the application event loop and exit on close
    exit(app.exec())