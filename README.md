A real-time SSH brute-force detection tool built in Python, developed and tested 
in a personal home lab running Kali Linux (attacker) and Windows (target).

## What it does

Monitors failed SSH login attempts on a Windows machine and raises alerts when 
brute-force patterns are detected. Tracks per-IP failure counts, filters duplicate 
events, so you're not spammed, and triggers an instant alert the moment a new attack 
is identified.

## Files

| File | Description |
|------|-------------|
| `ids_windows_log.py` | Queries the Windows OpenSSH/Operational event log in real-time via PowerShell. Detects failed logins, tracks per-IP attempt counts, and flags brute-force when an IP exceeds 5 failures. |
| `ids_log_file_monitor.py` | File-tailing version. Monitors a flat log file for incoming events, deduplicates by event ID, and includes a Discord webhook alert stub. |

## How to use

**ids_windows_log.py** — Run on a Windows machine with OpenSSH server installed.
Requires Python 3 and PowerShell access. No additional packages needed.
