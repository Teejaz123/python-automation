import os
import time
from datetime import datetime

TARGET_DIR = "./temp"
MAX_AGE_DAYS = 7
DRY_RUN = True  # Set to False to enable deletion

REPORT_FILE = "cleanup_report.txt"


def cleanup_old_files():
    now = time.time()
    deleted_files = []

    os.makedirs(TARGET_DIR, exist_ok=True)

    for filename in os.listdir(TARGET_DIR):
        path = os.path.join(TARGET_DIR, filename)

        if not os.path.isfile(path):
            continue

        file_age_days = (now - os.path.getmtime(path)) / 86400

        if file_age_days > MAX_AGE_DAYS:
            if DRY_RUN:
                print(f"[DRY RUN] Would delete: {filename}")
            else:
                os.remove(path)
                deleted_files.append(filename)
                print(f"Deleted: {filename}")

    return deleted_files


def write_report(deleted_files):
    with open(REPORT_FILE, "w") as report:
        report.write("TEMP FILE CLEANUP REPORT\n")
        report.write("========================\n")
        report.write(f"Run time: {datetime.now()}\n\n")

        if not deleted_files:
            report.write("No files deleted.\n")
        else:
            report.write("Deleted files:\n")
            for file in deleted_files:
                report.write(f" - {file}\n")


if __name__ == "__main__":
    deleted = cleanup_old_files()
    write_report(deleted)

