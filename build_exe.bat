@echo off
echo Building Fallout 4 Resolution Updater...
echo.

REM Change to the directory where this batch file is located
REM Use pushd instead of cd to handle UNC/WSL paths better
pushd "%~dp0"

REM Verify we're in the correct directory and the Python file exists
if not exist "update_fallout4_resolution.py" (
    echo ERROR: Cannot find update_fallout4_resolution.py
    echo Current directory: %CD%
    echo Script directory: %~dp0
    popd
    pause
    exit /b 1
)

REM Display current directory for debugging
echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
python -m pip install pyinstaller

REM Build the executable
echo.
echo Building executable...
REM Use explicit paths to ensure PyInstaller runs from the correct directory
python -m PyInstaller --onefile --name "UpdateFallout4Resolution" --workpath "%CD%\build" --distpath "%CD%\dist" --specpath "%CD%" update_fallout4_resolution.py

echo.
echo Build complete! The executable is in the 'dist' folder.
popd
pause
