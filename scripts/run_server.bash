#!/bin/bash
# Activate the virtual environment
source ../autogenVenv/bin/activate

# Set the QUART_APP environment variable
export QUART_APP=app:app

# Navigate to the directory of your Quart app
# This assumes that the script is run from the 'scripts' directory
cd ..

# Run the Quart server with Hypercorn
hypercorn $QUART_APP --reload

# You don't typically need a 'pause' command in Unix systems.
# The terminal window will remain open.
#chmod +x scripts/run_server.sh
#./scripts/run_server.sh