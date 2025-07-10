#!/bin/bash

# Exit on any error
set -e

REPORTS_DIR="reports"
ALLURE_RESULTS_DIR="$REPORTS_DIR/allure-results"
HTML_REPORT="$REPORTS_DIR/report.html"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Create necessary directories
mkdir -p "$REPORTS_DIR/screenshots" "$REPORTS_DIR/logs"

# Check if Allure is installed
if command_exists allure; then
    echo "Serving Allure report from $ALLURE_RESULTS_DIR..."
    if [ -d "$ALLURE_RESULTS_DIR" ]; then
        allure serve "$ALLURE_RESULTS_DIR"
    else
        echo "Error: Allure results directory $ALLURE_RESULTS_DIR not found."
        exit 1
    fi
else
    echo "Allure not detected. Running tests with HTML reporting..."
    if command_exists pytest; then
        pytest -v -s --html="$HTML_REPORT" || {
            echo "Tests failed."
            exit 1
        }
    else
        echo "Error: pytest not installed."
        exit 1
    fi

    echo "Tests completed. HTML report generated at $HTML_REPORT"

    # Open HTML report if it exists
    if [ -f "$HTML_REPORT" ]; then
        case "$(uname)" in
            "Darwin"*)
                open "$HTML_REPORT"
                ;;
            "Linux"*)
                if command_exists xdg-open; then
                    xdg-open "$HTML_REPORT"
                elif command_exists sensible-browser; then
                    sensible-browser "$HTML_REPORT"
                else
                    echo "No browser opener found. Please open $HTML_REPORT manually."
                fi
                ;;
            MINGW*|MSYS*)
                start "$HTML_REPORT"
                ;;
            *)
                echo "Unsupported OS. Please open $HTML_REPORT manually."
                ;;
        esac
    else
        echo "Error: HTML report not generated at $HTML_REPORT."
        exit 1
    fi
fi