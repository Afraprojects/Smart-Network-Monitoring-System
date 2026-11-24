
import subprocess
import re
import time
from datetime import datetime
from database import create_database, save_record, save_alert

devices = {
    "Google DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1",
    "Localhost": "127.0.0.1"
}

previous_status = {"Localhost": "OFFLINE"}


def check_device(name, ip_address):

    result = subprocess.run(
        ["ping", "-n", "4", "-w", "2000", ip_address],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    # Extract packet statistics
    match = re.search(
        r"Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+),\s*Lost\s*=\s*(\d+)",
        output
    )

    if match:
        packets_sent = int(match.group(1))
        packets_received = int(match.group(2))
        packets_lost = int(match.group(3))
    else:
        packets_sent = 4
        packets_received = 0
        packets_lost = 4

    # Calculate packet loss
    packet_loss = (
        (packets_lost / packets_sent) * 100
        if packets_sent > 0 else 0
    )

    # Determine device status
    if packets_received > 0:
        status = "ONLINE"
    else:
        status = "OFFLINE"

    # Extract average latency
    latency = None

    latency_match = re.search(
        r"Average\s*=\s*(<\s*)?(\d+(?:\.\d+)?)\s*ms",
        output
    )

    if latency_match:
        latency = float(latency_match.group(2))

        if latency_match.group(1):
            latency = 0.5

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nTime:", timestamp)
    print("Device:", name)
    print("IP:", ip_address)
    print("Status:", status)
    print("Latency:", latency if latency is not None else "No response")
    print("Packets Sent:", packets_sent)
    print("Packets Received:", packets_received)
    print("Packets Lost:", packets_lost)
    print("Packet Loss:", round(packet_loss, 2), "%")

    # Detect device status changes
    if name in previous_status:

        if previous_status[name] == "ONLINE" and status == "OFFLINE":

            message = "Network device went OFFLINE!"

            print("ALERT:", message)

            save_alert(
                name, ip_address, "OFFLINE", message, timestamp
            )

        elif previous_status[name] == "OFFLINE" and status == "ONLINE":

            message = "Network device RECOVERED!"

            print("ALERT:", message)

            save_alert(
                name, ip_address, "RECOVERED", message, timestamp
            )

    previous_status[name] = status

    # Save monitoring information
    save_record(
        name,
        ip_address,
        status,
        latency,
        timestamp,
        packets_sent,
        packets_received,
        packet_loss
    )


create_database()

try:

    print("SMART NETWORK MONITOR STARTED")

    while True:

        print("\n========== NETWORK CHECK ==========")

        for name, ip_address in devices.items():
            check_device(name, ip_address)

        print("\nNext check in 10 seconds...")
        time.sleep(10)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
