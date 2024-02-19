@REM @echo off
@REM rem Set the title of the CMD window
@REM title Superai FASTAPI
@REM echo Installing packages...

@REM rem Get the full path to the directory of the batch script
@REM set "script_dir=%~dp0"

@REM rem Create a new environment 
@REM call python -m venv SuperAIEnv


@REM rem Activate the virtual environment
@REM call "%script_dir%\SuperAIEnv\Scripts\activate"

@REM rem Going to the root directory of superai 
@REM cd ..
@REM cd LearningFastAPI

@REM call pip install -r requirements.txt
@REM echo Virtual environment activated.

@REM echo Starting uvicorn server...
@REM cd
@REM echo Current working directory: %cd%

@REM rem Start the uvicorn server
@REM call uvicorn main:app --host 0.0.0.0 --port 8000

@REM echo uvicorn server started.





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

cd ..
cd LearningFastAPI

call pip install -r requirements.txt
echo Virtual environment activated.


echo Starting uvicorn server...

rem Start the uvicorn server in a separate process
@REM start "uvicorn_server" cmd /c "uvicorn main:app --host 0.0.0.0 --port 8000"

uvicorn main:app --host 0.0.0.0 --port 8000

echo uvicorn server started.

@REM pause
