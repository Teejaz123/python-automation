
import os
import sys
from datetime import datetime

REQUIRED_ENV_VARS = [
    "APP_ENV",
    "DATABASE_URL",
    "API_KEY"
]

REPORT_FILE = "env_validation_report.txt"


def validate_env():
    missing = []
    empty = []

    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if value is None:
            missing.append(var)
        elif value.strip() == "":
            empty.append(var)

    return missing, empty


def write_report(missing, empty):
    with open(REPORT_FILE, "w") as report:
        report.write("ENVIRONMENT VALIDATION REPORT\n")
        report.write("=============================\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        if not missing and not empty:
            report.write("All required environment variables are correctly set.\n")
        else:
            if missing:
                report.write("Missing variables:\n")
                for var in missing:
                    report.write(f" - {var}\n")

            if empty:
                report.write("\nEmpty variables:\n")
                for var in empty:
                    report.write(f" - {var}\n")


def main():
    missing, empty = validate_env()
    write_report(missing, empty)

    if missing or empty:
        print("❌ Environment validation failed.")
        sys.exit(1)

    print("✅ Environment validation passed.")


if __name__ == "__main__":
    main()
~
~
~
~
~
~
~
~

~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~

