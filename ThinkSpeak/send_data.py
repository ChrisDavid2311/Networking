#!/usr/bin/env python3

import time
import subprocess
import urllib.parse
import urllib.request
from collections import deque

API_KEY = "G9ZGAIEWSMX67FGB"


# Keep the five most recent temperature readings in memory.
recent_temperatures = deque(maxlen=5)

def get_cpu_usage():
    def read_cpu_times():
        with open("/proc/stat", "r") as file:
            values = list(map(int, file.readline().split()[1:]))
        idle = values[3] + values[4]
        total = sum(values)
        return idle, total

    idle_before, total_before = read_cpu_times()
    time.sleep(1)
    idle_after, total_after = read_cpu_times()

    total_change = total_after - total_before
    idle_change = idle_after - idle_before

    return 100 * (1 - idle_change / total_change)

def get_cpu_temperature():
    result = subprocess.run(
        ["vcgencmd", "measure_temp"],
        capture_output=True,
        text=True,
        check=True
    )
    # Example output: temp=32.6'C
    return float(result.stdout.split("=")[1].split("'")[0])

while True:
    try:
        current_temp = get_cpu_temperature()
        cpu_usage = get_cpu_usage()
        recent_temperatures.append(current_temp)
        average_temp = sum(recent_temperatures) / len(recent_temperatures)

        print(f"Current: {current_temp:.1f}°C | Average: {average_temp:.1f}°C | CPU: {cpu_usage:.1f}%")

        data = urllib.parse.urlencode({
            "api_key": API_KEY,
            "field1": current_temp,
            "field2": average_temp,
	    "field3": cpu_usage

        }).encode("utf-8")

        request = urllib.request.Request(
            "https://api.thingspeak.com/update",
            data=data,
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            entry_id = response.read().decode("utf-8").strip()
            if entry_id == "0":
                print("ThingSpeak did not accept the update.")
            else:
                print(f"ThingSpeak update accepted (entry {entry_id}).")

    except Exception as error:
        print(f"Error: {error}")

    # ThingSpeak requires at least 15 seconds between channel updates.
    time.sleep(20)

