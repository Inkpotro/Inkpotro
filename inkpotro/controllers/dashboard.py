# Import Path from pathlib to handle filesystem paths
from pathlib import Path

# Access system-level functions and arguments
import sys

# Import necessary PyQt6 widgets
from PyQt6.QtWidgets import QWidget, QMessageBox

# Import uic for loading .ui files
from PyQt6 import uic

# Import the PostController class to manage user actions
from inkpotro.generator.content_generator import PostController

# Import datetime for default post date generation
from datetime import datetime

# Import GitHub API and auth manager
from github import Github, BadCredentialsException
from inkpotro.auth import Manager

# Import QFontDatabase for loading custom fonts dynamically
from PyQt6.QtGui import QFontDatabase, QFont

# Initialize token manager to load GitHub token
token_manager =  Manager()
token =  token_manager.load_token()

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

# Class representing the dashboard window
class DashboardWindow(QWidget):
    # Constructor to initialize the window
    def __init__(self):
        # Call parent class constructor
        super().__init__()

        # Get the full path to the UI file
        ui_path = resource_path("ui/dashboard.ui")

        # Load the UI file into this widget
        uic.loadUi(ui_path, self)

        # Create an instance of PostController
        self.controller = PostController(self)

        # Add input for post date with default to current time
        self.date_input.setText(datetime.now().strftime("%Y-%m-%dT%H:%M:%S+06:00"))

        # If a GitHub token is found
        if token:
            try:
                # Attempt to log in to GitHub using the token
                login = Github(token)

                # Retrieve the user object associated with the token
                user = login.get_user()

                # Get the user's name from the GitHub profile
                user_name = user.name
                
                # Add an input field for the author's name, pre-filled with GitHub Fullname
                self.author_input.setText(user_name)
            except BadCredentialsException:
                self.show_invalid_token_dialog()

        # Get the full path to the custom Bengali font (SolaimanLipi.ttf)
        font_path = resource_path("font/SolaimanLipi.ttf")

        # Attempt to load the font into the application font database
        font_id = QFontDatabase.addApplicationFont(str(font_path))

        # Get the font family name of the loaded font
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Create a QFont object with the loaded font family and set font size to 12
        app_font = QFont(font_family, 12)

        # Apply the font to the markdown editor
        self.editor_textedit.setFont(app_font)

        # Apply the same font to the preview browser for consistency
        self.preview_browser.setFont(app_font)
    
    # Method to show a critical error dialog when the GitHub token is invalid
    def show_invalid_token_dialog(self):
        # Create a QMessageBox attached to the current widget
        msg = QMessageBox(self)
        
        # Set the title of the dialog window
        msg.setWindowTitle("Invalid Token")
        
        # Set the message text shown in the dialog
        msg.setText("Your GitHub token is invalid. Please login again.")
        
        # Set the icon to indicate a critical error (red X)
        msg.setIcon(QMessageBox.Icon.Critical)
        
        # Set a single OK button in the message box
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Display the message box and wait for the user's response
        response = msg.exec()
        
        # If the user clicks OK
        if response == QMessageBox.StandardButton.Ok:
            # Import and open the AuthenticationWindow to allow re-login
            from inkpotro.controllers.authentication import AuthenticationWindow
            self.auth_window = AuthenticationWindow()
            self.auth_window.show()
            
            # Ensure this window is deleted from memory when closed
            from PyQt6.QtCore import Qt
            self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            
            # Close the current window
            self.close()