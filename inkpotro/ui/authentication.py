# Import the custom base window class from the UI module
from inkpotro.ui import Window

# Import custom widgets from CustomTkinter
from customtkinter import (
    CTkEntry,
    CTkButton
)

# Import the Manager class for saving GitHub token
from inkpotro.auth import Manager

# Import messagebox from CTkMessagebox for user feedback
from CTkMessagebox import CTkMessagebox

# Class for handling GitHub token input and submission
class GetToken:
    def __init__(self):
        # Create a new window with title and size
        token_page = Window("GitHub Authentication - Inkpotro", "600x200")

        # Create a password-style entry for GitHub token input
        github_token = CTkEntry(
            token_page.window,
            show="*",
            placeholder_text="Example: ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            width=400
        )
        
        # Add spacing around the entry
        github_token.pack(padx=10, pady=50)

        # Function to handle token submission
        def submit_token():
            # Get token input and remove leading/trailing spaces
            token = github_token.get().strip()
            if token:
                # Create an instance of Manager class
                token_manager = Manager()

                # Save the token using Manager
                token_manager.save_token(token)

                # Show a confirmation messagebox
                message_box = CTkMessagebox(
                    title = "GitHub Authenticated - Inkpotro",
                    message = "GitHub Token saved successfully!",
                    icon = "check",
                    option_1="Close"
                )

                # Close the window if the user click "Close"
                if message_box.get() == "Close":
                    token_page.window.destroy()
        
        # Create the Save button
        save_button = CTkButton(token_page.window, text="Save Token", command=submit_token)

        # Add horizontal padding
        save_button.pack(padx=10)

        # Show the main window and start the event loop
        token_page.show_window()