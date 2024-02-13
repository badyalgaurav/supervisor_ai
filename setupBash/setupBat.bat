@echo off

rem Define variables
set GITBASH_INSTALLER=Git-2.42.0.2-64-bit.exe
set PYTHON_INSTALLER=python311.exe
set NODEJS_INSTALLER=node.exe
set NODEJS_MSI_INSTALLER=node.msi
set MONGODB_INSTALLER=mongodb.msi
set SuperAIEnv=SuperAIEnv
set SAIFrameworkEnv=SAIFrameworkEnv
set super_ai_requirement=super_ai_requirement.txt
set sai_framwork_requirement=sai_requirement.txt

@****************************************************************GITBASH********************************************
rem Install Python
echo Installing GITBASH...
%GITBASH_INSTALLER%
echo GITBASH installation completed.

@****************************************************************PYTHON********************************************
rem Install Python
echo Installing Python...
%PYTHON_INSTALLER%
echo Python installation completed.

@****************************************************************NODEJS********************************************
rem Install NODJS
echo Installing Node.js...
msiexec /i %NODEJS_MSI_INSTALLER%
echo Node.js installation completed.

@****************************************************************MONGODB********************************************
rem Install MONGODB

rem Install MONGODB using MSI installer
echo Installing MONGODB...
msiexec /i %MONGODB_INSTALLER%
echo MONGODB installation completed.

@****************************************************************super ai environment********************************************

rem Create a super ai environment
echo Creating virtual environment...
python -m venv %SuperAIEnv%
echo Virtual environment "%SuperAIEnv%" created.


@****************************************************************sai environment********************************************
rem Create a sai environment
python -m venv %SAIFrameworkEnv%
echo Virtual environment "%SAIFrameworkEnv%" created.

