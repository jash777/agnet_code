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

# Check if the script is run as root
check_root

# Update apt packages
run_command "apt update"

# Install Python and pip
run_command "apt install -y python3 python3-pip"

# Get the working directory
echo "Getting the working directory..."
WORKING_DIRECTORY=$(pwd)
echo "Working directory: $WORKING_DIRECTORY"

# Install requirements
if [ -f "$WORKING_DIRECTORY/requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    run_command "pip3 install -r $WORKING_DIRECTORY/requirements.txt"
else
    echo "requirements.txt not found. Skipping installation of requirements."
fi

# Run the main app with sudo
echo "Running the main app with sudo..."
run_command "sudo python3 $WORKING_DIRECTORY/agent.py"
