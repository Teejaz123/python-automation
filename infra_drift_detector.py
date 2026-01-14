import json
import sys
from datetime import datetime

DESIRED_STATE_FILE = "desired_state.json"
ACTUAL_STATE_FILE = "actual_state.json"
REPORT_FILE = "infra_drift_report.txt"


def load_state(path):
    with open(path, "r") as f:
        return json.load(f)


def detect_drift(desired, actual):
    drift = []

    desired_resources = {r["id"]: r for r in desired}
    actual_resources = {r["id"]: r for r in actual}

    for rid, res in desired_resources.items():
        if rid not in actual_resources:
            drift.append(f"Missing resource: {rid}")
        elif res != actual_resources[rid]:
            drift.append(f"Config mismatch: {rid}")

    for rid in actual_resources:
        if rid not in desired_resources:
            drift.append(f"Unexpected resource: {rid}")

    return drift


def write_report(drift):
    with open(REPORT_FILE, "w") as f:
        f.write("INFRASTRUCTURE DRIFT REPORT\n")
        f.write("===========================\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        if not drift:
            f.write("No infrastructure drift detected.\n")
        else:
            for d in drift:
                f.write(f"- {d}\n")


def main():
    desired = load_state(DESIRED_STATE_FILE)
    actual = load_state(ACTUAL_STATE_FILE)

    drift = detect_drift(desired, actual)
    write_report(drift)

    if drift:
        print("❌ Infrastructure drift detected")
        sys.exit(1)

    print("✅ Infrastructure is in sync")
    sys.exit(0)


if __name__ == "__main__":
    main()

