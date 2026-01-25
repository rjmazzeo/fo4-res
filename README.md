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

3. The executable will be created in the `dist` folder as `UpdateFallout4Resolution.exe`

### Building from WSL

1. Open a WSL terminal in this directory
2. Run the build script:
   ```bash
   ./build_exe.sh
   ```

   The script will automatically:
   - Detect Windows Python installation (if available)
   - Use Wine with Python (if Windows Python not found)
   - Install PyInstaller if needed
   - Build the Windows .exe

3. The executable will be created in the `dist` folder as `UpdateFallout4Resolution.exe`

**Note:** The WSL build script prefers using Windows Python directly (accessed via `/mnt/c/`), which produces native Windows executables. If Windows Python is not available, it will attempt to use Wine.

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

## Troubleshooting

### Line Ending Issues in WSL

If you encounter the error `bad interpreter: /bin/bash^M` when running `build_exe.sh` in WSL, this means the file has Windows line endings (CRLF) instead of Unix line endings (LF).

**Quick Fix:**

Run one of these commands in WSL to fix the line endings:

```bash
# Option 1: Using sed (built-in)
sed -i 's/\r$//' build_exe.sh

# Option 2: Using dos2unix (if installed)
dos2unix build_exe.sh

# Option 3: Using tr
tr -d '\r' < build_exe.sh > build_exe.sh.tmp && mv build_exe.sh.tmp build_exe.sh
```

After fixing, make sure the script is executable:
```bash
chmod +x build_exe.sh
```

**Prevention:**

The `.gitattributes` file in this repository ensures that shell scripts always use LF line endings when checked out from Git, preventing this issue in the future.
