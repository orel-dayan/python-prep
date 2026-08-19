import platform
import subprocess


def ping_host(host: str, count: int = 4) -> subprocess.CompletedProcess[str]:
    """Ping a host using the correct parameter for the current OS."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, str(count), host]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def check_service_status(service: str) -> tuple[bool, str]:
    """Check if a service is running, in a portable way."""
    if platform.system().lower() == "windows":
        command = ["sc", "query", service]
    else:
        command = ["systemctl", "is-active", service]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return False, f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"


if __name__ == "__main__":
    ping_result = ping_host("8.8.8.8")
    print(ping_result.stdout or ping_result.stderr)

    service_ok, service_output = check_service_status("nginx")
    print(f"Service running: {service_ok}")
    print(service_output)