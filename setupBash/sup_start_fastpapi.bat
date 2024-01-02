@echo off
rem Set the title of the CMD window
title Supervisor
echo Activating virtual environment...

rem Get the full path to the directory of the batch script
set "script_dir=%~dp0"

rem Activate the virtual environment
call "%script_dir%\SuperAIEnv\Scripts\activate"

echo Virtual environment activated.

rem Change the current directory to your project directory
cd ..
cd LearningFastAPI

echo Starting uvicorn server...

rem Start the uvicorn server
call uvicorn main:app --host 0.0.0.0 --port 8000

echo uvicorn server started.
pause