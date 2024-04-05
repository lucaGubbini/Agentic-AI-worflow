@echo off
REM Activate the virtual environment
call "C:\Luca\AI\autogen\esperimenti\0.2 CrewAI\autogenVenv\Scripts\activate.bat"

REM Set the QUART_APP environment variable
set QUART_APP=app:app

REM Navigate to the directory of your Quart app
cd "C:\Luca\AI\autogen\esperimenti\0.2 CrewAI"

REM Run the Quart server with Hypercorn
call hypercorn %QUART_APP% --reload

REM Pause command to prevent the command window from closing immediately after running
pause
