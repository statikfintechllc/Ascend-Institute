
#!/bin/bash

echo "Starting Ascend AI System..."

# Run the deployment script
echo "Running deployment script..."
bash /mnt/data/deploy_ascend.sh

# Start AI Task Agent
echo "Starting AI Task Agent..."
python3 /mnt/data/ai_task_agent.py &

# Launch the Dashboard
echo "Launching the Dashboard..."
bash /mnt/data/setup_dashboard.sh &

echo "Ascend AI System is now running."
