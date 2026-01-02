import shutil
import logging
import getpass
from datetime import datetime

# logging setup
logging.basicConfig(
    filename="health.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

total, used, free = shutil.disk_usage("/")

user = getpass.getuser()

logging.info(f"User: {user}")
logging.info(f"Disk Total: {total // (2**30)} GB")
logging.info(f"Disk Used: {used // (2**30)} GB")
logging.info(f"Disk Free: {free // (2**30)} GB")

print("System health check complete. Logged to health.log")

THRESHOLD = 10  # GB

free_gb = free // (2**30)

if free_gb < THRESHOLD:
    logging.warning("Disk space is running low!")

