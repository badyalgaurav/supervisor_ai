@echo off

rem Define variables
set PYTHON_INSTALLER=python311.exe
set NODEJS_INSTALLER=node.exe
set NODEJS_MSI_INSTALLER=node.msi
set SuperAIEnv=SuperAIEnv
set SAIFrameworkEnv=SAIFrameworkEnv
set super_ai_requirement=super_ai_requirement.txt
set sai_framwork_requirement=sai_requirement.txt

rem Check if Python is already installed
where python > nul 2>nul
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    rem Install Python
    echo Installing Python...
    %PYTHON_INSTALLER%
    if %errorlevel% neq 0 (
        echo Error installing Python. Press any key to exit.
        pause
        exit /b %errorlevel%
    )
    echo Python installation completed.
)

rem Check if Node.js is already installed
where node > nul 2>nul
if %errorlevel% equ 0 (
    echo Node.js is already installed.
) else (
    rem Check if Node.js MSI installer exists
    if exist %NODEJS_MSI_INSTALLER% (
        rem Install Node.js using MSI installer
        echo Installing Node.js...
        msiexec /i %NODEJS_MSI_INSTALLER%
        if %errorlevel% neq 0 (
            echo Error installing Node.js. Press any key to exit.
            pause
            exit /b %errorlevel%
        )
        echo Node.js installation completed.
    ) else (
        rem Install Node.js using executable installer
        echo Installing Node.js...
        %NODEJS_INSTALLER%
        if %errorlevel% neq 0 (
            echo Error installing Node.js. Press any key to exit.
            pause
            exit /b %errorlevel%
        )
        echo Node.js installation completed.
    )
)

rem Create a new virtual environment
echo Creating virtual environment...
python -m venv %SuperAIEnv%
echo Virtual environment "%SuperAIEnv%" created.
python -m venv %SAIFrameworkEnv%
echo Virtual environment "%SAIFrameworkEnv%" created.
if %errorlevel% neq 0 (
    echo Error creating virtual environment. Press any key to exit.
    pause
    exit /b %errorlevel%
)



rem Activate the virtual environment
echo Activating virtual environment...
call %SuperAIEnv%\Scripts\activate
if %errorlevel% neq 0 (
    echo Error activating virtual environment. Press any key to exit.
    pause
    exit /b %errorlevel%
)
echo Virtual environment "%SuperAIEnv%" activated.

call %SAIFrameworkEnv%\Scripts\activate
if %errorlevel% neq 0 (
    echo Error activating virtual environment. Press any key to exit.
    pause
    exit /b %errorlevel%
)
echo Virtual environment "%SAIFrameworkEnv%" activated.

rem Install packages from requirements.txt
echo Installing packages from requirements.txt...
pip install -r %REQUIREMENTS_FILE%
if %errorlevel% neq 0 (
    echo Error installing packages. Press any key to exit.
    pause
    exit /b %errorlevel%
)
echo Packages installation completed.




rem Change the current directory to your project directory
cd C:\Develop\ixplatformframework\FastPAPI

echo Starting uvicorn server...

rem Start the uvicorn server
call uvicorn main:app --host 0.0.0.0 --port 9005

echo uvicorn server started.

echo Press any key to exit.
pause
