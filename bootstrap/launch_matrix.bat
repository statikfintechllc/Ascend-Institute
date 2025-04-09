@echo off
echo [BOOT] Launching Ascend Matrix Environment...

:: Activate Conda environment
call conda activate ascendenv

:: Run the Neo boot sequence
python bootstrap\Neo.sh

pause
