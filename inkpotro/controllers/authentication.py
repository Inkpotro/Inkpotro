# Import Path from pathlib to handle filesystem paths
from pathlib import Path

# Access system-level functions and arguments
import sys

# Import necessary PyQt6 widgets and classes
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QPixmap

# Import uic for loading .ui files
from PyQt6 import uic

# Import the Manager class
from inkpotro.auth import Manager

# Import GitHub API
from github import Github, BadCredentialsException

# Import the dashboard window UI class
from inkpotro.controllers.dashboard import DashboardWindow

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

            # Get the full path to the custom icon
            icon_path = resource_path("icons/success.png")
            pixmap = QPixmap(str(icon_path))

            # Set the icon
            message_box.setIconPixmap(pixmap)

            # Set a single OK button in the message box
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            # Show the message box and store the user's response
            response = message_box.exec()

            # If the user clicks OK
            if response == QMessageBox.StandardButton.Ok:
                try:
                    # Attempt to log in to GitHub using the token
                    login = Github(token)

                    # Retrieve the user object associated with the token
                    user = login.get_user()

                    # Get the user's name from the GitHub profile
                    user_name = user.name

                    # Open Dashboard
                    self.open_dashboard(user_name)
                except BadCredentialsException:
                    self.show_invalid_token_dialog()
        else:
            # If no token is provided, show an information message box
            # Create a message box to notify the user
            message_box = QMessageBox(self)

            # Set the title of the message box
            message_box.setWindowTitle("Missing GitHub Token")

            # Set the message text
            message_box.setText("Please enter your GitHub token to proceed.")

            # Get the full path to the custom icon
            icon_path = resource_path("icons/information.png")
            pixmap = QPixmap(str(icon_path))

            # Set the icon
            message_box.setIconPixmap(pixmap)

            # Show the message box
            response = message_box.exec()
    
    # Open dashboard
    def open_dashboard(self, author_name):
        # Create an instance of the DashboardWindow class
        self.dashboard = DashboardWindow()

        # Set the GitHub author's name in the author input field
        self.dashboard.author_input.setText(author_name)

        # Show the dashboard window to the user
        self.dashboard.show()

        # Close the current authentication window
        self.close()

    # Method to show a critical error dialog when the GitHub token is invalid
    def show_invalid_token_dialog(self):
        # Create a message box to notify the user
        message_box = QMessageBox(self)

        # Set the title of the message box
        message_box.setWindowTitle("Invalid Token")

        # Set the message text
        message_box.setText("Your GitHub token is invalid. Please login again.")

        # Get the full path to the custom icon
        icon_path = resource_path("icons/error.png")
        pixmap = QPixmap(str(icon_path))

        # Set the icon
        message_box.setIconPixmap(pixmap)

        # Set a single OK button in the message box
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Show the message box
        response = message_box.exec()