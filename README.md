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

`\`\`python
python ids_windows_log.py
\`\`\`

To test it, run a brute-force attack from Kali using Hydra:

\`\`\`bash
hydra -l administrator -P /usr/share/wordlists/rockyou.txt ssh://<target-ip>
\`\`\`

**ids_log_file_monitor.py** — Point it at any log file that produces lines in the 
format: `IP | event_id | HH:MM:SS | port | True/False`

\`\`\`python
python ids_log_file_monitor.py
\`\`\`

## Lab setup

- **Attacker**: Kali Linux (Hydra for brute-force simulation)
- **Target**: Windows 10/11 with OpenSSH server enabled
- **Detection threshold**: 5 failed attempts from same IP triggers HIGH alert

## Requirements

- Python 3.x
- Windows with OpenSSH/Operational event log enabled
- PowerShell (for ids_windows_log.py)

## License

GPL-3.0
