
#!/bin/bash

echo "Initializing Ascend AI Environment..."

# Update and install system packages
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install necessary dependencies
echo "Installing dependencies..."
sudo apt-get install -y docker.io docker-compose python3 python3-pip

# Install Python dependencies from requirements.txt
echo "Installing Python libraries..."
pip3 install -r /mnt/data/requirements.txt

# Set up Docker environment
echo "Setting up Docker..."
sudo systemctl enable docker
sudo systemctl start docker

# Load environment variables (if any)
echo "Loading environment variables..."
if [ -f /mnt/data/env_variables ]; then
    export $(cat /mnt/data/env_variables | xargs)
else
    echo "No environment variables found."
fi

# Build Docker containers if docker-compose file is present
if [ -f /mnt/data/extracted_archive/docker-compose.yml ]; then
    echo "Building Docker containers..."
    sudo docker-compose -f /mnt/data/extracted_archive/docker-compose.yml up -d
else
    echo "No docker-compose.yml found. Skipping Docker build."
fi

echo "Ascend AI Environment Initialized."
