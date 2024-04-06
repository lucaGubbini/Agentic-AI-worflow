@echo off
REM Starting Node.js server and Python Quart app from the scripts directory

REM Navigate to the parent directory where app.py and server.js are located
cd ..

REM Starting the Node.js server in a new command prompt window
echo Starting Node.js server...
start cmd /k "node server.js"

REM Activating the Python virtual environment
echo Activating Python virtual environment...
call .\autogenVenv\Scripts\activate.bat

REM Set the environment variable for the Quart app
set QUART_APP=app:app

REM Running the Quart app with Hypercorn in a new command prompt window
echo Starting Python Quart app...
start cmd /k "hypercorn %QUART_APP% --reload"

REM Pause command to prevent the command window from closing immediately after running (optional)
pause
