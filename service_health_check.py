import socket
import time
import sys
from datetime import datetime

SERVICES = {
    "Localhost HTTP": ("127.0.0.1", 80),
    "Localhost HTTPS": ("127.0.0.1", 443),
}

TIMEOUT_SECONDS = 3
REPORT_FILE = "service_health_report.txt"


def check_service(name, host, port):
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT_SECONDS):
            latency = round((time.time() - start) * 1000, 2)
            return True, latency
    except Exception:
        return False, None


def main():
    failures = 0

    with open(REPORT_FILE, "w") as report:
        report.write("SERVICE HEALTH REPORT\n")
        report.write("=====================\n")
        report.write(f"Run time: {datetime.now()}\n\n")

        for name, (host, port) in SERVICES.items():
            healthy, latency = check_service(name, host, port)
            if healthy:
                report.write(f"[OK] {name} - {latency} ms\n")
                print(f"✅ {name} healthy ({latency} ms)")
            else:
                report.write(f"[FAIL] {name} unreachable\n")
                print(f"❌ {name} unreachable")
                failures += 1

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

