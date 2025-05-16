@echo off
echo [BOOT] Launching Ascend Matrix Environment...

:: Activate Conda environment (must be in PATH)
call conda activate ascendenv

:: Run the Neo boot sequence using Git Bash or WSL
:: Try Git Bash first
where bash >nul 2>nul
if %errorlevel%==0 (
    bash bootstrap/Neo.sh
) else (
    echo [ERROR] Bash not found. Install Git Bash or WSL.
    pause
    exit /b 1
)

pause
