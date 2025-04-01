import os
import time
import subprocess
from datetime import datetime, timedelta

# Get the greenhouse IDs from environment variables
GREENHOUSE_IDS = os.getenv("GREENHOUSE_IDS", "")
if not GREENHOUSE_IDS:
    print("? No GREENHOUSE_IDS found. Exiting...")
    exit(1)

print(f"? Scheduler started for GREENHOUSE_IDS: {GREENHOUSE_IDS}")

def get_next_run_time():
    """
    Calculates the next time the script should run (25 and 55 minutes past the hour).
    Handles day rollover correctly.
    """
    now = datetime.now()
    # Possible run times within an hour
    run_times = [25, 55]
    
    # Find the next run time
    for minute in run_times:
        candidate = now.replace(minute=minute, second=0, microsecond=0)
        if now < candidate:
            return candidate
    
    # If past 55, schedule for next hour 25
    next_hour = now.replace(hour=(now.hour + 1) % 24, minute=25, second=0, microsecond=0)
    if now.hour == 23:  # Midnight rollover
        next_hour = next_hour + timedelta(days=1)
    return next_hour

while True:
    # Get the next scheduled run time
    next_run_time = get_next_run_time()
    wait_time = (next_run_time - datetime.now()).total_seconds()
    
    # Ensure wait_time is non-negative
    if wait_time < 0:
        print(f"? Warning: Missed scheduled time {next_run_time.strftime('%H:%M')}. Recalculating...")
        continue
    
    print(f"? Waiting {wait_time:.2f} seconds until next prediction at {next_run_time.strftime('%H:%M')}")
    
    # Wait until the next scheduled time
    time.sleep(wait_time)
    
    # Run inference for each greenhouse ID
    greenhouse_ids = GREENHOUSE_IDS.split(",")
    for greenhouse_id in greenhouse_ids:
        print(f"?? Running inference for Greenhouse {greenhouse_id}...")
        subprocess.run(["python", "inference.py", greenhouse_id])
    
    print(f"? Predictions completed at {datetime.now().strftime('%H:%M')}")
