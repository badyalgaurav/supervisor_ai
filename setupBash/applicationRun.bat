@echo off

rem Set the title of the CMD window
title Install and Run ReactJS Build

rem Redirect output to a log file
call npm install -g serve --save --force


rem Start the ReactJS build using serve
call npx serve -s . -l 20010 

pause