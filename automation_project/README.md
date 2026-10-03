# Mini Network Automation Project

## Purpose

This project is a small Python tool that checks whether Cisco network devices are
**UP** or **DOWN**. It reads the devices from a JSON file, checks each one, shows the
result on the screen, and saves the results to another JSON file.

## Files

| File | What it does |
| --- | --- |
| `inventory.json` | List of devices (hostname, IP, type, location, port, check mode) |
| `network_check.py` | The program that checks each device |
| `output.json` | Results saved by the program (created when you run it) |
| `README.md` | This documentation |

## How it works

1. Reads `inventory.json`.
2. For each device:
   - `"mode": "real"` tries to open a TCP connection to the device's port. If it connects, the device is **UP**. If not, it is **DOWN**.
   - `"mode": "simulate"` uses the `simulated_status` value in the inventory for devices that are not reachable from the internet.
3. Prints the result for every device and a summary.
4. Saves everything to `output.json`.

## Requirements

- Python 3 (no extra libraries needed)

## Usage

```sh
python network_check.py
```

## Example output

```text
NETWORK STATUS CHECK
Cat8000-Sandbox    devnetsandboxiosxec8k.cisco.com    UP
R1-HQ              192.168.1.1                        UP
SW1-Floor2         192.168.1.2                        UP
R2-Branch          10.10.10.1                         DOWN
Summary: 3 UP, 1 DOWN, 4 total
```

## Error handling

- Missing or invalid `inventory.json` shows a clear message instead of crashing.
- Connection timeouts or DNS problems mark a device as DOWN.
- A problem with one device does not stop the others from being checked.

## Adding a device

Add a new block inside the `devices` list in `inventory.json` with the same fields.