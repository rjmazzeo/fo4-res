# Fallout 4 Resolution Updater

A Windows executable that automatically detects your current screen resolution and updates your Fallout 4 INI file with that resolution.

## Features

- Automatically detects your primary monitor's resolution
- Updates `iSize H` and `iSize W` in Fallout 4's INI file
- Works with both `Fallout4Prefs.ini` and `Fallout4.ini`
- Simple one-click operation

## Building the Executable

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Building from Windows

1. Open a command prompt in this directory
2. Run the build script:
   ```
   build_exe.bat
   ```

   Or manually:
   ```
   pip install pyinstaller
   pyinstaller --onefile --name "UpdateFallout4Resolution" update_fallout4_resolution.py
   ```


## Usage

1. Run `UpdateFallout4Resolution.exe`
2. The program will:
   - Detect your current screen resolution
   - Find your Fallout 4 INI file (in `Documents/My Games/Fallout4/`)
   - Update the resolution settings
   - Display a success message

## INI File Location

The program looks for Fallout 4 INI files in:
- `Documents/My Games/Fallout4/Fallout4Prefs.ini` (preferred)
- `Documents/My Games/Fallout4/Fallout4.ini` (fallback)

## What Gets Updated

The program updates the following settings in the `[Display]` section:
- `iSize H` = Your screen height
- `iSize W` = Your screen width

## Notes

- The program will create a `[Display]` section if it doesn't exist
- Existing resolution values will be overwritten
- The INI file is backed up automatically by Windows (if file history is enabled)

