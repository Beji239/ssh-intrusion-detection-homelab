import time
import os

# --- CONFIGURATION ---
LOG_FILE = "powershell_logs.txt"

# --- TOOLS ---
def check_ssh_login(attacker_ip, port, success):
    # Logic: Alert if login failed on port 22
    return not success and port == 22

def send_discord_alert(attacker_ip, event_time):
    # Placeholder for your Discord Webhook
    print(f" [DISCORD_WEBHOOK] Sending alert for {attacker_ip}")

def tail_event_log(filename):
    if not os.path.exists(filename):
        # Create the file if it doesn't exist so the script doesn't crash
        open(filename, 'a').close()

    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line.strip()

# --- MAIN ENGINE ---
def run_monitor():
    ssh_attempts = 0
    seen_events = set()

    print(f"--- Monitoring {LOG_FILE} ---")

    try:
        # We "loop" over the generator
        for log_entry in tail_event_log(LOG_FILE):
            # This is where you parse the string into variables
            # Example: "192.168.1.50 | log_123 | 12:00:01 | 22 | False"
            parts = log_entry.split(" | ")
            if len(parts) < 5: continue

            attacker_ip, event_id, event_time, port, success = parts
            port = int(port)
            success = success.lower() == 'true'

            if attacker_ip != 'unknown' and event_id not in seen_events:
                if check_ssh_login(attacker_ip, port, success):
                    ssh_attempts += 1
                    send_discord_alert(attacker_ip, event_time)
                    print(f"[{event_time}] ALERT: {attacker_ip} (Attempt {ssh_attempts})")
                    time.sleep(2) # Throttle alerts

                seen_events.add(event_id)

    except KeyboardInterrupt:
        print(f"\n\n{'='*30}")
        print("IDS shutting down.")
