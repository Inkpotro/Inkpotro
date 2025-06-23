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
ICON_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/icon/icon.png'))")
AUTH_UI=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/ui/authentication.ui'))")
DASH_UI=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/ui/dashboard.ui'))")
FONT_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/font/SolaimanLipi.ttf'))")
MAIN_FILE=$(uv run $PYTHON_EXEC -c "import os; print(os.path.abspath('inkpotro/__main__.py'))")

# Run PyInstaller to build the executable
uv run pyinstaller \
  --noconfirm \
  --onefile \
  --windowed \
  --icon="$ICON_FILE" \
  --add-data "$AUTH_UI${SEP}ui" \
  --add-data "$DASH_UI${SEP}ui" \
  --add-data "$ICON_FILE${SEP}icon" \
  --add-data "$FONT_FILE${SEP}font" \
  -n Inkpotro \
  "$MAIN_FILE"