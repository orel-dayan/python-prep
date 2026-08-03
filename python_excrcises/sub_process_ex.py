import platform
import subprocess

def ping_host(host: str, count: int = 4) -> subprocess.CompletedProcess:
    # Determine the correct count flag based on OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    command = ["ping", param, str(count), host]
    
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=10
    )

# 1. Ping execution
res = ping_host("8.8.8.8")
print(res.stdout)
print(f"Return code: {res.returncode}")

# 2. Systemctl execution with complete exception handling
try:
    result = subprocess.run(
        ["systemctl", "status", "nginx"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)

except FileNotFoundError as e:
    # Triggered when the executable binary (e.g., systemctl) does not exist on the OS
    print(f"[ERROR] Binary not found on this OS: {e}")

except subprocess.CalledProcessError as e:
    # Triggered when check=True and returncode != 0
    print(f"[ERROR] Command executed but returned failure code {e.returncode}: {e.stderr}")

except subprocess.TimeoutExpired as e:
    # Triggered when execution exceeds timeout limit
    print(f"[ERROR] Command timed out: {e}")