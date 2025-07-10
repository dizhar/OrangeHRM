@echo off
setlocal EnableDelayedExpansion

:: Define paths
set "REPORTS_DIR=reports"
set "ALLURE_RESULTS_DIR=%REPORTS_DIR%\allure-results"
set "HTML_REPORT=%REPORTS_DIR%\report.html"

:: Create necessary directories
if not exist "%REPORTS_DIR%\screenshots" mkdir "%REPORTS_DIR%\screenshots"
if not exist "%REPORTS_DIR%\logs" mkdir "%REPORTS_DIR%\logs"

:: Check if Allure is installed
where allure >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo Serving Allure report from %ALLURE_RESULTS_DIR%...
    if exist "%ALLURE_RESULTS_DIR%" (
        allure serve "%ALLURE_RESULTS_DIR%"
    ) else (
        echo Error: Allure results directory %ALLURE_RESULTS_DIR% not found.
        exit /b 1
    )
) else (
    echo Allure not detected. Running tests with HTML reporting...
    where pytest >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        pytest -v -s --html="%HTML_REPORT%"
        if !ERRORLEVEL! neq 0 (
            echo Tests failed.
            exit /b 1
        )
    ) else (
        echo Error: pytest not installed.
        exit /b 1
    )

    echo Tests completed. HTML report generated at %HTML_REPORT%

    :: Open HTML report if it exists
    if exist "%HTML_REPORT%" (
        start "" "%HTML_REPORT%"
    ) else (
        echo Error: HTML report not generated at %HTML_REPORT%.
        exit /b 1
    )
)

endlocal