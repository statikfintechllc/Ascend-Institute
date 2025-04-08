
#!/bin/bash

echo "Configuring Dashboard for Remote Access..."

# Ensure Dash and other necessary Python packages are installed
echo "Installing required Python packages..."
pip3 install dash flask requests

# Start the Dashboard
echo "Starting the Dashboard UI..."
python3 /mnt/data/dashboard.ui &

# Enable Remote Access using SSH Tunneling
echo "Setting up SSH Tunneling for Remote Access..."
echo "You can access the dashboard using: http://localhost:8050 via SSH Tunnel"

echo "Dashboard is now running."
