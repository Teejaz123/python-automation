import os
import sys
import json
import socket
import shutil
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------

REQUIRED_ENV_VARS = [
    "APP_ENV",
    "DATABASE_URL",
    "AWS_REGION"
]

DEPENDENCIES = [
    ("Database", "localhost", 5432)
]

SECRETS_FILE = "secrets.json"
MAX_SECRET_AGE_DAYS = 90

MIN_FREE_DISK_PERCENT = 10

# ---------------- CHECKS ----------------

def check_env_vars():
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        print(f"❌ Missing env vars: {', '.join(missing)}")
        return False
    return True


def check_dependencies():
    for name, host, port in DEPENDENCIES:
        try:
            socket.create_connection((host, port), timeout=3)
            print(f"✅ {name} reachable")
        except Exception:
            print(f"❌ {name} unreachable ({host}:{port})")
            return False
    return True


def check_secret_rotation():
    if not os.path.exists(SECRETS_FILE):
        print("❌ Secrets metadata file missing")
        return False

    now = datetime.utcnow()
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)

    for s in secrets:
        last_rotated = datetime.fromisoformat(s["last_rotated"])
        if now - last_rotated > timedelta(days=MAX_SECRET_AGE_DAYS):
            print(f"❌ Secret expired: {s['name']}")
            return False

    print("✅ Secrets rotation within policy")
    return True


def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    free_percent = (free / total) * 100

    if free_percent < MIN_FREE_DISK_PERCENT:
        print(f"❌ Low disk space: {free_percent:.2f}% free")
        return False

    print(f"✅ Disk space OK: {free_percent:.2f}% free")
    return True


# ---------------- MAIN ----------------

def main():
    checks = [
        check_env_vars(),
        check_secret_rotation(),
        check_dependencies(),
        check_disk_space()
    ]

    if not all(checks):
        print("\n🚫 PRE-FLIGHT CHECK FAILED — DEPLOYMENT BLOCKED")
        sys.exit(1)

    print("\n🚀 PRE-FLIGHT CHECK PASSED — SAFE TO DEPLOY")
    sys.exit(0)


if __name__ == "__main__":
    main()

