
import os
import shutil
import sys
import platform

# Determine OS for system-specific installations
system = platform.system()

# Define paths
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
install_path = os.path.join(desktop_path, "AlphaSentinel")
exe_path = os.path.join(install_path, "AlphaSentinel.exe")

# Ensure necessary directories exist
os.makedirs(install_path, exist_ok=True)

# Create the desktop application launcher
def create_desktop_application():
    if system == "Windows":
        with open(os.path.join(install_path, "AlphaSentinel.bat"), "w") as f:
            f.write(f'@echo off\npython "{install_path}/AlphaSentinel_Main.py"\npause')

        # Create startup shortcut
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\Windows\Start Menu\Programs\Startup')
        shutil.copy(os.path.join(install_path, "AlphaSentinel.bat"), startup_path)

    elif system == "Darwin":  # macOS
        with open(os.path.join(install_path, "AlphaSentinel.command"), "w") as f:
            f.write(f'#!/bin/bash\npython3 "{install_path}/AlphaSentinel_Main.py"\nread -p "Press enter to continue"')

        os.system(f'chmod +x "{install_path}/AlphaSentinel.command"')

    print("✅ AlphaSentinel is now installed as a desktop application.")

# Copy core AI files to install directory
def copy_ai_files():
    ai_core_files = ["AlphaSentinel_Main.py", "Ascend_AI_Execution.py", "UI_Draggable_Bubble.py"]
    source_path = os.path.dirname(os.path.abspath(__file__))

    for file in ai_core_files:
        shutil.copy(os.path.join(source_path, file), install_path)

    print("✅ AI Core Files Installed.")

# Set AI to auto-launch on startup
def enable_auto_start():
    if system == "Windows":
        os.system(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v AlphaSentinel /t REG_SZ /d "{exe_path}" /f')
    elif system == "Darwin":
        os.system(f'osascript -e 'tell application "System Events" to make login item at end with properties {{name: "AlphaSentinel", path: "{exe_path}", hidden:false}}'' )

    print("✅ AI is set to launch on startup.")

# Run installation
if __name__ == "__main__":
    copy_ai_files()
    create_desktop_application()
    enable_auto_start()
    print("🚀 AlphaSentinel is now installed, persistent, and ready for execution.")
