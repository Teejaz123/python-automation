import os
from datetime import datetime

LOG_DIRECTORY = "./logs"
OUTPUT_DIRECTORY = "./reports"

KEYWORDS = {
    "ERROR": 0,
    "WARNING": 0,
    "INFO": 0
}


def ensure_directories():
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)


def analyze_logs():
    for file in os.listdir(LOG_DIRECTORY):
        if file.endswith(".log") or file.endswith(".txt"):
            with open(os.path.join(LOG_DIRECTORY, file), "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    for key in KEYWORDS:
                        if key in line:
                            KEYWORDS[key] += 1


def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"system_report_{timestamp}.txt"
    report_path = os.path.join(OUTPUT_DIRECTORY, report_file)

    with open(report_path, "w") as report:
        report.write("SYSTEM LOG HEALTH REPORT\n")
        report.write("========================\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        for key, value in KEYWORDS.items():
            report.write(f"{key}: {value}\n")

    print(f"✅ Report generated: {report_path}")


if __name__ == "__main__":
    ensure_directories()
    analyze_logs()
    generate_report()

