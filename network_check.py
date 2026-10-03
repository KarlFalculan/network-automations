"""network_check.py - read devices from inventory.json, check if each is UP or DOWN,
show the results, and save them to output.json."""

import json
import socket
from datetime import datetime

INVENTORY_FILE = "inventory.json"
OUTPUT_FILE = "output.json"


def load_inventory(filename):
    """Read the device list from a JSON file (with error handling)."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data["devices"]
    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
    except KeyError:
        print(f"Error: {filename} has no 'devices' list.")
    return []


def check_real(device):
    """Really test the device by opening a TCP connection to its port."""
    try:
        with socket.create_connection((device["ip_address"], device["port"]), timeout=5):
            return "UP"
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
        return "DOWN"


def check_device(device):
    """Return UP or DOWN. Real devices are tested; others are simulated."""
    try:
        if device.get("mode") == "real":
            return check_real(device)
        return device.get("simulated_status", "DOWN").upper()
    except Exception as error:  # basic safety net so one bad device never stops the program
        print(f"  Could not check {device.get('hostname', 'unknown')}: {error}")
        return "DOWN"


def save_results(results, filename):
    """Write the results to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(results, file, indent=2)
        print(f"\nResults saved to {filename}")
    except OSError as error:
        print(f"Error: could not save {filename} ({error})")


def main():
    devices = load_inventory(INVENTORY_FILE)
    if not devices:
        print("No devices to check. Stopping.")
        return

    print("=" * 60)
    print("NETWORK STATUS CHECK")
    print("=" * 60)

    results = []
    for device in devices:
        status = check_device(device)
        print(f"{device['hostname']:<18} {device['ip_address']:<34} {status}")
        results.append({
            "hostname": device["hostname"],
            "ip_address": device["ip_address"],
            "device_type": device["device_type"],
            "location": device["location"],
            "status": status,
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    up_count = sum(1 for r in results if r["status"] == "UP")
    print("-" * 60)
    print(f"Summary: {up_count} UP, {len(results) - up_count} DOWN, {len(results)} total")

    save_results(results, OUTPUT_FILE)


if __name__ == "__main__":
    main()