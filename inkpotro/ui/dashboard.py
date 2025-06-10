# Import the Window class to create the main app window
from inkpotro.ui import Window

# Import the PostController class to manage user actions
from inkpotro.controllers import PostController

# Import necessary widgets from customtkinter
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkScrollableFrame,
    BooleanVar,
    CTkCheckBox,
    CTkTextbox
)

# Import a helper function to add CTkEntry inputs
from inkpotro.misc import add_entry

# Import GitHub API and auth manager
from github import Github, BadCredentialsException
from inkpotro.auth import Manager

# Import custom message box for displaying error messages
from CTkMessagebox import CTkMessagebox

# Import datetime for default post date generation
from datetime import datetime

# Initialize token manager to load GitHub token
token_manager =  Manager()
token =  token_manager.load_token()

# Define the Dashboard class which creates the UI
class Dashboard:
    def __init__(self):
        # Create the main application window
        dashboard = Window("Dashboard - Inkpotro", "1000x500")
        
        # Initialize the post controller with current UI
        self.controller = PostController(self)

        # Create the sidebar on the left for navigation
        sidebar = CTkFrame(dashboard.window, width=200)
        sidebar.pack(side="left", fill="y")

        # Add title label to the sidebar
        sidebar_title = CTkLabel(sidebar, text="Inkpotro", font=("Arial", 20, "bold"))
        sidebar_title.pack(pady=20)

        # Add button to switch to metadata form
        metadata = CTkButton(sidebar, text="Metadata", command=self.controller.show_metadata)
        metadata.pack(pady=10, fill="x", padx=10)

        # Add button to switch to the compose screen
        compose = CTkButton(sidebar, text="Compose", command=self.controller.show_compose)
        compose.pack(pady=10, fill="x", padx=10)

        # Create main content frame on the right
        self.main_frame = CTkFrame(dashboard.window)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Create a scrollable frame to hold metadata inputs
        self.metadata_frame = CTkScrollableFrame(self.main_frame, width=780, height=700)

        # Add input for cover image path
        self.cover_image_entry = add_entry(self.metadata_frame, "Cover Image Path")

        # Add input for cover image alt text
        self.cover_alt_entry = add_entry(self.metadata_frame, "Cover Alt Text")

        # Add input for the post title
        self.title_entry = add_entry(self.metadata_frame, "Title")

        # If a GitHub token is found
        if token:
            try:
                # Attempt to log in to GitHub using the token
                login = Github(token)

                # Retrieve the user object associated with the token
                user = login.get_user()

                # Get the user's name from the GitHub profile
                user_name = user.name

                # Add an input field for the author's name, pre-filled with GitHub username
                self.author_entry = add_entry(self.metadata_frame, "Author Name", user_name)
            except BadCredentialsException:
                # Show an error message if the GitHub token is invalid
                message_box = CTkMessagebox(
                    title = "Error",
                    message = "The GitHub token you are using is not valid. Please use a correct GitHub token.",
                    icon = "cancel",
                    option_1="Close"
                )
                # If the user clicks "Close", destroy the window and stop further execution
                if message_box.get() == "Close":
                    dashboard.window.destroy()

                    # Exit the constructor to avoid further UI operations
                    return
        
        # Add input for post date with default to current time
        self.date_entry = add_entry(
            self.metadata_frame,
            "Date (YYYY-MM-DDTHH:MM:SS+06:00)",
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S+06:00")
        )

        # Add input for tags
        self.tags_entry = add_entry(self.metadata_frame, "Tags (comma-separated)")

        # Add input for categories
        self.categories_entry = add_entry(self.metadata_frame, "Categories (comma-separated)")

        # Create a checkbox to mark post as draft
        self.draft_var = BooleanVar(value=False)
        is_draft = CTkCheckBox(self.metadata_frame, text="Draft", variable=self.draft_var)
        is_draft.pack(pady=(5, 15))

        # Add button to save the markdown post locally
        save_locally = CTkButton(self.metadata_frame, text="Save Locally", command=self.controller.save_markdown)
        save_locally.pack(pady=20)

        # Create compose frame to write post content
        self.compose_frame = CTkFrame(self.main_frame, width=780, height=700)

        # Add a text box for the post body/content
        self.content_text = CTkTextbox(self.compose_frame, height=500, font=("Arial", 15))
        self.content_text.pack(padx=20, pady=(10, 20), fill="x")

        # Show metadata form initially
        self.controller.show_metadata()

        # Display the window
        dashboard.show_window()