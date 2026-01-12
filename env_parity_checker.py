import json
import sys
from datetime import datetime

ENV_FILES = {
    "development": "dev.json",
    "staging": "staging.json",
    "production": "prod.json"
}

REPORT_FILE = "env_parity_report.txt"


def load_env(file):
    with open(file, "r") as f:
        return json.load(f)


def main():
    env_data = {}
    all_keys = set()

    for env, file in ENV_FILES.items():
        try:
            data = load_env(file)
            env_data[env] = set(data.keys())
            all_keys.update(data.keys())
        except FileNotFoundError:
            print(f"❌ Missing file: {file}")
            sys.exit(1)

    mismatches = []

    for key in all_keys:
        missing_in = [
            env for env, keys in env_data.items() if key not in keys
        ]
        if missing_in:
            mismatches.append((key, missing_in))

    with open(REPORT_FILE, "w") as report:
        report.write("ENVIRONMENT PARITY REPORT\n")
        report.write("=========================\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        if not mismatches:
            report.write("All environments are consistent.\n")
        else:
            for key, envs in mismatches:
                report.write(f"Missing '{key}' in: {', '.join(envs)}\n")

    if mismatches:
        print("❌ Environment parity check failed.")
        sys.exit(1)

    print("✅ Environment parity check passed.")


if __name__ == "__main__":
    main()

