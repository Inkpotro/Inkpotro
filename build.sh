#!/bin/bash

# Get paths
CTK_PATH=$(uv run python3 -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))")
THEME_FILE=$(realpath inkpotro/theme/inksky.json)
ICON_FILE=$(realpath inkpotro/icon/icon.png)
MAIN_FILE=$(realpath inkpotro/__main__.py)

# Build using PyInstaller
uv run pyinstaller \
  --noconfirm \
  --onefile \
  --windowed \
  --icon="$ICON_FILE" \
  --add-data "$THEME_FILE:theme" \
  --add-data "$ICON_FILE:icon" \
  --add-data "${CTK_PATH}:customtkinter" \
  --hidden-import PIL._tkinter_finder \
  -n Inkpotro \
  "$MAIN_FILE"