@echo off
@REM FOR ADMINISTRATION ACCESS
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:-------------------------------------- 

rem Define variables
set GITBASH_INSTALLER=Git-2.42.0.2-64-bit.exe
set PYTHON_INSTALLER=python311.exe
set NODEJS_INSTALLER=node.exe
set NODEJS_MSI_INSTALLER=node-v18.12.0-x64.msi
set MONGODB_INSTALLER=mongodb.msi
set SuperAIEnv=SuperAIEnv
set SAIFrameworkEnv=SAIFrameworkEnv
set super_ai_requirement=super_ai_requirement.txt
set sai_framwork_requirement=sai_requirement.txt

@REM @****************************************************************GITBASH********************************************
@REM rem Install Python
@REM echo Installing GITBASH...
@REM %GITBASH_INSTALLER%
@REM echo GITBASH installation completed.

@REM @****************************************************************PYTHON********************************************
rem Install Python
echo Installing Python...
%PYTHON_INSTALLER%
echo Python installation completed.

@REM @****************************************************************NODEJS********************************************
rem Install NODJS
echo Installing Node.js...
msiexec /i %NODEJS_MSI_INSTALLER%
echo Node.js installation completed.

@REM @****************************************************************MONGODB********************************************
rem Install MONGODB

rem Install MONGODB using MSI installer
echo Installing MONGODB...
msiexec /i %MONGODB_INSTALLER%
echo MONGODB installation completed.

@REM @****************************************************************super ai environment********************************************

rem Create a super ai environment
echo Creating virtual environment...
python -m venv %SuperAIEnv%
echo Virtual environment "%SuperAIEnv%" created.


@REM @****************************************************************sai environment********************************************
rem Create a sai environment
python -m venv %SAIFrameworkEnv%
echo Virtual environment "%SAIFrameworkEnv%" created.

echo SUCCESSFULLY INSTALLED ALL THE SETTINGS


@REM @****************************************************************Making applicatoins services********************************************
@REM echo APPLICATION SETTINGS  ARE GETTING READY 

@REM set "script_dir=%~dp0"
@REM echo %script_dir%

@REM call nssm install saiFastAPI "%script_dir%\sai_start_fastapi.bat"
@REM pause
@REM call nssm set saiFastAPI AppDirectory "%script_dir%"
@REM pause
@REM call nssm start saiFastAPI
@REM pause

@REM call nssm install supFastAPI %script_dir%\sup_start_fastapi.bat
@REM pause
@REM call nssm set supFastAPI AppDirectory "%script_dir%"
@REM pause
@REM call nssm start supFastAPI
@REM pause


@REM echo Initializing Application
@REM call "%script_dir%\applicationRun.bat" 

pause