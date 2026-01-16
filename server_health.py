import psutil
import subprocess
import logging
from datetime import datetime

# ================= CONFIGURATION =================
CPU_THRESHOLD = 80      # percent
MEM_THRESHOLD = 80      # percent
DISK_THRESHOLD = 85     # percent

SERVICES = ["docker", "nginx"]  # services to monitor
LOG_FILE = "/var/log/server_health.log"
# =================================================

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_cpu():
    return psutil.cpu_percent(interval=1)

def check_memory():
    return psutil.virtual_memory().percent

def check_disk():
    return psutil.disk_usage("/").percent

def check_service(service):
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "active"

def main():
    logging.info("Starting server health check")

    cpu = check_cpu()
    memory = check_memory()
    disk = check_disk()

    logging.info(f"CPU Usage: {cpu}%")
    logging.info(f"Memory Usage: {memory}%")
    logging.info(f"Disk Usage: {disk}%")

    if cpu > CPU_THRESHOLD:
        logging.warning(f"High CPU usage detected: {cpu}%")

    if memory > MEM_THRESHOLD:
        logging.warning(f"High memory usage detected: {memory}%")

    if disk > DISK_THRESHOLD:
        logging.warning(f"High disk usage detected: {disk}%")

    for service in SERVICES:
        if check_service(service):
            logging.info(f"Service running: {service}")
        else:
            logging.error(f"Service NOT running: {service}")

    logging.info("Health check completed\n")

if __name__ == "__main__":
    main()

