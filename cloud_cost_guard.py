import json
from datetime import datetime

RESOURCE_FILE = "resources.json"
REPORT_FILE = "cost_guard_report.txt"


def load_resources():
    with open(RESOURCE_FILE, "r") as f:
        return json.load(f)


def analyze_resources(resources):
    warnings = []

    for r in resources:
        if r["type"] == "EC2" and r["state"] == "running" and not r["has_traffic"]:
            warnings.append(f"Idle EC2 instance: {r['name']}")

        if r["type"] == "RDS" and r["public_access"]:
            warnings.append(f"Publicly accessible RDS: {r['name']}")

        if r["type"] == "S3" and not r["encryption"]:
            warnings.append(f"Unencrypted S3 bucket: {r['name']}")

    return warnings


def write_report(warnings):
    with open(REPORT_FILE, "w") as report:
        report.write("CLOUD COST & RISK REPORT\n")
        report.write("=======================\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        if not warnings:
            report.write("No cost or security risks detected.\n")
        else:
            for w in warnings:
                report.write(f"- {w}\n")


if __name__ == "__main__":
    resources = load_resources()
    issues = analyze_resources(resources)
    write_report(issues)

    if issues:
        print("⚠️ Potential cost or security issues found.")
    else:
        print("✅ No issues detected.")

