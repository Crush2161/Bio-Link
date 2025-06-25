@echo off
echo BioLink Protector Bot Setup and Starter
echo =====================================
echo.

echo Running setup script...
python setup_env.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Python script failed to execute.
    echo Please make sure Python is installed and in your PATH.
    echo.
    pause
    exit /b 1
)

pause
