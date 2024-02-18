@echo off
rem Set the title of the CMD window
title Superai FASTAPI
echo Installing packages...

rem Get the full path to the directory of the batch script
set "script_dir=%~dp0"

rem Create a new environment 
call python -m venv SuperAIEnv


rem Activate the virtual environment
call "%script_dir%\SuperAIEnv\Scripts\activate"

rem Going to the root directory of superai 
cd ..
cd LearningFastAPI

call pip install -r requirements.txt
echo Virtual environment activated.

echo Starting uvicorn server...
cd
echo Current working directory: %cd%

rem Start the uvicorn server
call uvicorn main:app --host 0.0.0.0 --port 8000

echo uvicorn server started.

