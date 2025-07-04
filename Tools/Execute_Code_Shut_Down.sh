#! /bin/bash

# Set the target time in HH:MM format
TARGET_TIME="6:57"

# Function to get the current time in HH:MM format
current_time() {
    echo $(date +"%H:%M")
}

# Loop until the current time matches the target time
while [ "$(current_time)" != "$TARGET_TIME" ]; do
    echo "Current time: $(current_time). Waiting until $TARGET_TIME..."
    sleep 30  # Check every 30 seconds
done

# open folder and run python script
cd /Users/n02-19/Desktop/Night_Water/
/usr/local/bin/python3.11 ./oneclick.py

echo "Script executed at $(current_time)"

# Shut down the Mac
sudo shutdown -h now

