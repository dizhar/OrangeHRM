@echo off
setlocal EnableDelayedExpansion

:: Exit on any error
set "ERRORLEVEL="

:: Define paths
set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "ALLURE_REPORT_DIR=reports\allure-results"

:: Check for required commands
for %%C in (python pip pytest) do (
    where %%C >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        echo Error: %%C is not installed.
        exit /b 1
    )
)

:: Create and activate virtual environment
if not exist "%VENV_DIR%" (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv "%VENV_DIR%"
    
    :: Activate virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"
    
    :: Install dependencies
    if exist "%REQUIREMENTS_FILE%" (
        echo Installing dependencies from %REQUIREMENTS_FILE%...
        pip install -r "%REQUIREMENTS_FILE%"
    ) else (
        echo Error: %REQUIREMENTS_FILE% not found.
        exit /b 1
    )
) else (
    :: Activate virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"
)

:: Run tests with pytest and generate Allure results
echo Running tests...
pytest --alluredir="%ALLURE_REPORT_DIR%" -v -s
if !ERRORLEVEL! neq 0 (
    echo Tests failed.
    exit /b 1
)

:: Serve Allure report
echo Tests completed. Serving Allure report...
if exist "serve_allure_report.bat" (
    call serve_allure_report.bat
) else (
    echo Error: serve_allure_report.bat not found.
    exit /b 1
)

endlocal