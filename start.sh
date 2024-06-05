#!/bin/bash

# Function to check if the script is run as root
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script must be run as root. Please use sudo."
        exit 1
    fi
}

# Function to run a command and handle errors
run_command() {
    echo "Running: $1"
    $1
    if [ $? -ne 0 ]; then
        echo "Error executing command: $1"
        exit 1
    fi
}

# Function to check if port 5000 is in use
check_port() {
    if ss -tuln | grep ':5000' > /dev/null; then
        echo "******************************************************"
        echo "*** Agent started and running on port 5000 ***"
        echo "******************************************************"
    else
        echo "Error: Agent is not running on port 5000."
        exit 1
    fi
}

# Check if the script is run as root
check_root

# Update apt packages
run_command "apt update"

# Install Python, pip, net-tools, and screen
run_command "apt install -y python3 python3-venv python3-pip net-tools screen"

# Get the working directory
echo "Getting the working directory..."
WORKING_DIRECTORY=$(pwd)
echo "Working directory: $WORKING_DIRECTORY"

# Set up Python virtual environment
VENV_DIR="$WORKING_DIRECTORY/venv"
echo "Setting up Python virtual environment in $VENV_DIR..."
run_command "python3 -m venv $VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$WORKING_DIRECTORY/requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    run_command "pip install -r $WORKING_DIRECTORY/requirements.txt"
else
    echo "requirements.txt not found. Skipping installation of requirements."
fi

# Run the main app in a new screen session
SCREEN_SESSION_NAME="agentapp"
echo "Running the main app in a new screen session ($SCREEN_SESSION_NAME)..."
screen -dmS $SCREEN_SESSION_NAME bash -c "source $VENV_DIR/bin/activate && python3 $WORKING_DIRECTORY/agent.py"

# Give the agent some time to start
sleep 5

# Check if the agent started and is running on port 5000
echo "Checking if the agent started on port 5000..."
if ! check_port; then
    echo "Error: Agent did not start properly."
    echo "To reattach to the screen session, use: screen -r $SCREEN_SESSION_NAME"
    exit 1
fi

echo "******************************************************"
echo "*** Agent started and running on port 5000 ***"
echo "******************************************************"
echo "To reattach to the screen session, use: screen -r $SCREEN_SESSION_NAME"
