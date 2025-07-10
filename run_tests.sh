#!/bin/bash

# Exit on any error
set -e

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
ALLURE_REPORT_DIR="reports/allure-results"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
for cmd in python3 pip pytest; do
    if ! command_exists "$cmd"; then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install dependencies
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing dependencies from $REQUIREMENTS_FILE..."
        pip install -r "$REQUIREMENTS_FILE"
    else
        echo "Error: $REQUIREMENTS_FILE not found."
        exit 1
    fi
else
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
fi

# Run tests with pytest and generate Allure results
echo "Running tests..."
pytest --alluredir="$ALLURE_REPORT_DIR" -v -s || {
    echo "Tests failed."
    exit 1
}

# Serve Allure report
echo "Tests completed. Serving Allure report..."
if [ -f "serve_allure_report.sh" ]; then
    bash serve_allure_report.sh
else
    echo "Error: serve_allure_report.sh not found."
    exit 1
fi