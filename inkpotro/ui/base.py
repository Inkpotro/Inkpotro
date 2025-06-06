# Import CustomTkinter base class and appearance functions
from customtkinter import (
    CTk,
    set_appearance_mode,
    set_default_color_theme
)

# For accessing package resource files
from importlib.resources import files

# Importing local resource packages (theme & icon)
from inkpotro import theme, icon

# Standard Tkinter image class for window icons
from tkinter import PhotoImage

# Get the full path to the custom theme JSON file
theme_path = files(theme).joinpath("inksky.json")

# Get the full path to the icon image file
icon_path = files(icon).joinpath("icon.png")

# Set global appearance mode: "light", "dark", or "system"
set_appearance_mode("light")

# Set the default color theme from the JSON theme file
set_default_color_theme(str(theme_path))

# Define a window class to encapsulate the main window logic
class Window:
    def __init__(self, title="Inkpotro", geometry="600x300"):
        # Create the main CustomTkinter window
        self.window = CTk()

        # Set the window title
        self.window.title(title)

        # Set the window size (width x height)
        self.window.geometry(geometry)

        # Load the icon image
        get_icon = PhotoImage(file=str(icon_path))

        # Set the window icon
        self.window.iconphoto(True, get_icon)
        
    def show_window(self):
        # Start the GUI event loop
        self.window.mainloop()