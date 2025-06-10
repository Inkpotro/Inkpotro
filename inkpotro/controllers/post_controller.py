# Import file dialog for selecting folder paths
from customtkinter import filedialog

# Import custom message box for displaying success or error messages
from CTkMessagebox import CTkMessagebox

# Import Markdown service responsible for saving post data
from inkpotro.services import MarkdownService

# Controller class that handles user interactions in the dashboard
class PostController:
    def __init__(self, ui):
        # Store reference to the UI elements
        self.ui = ui
    
    # Display the metadata input form and hide the compose form
    def show_metadata(self):
        self.ui.compose_frame.pack_forget()
        self.ui.metadata_frame.pack(fill="both", expand=True)
    
    # Display the compose form and hide the metadata input form
    def show_compose(self):
        self.ui.metadata_frame.pack_forget()
        self.ui.compose_frame.pack(fill="both", expand=True)
    
    # Save the blog post as a markdown file locally
    def save_markdown(self):
        try:
            # Retrieve metadata and content from UI inputs
            cover_image = self.ui.cover_image_entry.get()
            cover_alt = self.ui.cover_alt_entry.get()
            title = self.ui.title_entry.get()
            author = self.ui.author_entry.get()
            date = self.ui.date_entry.get()

            # Convert comma-separated strings to lists
            tags = [tag.strip() for tag in self.ui.tags_entry.get().split(",")]
            categories = [cat.strip() for cat in self.ui.categories_entry.get().split(",")]

            # Get the draft checkbox status (True/False)
            draft = self.ui.draft_var.get()

            # Get the actual post content from the text box
            content = self.ui.content_text.get("1.0", "end").strip()

            # Create a dictionary with all post data
            markdown_data = {
                "cover_image": cover_image,
                "cover_alt": cover_alt,
                "title": title,
                "author": author,
                "date": date,
                "tags": tags,
                "categories": categories,
                "draft": draft,
                "content": content
            }

            # Ask user to choose a folder where the markdown file will be saved
            folder = filedialog.askdirectory(title="Select folder")

            # If the user cancels the dialog, do nothing
            if not folder:
                return

            # Call the service to save markdown data to a file in the selected folder
            MarkdownService.save_post(markdown_data, folder)

            # Show success message box if save was successful
            message_box = CTkMessagebox(
                title = "Success",
                message = f"Post saved as {title}.md!",
                icon = "check"
            )

        except Exception as e:
            # Show error message box if something goes wrong
            message_box = CTkMessagebox(
                title = "Error",
                message = f"{str(e)}",
                icon = "cancel"
            )