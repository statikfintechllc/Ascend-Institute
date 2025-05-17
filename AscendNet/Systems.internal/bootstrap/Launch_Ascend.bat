@echo off
echo [BOOT] Launching Ascend Matrix Environment...

:: Attempt to activate Conda environment
call conda activate ascendenv

:: Step 1: Try Git Bash
where bash >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Git Bash detected.
    bash bootstrap/Neo.sh
    goto end
)

:: Step 2: Try WSL
where wsl >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Git Bash not found. Trying WSL...
    wsl bash bootstrap/Neo.sh
    goto end
)

:: Step 3: Fallback to PowerShell
where powershell >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] No Bash detected. Falling back to PowerShell...

    powershell -ExecutionPolicy Bypass -Command ^
        "$neo = Get-Content -Raw 'bootstrap/Neo.sh';" ^
        "$temp = '$env:TEMP\\neo_temp.ps1';" ^
        "$neo | Out-File -FilePath $temp -Encoding UTF8;" ^
        "& $temp; Remove-Item $temp"

    goto end
)

echo [ERROR] Could not find Bash, WSL, or PowerShell.
echo This system cannot run AscendAI with current configuration.
pause
exit /b 1

:end
pause