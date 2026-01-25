#!/usr/bin/env python3
"""
Fallout 4 Resolution Updater
Gets the current screen resolution and updates Fallout 4 INI files.
"""

import os
import sys
import ctypes
import subprocess
from pathlib import Path

def get_screen_resolution():
    """Get the primary monitor's resolution."""
    try:
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
        height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
        return width, height
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
        return None, None

def find_fallout4_ini():
    """Find the Fallout 4 INI file in the user's Documents folder."""
    documents_path = Path(os.path.expanduser("~/Documents"))
    fallout4_path = documents_path / "My Games" / "Fallout4"
    
    # Try Fallout4Prefs.ini first (most common for resolution settings)
    prefs_ini = fallout4_path / "Fallout4Prefs.ini"
    if prefs_ini.exists():
        return prefs_ini
    
    # Fallback to Fallout4.ini
    main_ini = fallout4_path / "Fallout4.ini"
    if main_ini.exists():
        return main_ini
    
    return None

def launch_fallout4_via_steam():
    """Launch Fallout 4 via Steam using its app ID."""
    # Fallout 4 Steam App ID: 377160
    STEAM_APP_ID = "377160"
    steam_url = f"steam://run/{STEAM_APP_ID}"
    
    try:
        # Try os.startfile first (works on most Windows versions)
        os.startfile(steam_url)
        return True
    except AttributeError:
        # Fallback for systems where os.startfile doesn't support URL protocols
        try:
            # Use Windows 'start' command via subprocess (shell=False for security)
            subprocess.Popen(['cmd', '/c', 'start', '', steam_url], shell=False)
            return True
        except Exception as e:
            print(f"Error launching Fallout 4 via Steam: {e}")
            return False
    except Exception as e:
        print(f"Error launching Fallout 4 via Steam: {e}")
        return False

def update_ini_resolution(ini_path, width, height):
    """Update the resolution settings and window mode in the INI file."""
    try:
        # Read the INI file line by line to preserve comments and formatting
        with open(ini_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Track if we found the Display section and updated the values
        in_display_section = False
        updated_h = False
        updated_w = False
        updated_fullscreen = False
        updated_borderless = False
        
        # Process each line
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for section headers
            if stripped.startswith('[') and stripped.endswith(']'):
                section_name = stripped[1:-1]
                in_display_section = (section_name == 'Display')
                continue
            
            # Only process lines in the Display section
            if in_display_section and '=' in stripped:
                # Check for iSize H
                if stripped.startswith('iSize H') or stripped.startswith('iSizeH'):
                    # Extract the key part (before =)
                    key_part = stripped.split('=')[0].strip()
                    lines[i] = f"{key_part}={height}\n"
                    updated_h = True
                # Check for iSize W
                elif stripped.startswith('iSize W') or stripped.startswith('iSizeW'):
                    # Extract the key part (before =)
                    key_part = stripped.split('=')[0].strip()
                    lines[i] = f"{key_part}={width}\n"
                    updated_w = True
                # Check for bFull Screen
                elif stripped.startswith('bFull Screen') or stripped.startswith('bFullScreen'):
                    key_part = stripped.split('=')[0].strip()
                    lines[i] = f"{key_part}=0\n"  # 0 = windowed mode
                    updated_fullscreen = True
                # Check for bBorderless
                elif stripped.startswith('bBorderless'):
                    key_part = stripped.split('=')[0].strip()
                    lines[i] = f"{key_part}=1\n"  # 1 = borderless window
                    updated_borderless = True
        
        # If Display section doesn't exist or values weren't found, add them
        if not in_display_section or not updated_h or not updated_w or not updated_fullscreen or not updated_borderless:
            # Find where to insert the Display section (after [Display] if it exists, or at end)
            display_section_index = -1
            for i, line in enumerate(lines):
                if line.strip() == '[Display]':
                    display_section_index = i
                    break
            
            if display_section_index == -1:
                # Add Display section at the end
                lines.append('\n[Display]\n')
                display_section_index = len(lines) - 1
            
            # Add missing values after the [Display] header
            insert_index = display_section_index + 1
            if not updated_h:
                lines.insert(insert_index, f'iSize H={height}\n')
                insert_index += 1
            if not updated_w:
                lines.insert(insert_index, f'iSize W={width}\n')
                insert_index += 1
            if not updated_fullscreen:
                lines.insert(insert_index, f'bFull Screen=0\n')
                insert_index += 1
            if not updated_borderless:
                lines.insert(insert_index, f'bBorderless=1\n')
        
        # Write the updated content back
        with open(ini_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True
    except Exception as e:
        print(f"Error updating INI file: {e}")
        return False

def main():
    """Main function."""
    print("Fallout 4 Resolution Updater")
    print("=" * 40)
    
    # Get current resolution
    print("Getting current screen resolution...")
    width, height = get_screen_resolution()
    
    if width is None or height is None:
        print("Failed to get screen resolution!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"Current resolution: {width}x{height}")
    
    # Find INI file
    print("\nLooking for Fallout 4 INI file...")
    ini_path = find_fallout4_ini()
    
    if ini_path is None:
        print("ERROR: Could not find Fallout 4 INI file!")
        print("Expected location: Documents/My Games/Fallout4/Fallout4Prefs.ini")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"Found INI file: {ini_path}")
    
    # Update resolution and window mode
    print(f"\nUpdating resolution to {width}x{height}...")
    print("Setting windowed mode and borderless window...")
    if update_ini_resolution(ini_path, width, height):
        print("✓ Resolution updated successfully!")
        print("✓ Windowed mode and borderless window enabled!")
    else:
        print("✗ Failed to update settings!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Launch Fallout 4 via Steam
    print("\nLaunching Fallout 4 via Steam...")
    if launch_fallout4_via_steam():
        print("✓ Fallout 4 launch command sent to Steam!")
        print("\nDone! Fallout 4 should be starting now.")
        # Don't wait for input if launching the game
        sys.exit(0)
    else:
        print("✗ Failed to launch Fallout 4 via Steam!")
        print("Make sure Steam is installed and running.")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
