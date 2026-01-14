import requests
import sys
import os
from datetime import datetime

SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:8080")
EXPECTED_VERSION = os.getenv("EXPECTED_VERSION")

TIMEOUT = 5
REPORT_FILE = "post_deploy_report.txt"


def check_health():
    r = requests.get(f"{SERVICE_URL}/health", timeout=TIMEOUT)
    return r.status_code == 200


def check_version():
    if not EXPECTED_VERSION:
        print("❌ EXPECTED_VERSION not set")
        return False

    r = requests.get(f"{SERVICE_URL}/version", timeout=TIMEOUT)
    return r.text.strip() == EXPECTED_VERSION


def write_report(health_ok, version_ok):
    with open(REPORT_FILE, "w") as f:
        f.write("POST-DEPLOYMENT VERIFICATION REPORT\n")
        f.write("=================================\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Service URL: {SERVICE_URL}\n\n")
        f.write(f"Health check: {'OK' if health_ok else 'FAILED'}\n")
        f.write(f"Version check: {'OK' if version_ok else 'FAILED'}\n")


def main():
    try:
        health_ok = check_health()
        version_ok = check_version()
    except Exception as e:
        print(f"❌ Verification error: {e}")
        sys.exit(1)

    write_report(health_ok, version_ok)

    if not (health_ok and version_ok):
        print("🚫 Post-deployment verification FAILED")
        sys.exit(1)

    print("✅ Post-deployment verification PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()

