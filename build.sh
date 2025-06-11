#!/bin/bash

# Detect OS and set separator + python command
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    PYTHON_EXEC="python"
    SEP=";"  # Windows
else
    PYTHON_EXEC="python3"
    SEP=":"  # Linux/macOS
fi

# Use Python to resolve absolute paths
CTK_PATH=$(uv run $PYTHON_EXEC -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))")
THEME_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/theme/inksky.json'))")
ICON_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/icon/icon.png'))")
MAIN_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/__main__.py'))")

# Run PyInstaller to build the executable
uv run pyinstaller \
  --noconfirm \
  --onefile \
  --windowed \
  --icon="$ICON_FILE" \
  --add-data "$THEME_FILE${SEP}theme" \
  --add-data "$ICON_FILE${SEP}icon" \
  --add-data "$CTK_PATH${SEP}customtkinter" \
  --hidden-import PIL._tkinter_finder \
  -n Inkpotro \
  "$MAIN_FILE"