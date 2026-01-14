import json
import sys
from datetime import datetime, timedelta

SECRETS_FILE = "secrets.json"
REPORT_FILE = "secret_rotation_report.txt"
WARNING_WINDOW_DAYS = 7


def load_secrets():
    with open(SECRETS_FILE, "r") as f:
        return json.load(f)


def check_secrets(secrets):
    now = datetime.utcnow()
    expired = []
    warning = []

    for s in secrets:
        last_rotated = datetime.fromisoformat(s["last_rotated"])
        max_age = timedelta(days=s["max_age_days"])
        expiry_date = last_rotated + max_age

        if now > expiry_date:
            expired.append(s["name"])
        elif expiry_date - now <= timedelta(days=WARNING_WINDOW_DAYS):
            warning.append(s["name"])

    return expired, warning


def write_report(expired, warning):
    with open(REPORT_FILE, "w") as f:
        f.write("SECRET ROTATION REPORT\n")
        f.write("======================\n")
        f.write(f"Generated: {datetime.utcnow()}\n\n")

        if not expired and not warning:
            f.write("All secrets are within rotation policy.\n")
            return

        if expired:
            f.write("Expired secrets:\n")
            for s in expired:
                f.write(f"- {s}\n")

        if warning:
            f.write("\nSecrets nearing expiry:\n")
            for s in warning:
                f.write(f"- {s}\n")


def main():
    secrets = load_secrets()
    expired, warning = check_secrets(secrets)
    write_report(expired, warning)

    if expired:
        print("Secret rotation check failed: expired secrets detected.")
        sys.exit(1)

    print("Secret rotation check passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()

