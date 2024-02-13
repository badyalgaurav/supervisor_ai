@echo off
rem Set the title of the CMD window
title Superai FASTAPI
echo Creating virtual environment...

rem Get the full path to the directory of the batch script
set "script_dir=%~dp0"

rem Create a new environment 
call python -m venv SuperAIEnv


rem Activate the virtual environment
call "%script_dir%\SuperAIEnv\Scripts\activate"

call pip install -r super_requirements.txt
echo Virtual environment activated.

echo Starting uvicorn server...

rem Start the uvicorn server
call uvicorn main:app --host 0.0.0.0 --port 8000

echo uvicorn server started.

pause