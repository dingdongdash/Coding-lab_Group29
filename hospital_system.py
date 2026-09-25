#!/usr/bin/env python3
import random
import time
import sys
import os
import signal
from datetime import datetime

# Configurations
LOG_DIR = "active_logs"
PID_FILE = "/tmp/hospital_system.pid"

# Device Configuration - Increased Scale
DEVICES = {
    "heart": [f"WARD_A_HR_{i:02d}" for i in range(1, 6)],      # 5 Heart Rate Monitors
    "temp": [f"WARD_B_TEMP_{i:02d}" for i in range(1, 6)],    # 5 Temperature Sensors
    "water": ["FACILITY_WATER_MAIN", "ICU_WATER_RESERVE"]    # 2 Water Meters
}

LOGS = {
    "heart": os.path.join(LOG_DIR, "heart_rate_log.log"),
    "temp": os.path.join(LOG_DIR, "temperature_log.log"),
    "water": os.path.join(LOG_DIR, "water_usage_log.log")
}

def ensure_environment():
    """Ensure log directory and headers exist."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Define headers with units and attributes
    headers = {
        "heart": "Timestamp | Device_ID | Heart_Rate (BPM) | Status\n",
        "temp": "Timestamp | Device_ID | Temperature (Celsius) | Status\n",
        "water": "Timestamp | Device_ID | Usage (Liters/min) | Status\n"
    }
    
    for key, path in LOGS.items():
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            with open(path, "w") as f:
                f.write(headers[key])

def generate_data():
    """Main simulation loop with realistic hospital data ranges."""
    ensure_environment()
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Heart Rate (Realistic Range: 40 - 160 BPM)
        for device in DEVICES["heart"]:
            hr = random.randint(45, 150)
            status = "NORMAL"
            if hr < 60 or hr > 100: status = "CRITICAL" # Bradycardia or Tachycardia
            elif 90 <= hr <= 100: status = "WARNING"
            with open(LOGS["heart"], "a") as f:
                f.write(f"{timestamp} | {device} | {hr} | {status}\n")

        # 2. Temperature (Realistic Range: 34.0 - 41.0 Celsius)
        for device in DEVICES["temp"]:
            temp = round(random.uniform(34.5, 40.5), 1)
            status = "NORMAL"
            if temp > 38.0: status = "CRITICAL"  # High Fever
            elif temp < 35.5: status = "CRITICAL" # Hypothermia
            elif 37.5 <= temp <= 38.0: status = "WARNING"
            with open(LOGS["temp"], "a") as f:
                f.write(f"{timestamp} | {device} | {temp} | {status}\n")

        # 3. Water Usage (Realistic Range: 0 - 50 Liters/min)
        for device in DEVICES["water"]:
            usage = random.randint(5, 45)
            status = "NORMAL"
            if usage > 35: status = "HIGH_USAGE"
            with open(LOGS["water"], "a") as f:
                f.write(f"{timestamp} | {device} | {usage} | {status}\n")

        time.sleep(1) # Collect data every second
