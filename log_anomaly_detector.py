from collections import Counter
from datetime import datetime

LOG_FILE = "app.log"
REPORT_FILE = "log_anomaly_report.txt"
ERROR_KEYWORDS = ["ERROR", "CRITICAL", "FAILED"]
REPEAT_THRESHOLD = 3


def load_logs():
    with open(LOG_FILE, "r") as f:
        return f.readlines()


def detect_anomalies(lines):
    error_lines = [line for line in lines if any(k in line for k in ERROR_KEYWORDS)]
    messages = Counter(error_lines)

    repeated_errors = {
        msg: count for msg, count in messages.items()
        if count >= REPEAT_THRESHOLD
    }

    return len(error_lines), repeated_errors


def write_report(total_errors, repeated_errors):
    with open(REPORT_FILE, "w") as report:
        report.write("LOG ANOMALY REPORT\n")
        report.write("=================\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        report.write(f"Total error-related lines: {total_errors}\n\n")

        if repeated_errors:
            report.write("Repeated errors detected:\n")
            for msg, count in repeated_errors.items():
                report.write(f"({count}x) {msg}")
        else:
            report.write("No repeated error patterns detected.\n")


if __name__ == "__main__":
    logs = load_logs()
    total, repeats = detect_anomalies(logs)
    write_report(total, repeats)

    if repeats:
        print("⚠️ Log anomalies detected.")
    else:
        print("✅ No anomalies detected.")

