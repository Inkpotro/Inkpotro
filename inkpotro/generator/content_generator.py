# Import necessary PyQt6 widgets and classes
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon

# Import custom MarkdownService for saving posts
from inkpotro.services import MarkdownService

# Import Path from pathlib to handle filesystem paths
from pathlib import Path

# Access system-level functions and arguments
import sys

# Helper to resolve resource paths in dev and bundled mode
def resource_path(relative_path):
    # Check if the application is running in a bundled (frozen) environment like PyInstaller
    if getattr(sys, 'frozen', False):
        # If frozen, use the temporary folder created by PyInstaller
        icon_path = Path(sys._MEIPASS)
    else:
        # If not frozen, use the directory two levels up from the current file
        icon_path = Path(__file__).resolve().parent.parent
    # Return the full path to the resource
    return icon_path / relative_path

# Controller class for handling blog post creation and preview
class PostController:
    # Initialize the controller with a reference to the UI
    def __init__(self, ui):
        # Store reference to the UI components
        self.ui = ui

        # Connect button/tab actions to methods
        self.connect_signals()

    # Connect UI signals (button clicks, tab changes) to methods
    def connect_signals(self):
        # When 'Save Locally' button is clicked, call save_markdown
        self.ui.save_locally_btn.clicked.connect(self.save_markdown)

        # When tab is changed, call handle_tab_change
        self.ui.tabs.currentChanged.connect(self.handle_tab_change)

    # Save markdown content to local file
    def save_markdown(self):
        try:
            # Get input values from UI
            title = self.ui.title_input.text().strip()
            author = self.ui.author_input.text().strip()
            date = self.ui.date_input.text().strip()
            tags = [tag.strip() for tag in self.ui.tags_input.text().split(",")]
            categories = [cat.strip() for cat in self.ui.category_input.text().split(",")]
            draft = self.ui.draft_checkbox.isChecked()
            content = self.ui.editor_textedit.toPlainText().strip()

            # Prepare data dictionary to pass to MarkdownService
            markdown_data = {
                "title": title,
                "author": author,
                "date": date,
                "tags": tags,
                "categories": categories,
                "draft": draft,
                "content": content
            }

            # Create a folder selection dialog (not native to allow icon setting)
            dialog = QFileDialog(self.ui, "Select Folder to Save Post")
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            icon_path = resource_path("icon/icon.png")
            dialog.setWindowIcon(QIcon(str(icon_path)))

            # If the user selects a folder
            if dialog.exec():
                # Get selected folder path
                folder = dialog.selectedFiles()[0]

                # Save the markdown file using the MarkdownService
                MarkdownService.save_post(markdown_data, folder)

                # Show success message
                QMessageBox.information(
                    self.ui,
                    "Success",
                    f"Post saved as {title}.md!"
                )
        except Exception as e:
            # Show error message if something goes wrong
            QMessageBox.critical(
                self.ui,
                "Error",
                f"Failed to save post:\n{str(e)}"
            )

    # Called when the tab is changed in the UI
    def handle_tab_change(self, index):
        # Get the name/text of the selected tab
        tab_text = self.ui.tabs.tabText(index)
        
        # If the 'Preview' tab is selected, update the preview
        if tab_text == "Preview":
            self.update_preview()

    # Render a live preview of the markdown content as HTML
    def update_preview(self):
        # Import markdown converter
        from markdown import markdown

        # Get raw markdown text from the editor
        content = self.ui.editor_textedit.toPlainText().strip()

        # Convert markdown to HTML with code and table support
        html = markdown(content, extensions=["fenced_code", "codehilite", "tables"])

        # Display the rendered HTML in the preview browser
        self.ui.preview_browser.setHtml(html)