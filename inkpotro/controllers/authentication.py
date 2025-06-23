# Import Path from pathlib to handle filesystem paths
from pathlib import Path

# Access system-level functions and arguments
import sys

# Import necessary PyQt6 widgets and classes
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

# Import uic for loading .ui files
from PyQt6 import uic

# Import the Manager class for saving GitHub token
from inkpotro.auth import Manager

# Function to get the path of resources (UI files), works in both development and bundled (frozen) mode
def resource_path(relative_path):
    # Check if the application is running in a bundled (frozen) environment like PyInstaller
    if getattr(sys, 'frozen', False):
        # If frozen, use the temporary folder created by PyInstaller
        ui_path = Path(sys._MEIPASS)
    else:
        # If not frozen, use the directory two levels up from the current file
        ui_path = Path(__file__).resolve().parent.parent
    # Return the full path to the resource
    return ui_path / relative_path

# Class representing the authentication window
class AuthenticationWindow(QWidget):
    # Constructor to initialize the window
    def __init__(self):
        # Call parent class constructor
        super().__init__()

        # Get the full path to the UI file
        ui_path = resource_path("ui/authentication.ui")

        # Load the UI file into this widget
        uic.loadUi(ui_path, self)

        # Connect the setup_github_token button click to save_token method
        self.setup_github_token.clicked.connect(self.save_token)

    # Method to save the GitHub token entered by the user
    def save_token(self):
        # Get the text from the GitHub token input field
        token = self.github_token_input.text()

        # If the token field is not empty
        if token:
            # Create an instance of the Manager class
            manager = Manager()

            # Call the save_token method to store the token
            manager.save_token(token)

            # Create a message box to notify the user
            message_box = QMessageBox(self)

            # Set the title of the message box
            message_box.setWindowTitle("GitHub Authenticated - Inkpotro")

            # Set the message text
            message_box.setText("GitHub Token saved successfully!")

            # Set the icon to an information symbol
            message_box.setIcon(QMessageBox.Icon.Information)

            # Set a single OK button in the message box
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            # Show the message box and store the user's response
            response = message_box.exec()

            # If the user clicks OK, quit the application
            if response == QMessageBox.StandardButton.Ok:
                QApplication.quit()
        else:
            # If no token is provided, show an information message box
            QMessageBox.information(self, "Missing GitHub Token", "Please enter your GitHub token to proceed.")