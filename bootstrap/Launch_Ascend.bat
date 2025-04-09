@echo off
echo [BOOT] Launching Ascend Matrix Environment...

:: Activate Conda environment (if available)
call conda activate ascendenv

:: Check for Bash support
where bash >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Bash detected. Running Neo.sh...
    bash bootstrap/Neo.sh
) else (
    echo [ERROR] Bash not found on system.
    echo Please install Git Bash or use WSL to run Neo.sh
    pause
    exit /b 1
)

pause
