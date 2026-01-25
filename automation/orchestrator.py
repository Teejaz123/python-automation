import subprocess
import yaml
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)

def load_config(path="tasks.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_command(task, defaults):
    name = task["name"]
    command = task["command"]
    timeout = task.get("timeout", defaults["default_timeout"])
    retries = task.get("retry", defaults["retry_count"])

    attempt = 0
    while attempt <= retries:
        try:
            logging.info(f"[{name}] Attempt {attempt + 1}")
            result = subprocess.run(
                command,
                shell=True,
                timeout=timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                logging.info(f"[{name}] SUCCESS")
                return {"task": name, "status": "SUCCESS", "output": result.stdout.strip()}

            raise subprocess.CalledProcessError(result.returncode, command, result.stderr)

        except Exception as e:
            logging.error(f"[{name}] FAILURE: {e}")
            attempt += 1

    return {"task": name, "status": "FAILED", "output": None}

def main():
    config = load_config()
    defaults = config["global"]
    tasks = config["tasks"]

    logging.info("Automation Orchestrator Started")
    start_time = datetime.now()

    results = []

    with ThreadPoolExecutor(max_workers=defaults["max_concurrency"]) as executor:
        futures = [executor.submit(run_command, task, defaults) for task in tasks]
        for future in as_completed(futures):
            results.append(future.result())

    duration = (datetime.now() - start_time).seconds
    success = sum(1 for r in results if r["status"] == "SUCCESS")

    logging.info(f"Completed in {duration}s | Success: {success} | Failed: {len(results) - success}")

if __name__ == "__main__":
    main()
