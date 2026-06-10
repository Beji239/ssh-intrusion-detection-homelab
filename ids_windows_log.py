import subprocess
import time

ssh_attempts = {} # Key = IP string, Value = int count

def check_ssh_login(ip_address, port, success):
    if port!= 22:
        return "INFO: Not SSH"
    
    if success:
        ssh_attempts[ip_address] = 0
        return f"INFO: SSH Login OK from {ip_address}"
    
    if ip_address not in ssh_attempts:
        ssh_attempts[ip_address] = 1
    else:
        ssh_attempts[ip_address] += 1
        
    if ssh_attempts[ip_address] > 5:
        return f"HIGH: SSH Brute-Force from {ip_address} - {ssh_attempts[ip_address]} fails"
    else: 
        return f"INFO: SSH fail count {ssh_attempts[ip_address]} from {ip_address}"

def tail_event_log():
    print("\n=== LIVE IDS STARTED ===")
    print("Monitoring OpenSSH/Operational log for failed logins...")
    print("Attack this machine from Kali with hydra. Press Ctrl+C to stop\n")
    
    # NEW: Query OpenSSH/Operational log for failed password events
    ps_cmd = '''
    $events = Get-WinEvent -FilterHashtable @{LogName='OpenSSH/Operational'; ID=4} -MaxEvents 20 -ErrorAction SilentlyContinue | Where-Object {$_.Message -match 'Failed password'}
    foreach ($e in $events) { 
        $ip = if ($e.Message -match 'from (\d+\.\d+\.\d+\.\d+)') { $matches[1] } else { 'unknown' }
        $e.TimeCreated.ToString('HH:mm:ss'), $ip 
    }
    '''
    
    seen_events = set()
    while True:
        try:
            result = subprocess.run(["powershell", "-Command", ps_cmd], 
                                    capture_output=True, text=True)
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for i in range(0, len(lines), 2):
                    if i+1 < len(lines):
                        event_time = lines[i].strip()
                        attacker_ip = lines[i+1].strip()
                        event_id = f"{event_time}-{attacker_ip}"
                        
                        if event_id not in seen_events and attacker_ip!= 'unknown' and attacker_ip!= '-':
                            seen_events.add(event_id)
                            alert = check_ssh_login(attacker_ip, 22, False)
                            print(f"[{event_time}] {alert}")
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print(f"\nIDS shutting down. Final counts: {ssh_attempts}")
            break

if __name__ == "__main__":
    tail_event_log()
            












































