@echo off
echo [MATRIX] Initializing Ascend AI Sovereign Runtime...

:: Attempt to activate Conda environment (must be in PATH)
call conda activate ascendenv >nul 2>&1

:: --- Try Git Bash ---
where bash >nul 2>&1
if %errorlevel%==0 (
    echo [MATRIX] Git Bash detected. Executing Neo sequence...
    bash bootstrap/launch_devin.sh
    goto end
)

:: --- Try WSL as fallback ---
where wsl >nul 2>&1
if %errorlevel%==0 (
    echo [MATRIX] Git Bash not found. Trying WSL fallback...
    wsl bash bootstrap/launch_devin.sh
    goto end
)

:: --- No bash found ---
echo [ERROR] No compatible Bash environment found (Git Bash or WSL required).
echo [FIX] Install Git Bash from https://gitforwindows.org or enable WSL.
pause
exit /b 1

:end
pause