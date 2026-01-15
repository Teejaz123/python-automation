import requests
import time
from datetime import datetime

URLS_TO_MONITOR = [
    "https://google.com",
    "https://github.com",
    "https://example.com"
]

TIMEOUT = 5
CHECK_INTERVAL = 60  # seconds
LOG_FILE = "uptime.log"


def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=TIMEOUT)
        response_time = round(time.time() - start, 2)

        status = "UP" if response.status_code == 200 else "DOWN"
        return status, response_time
    except requests.RequestException:
        return "DOWN", None


def log_status(url, status, response_time):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(
            f"{timestamp} | {url} | {status} | Response Time: {response_time}s\n"
        )


def run_monitor():
    print("Starting uptime monitor...")
    while True:
        for url in URLS_TO_MONITOR:
            status, response_time = check_website(url)
            log_status(url, status, response_time)
            print(f"{url} → {status}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_monitor()

