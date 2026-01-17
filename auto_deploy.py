import subprocess
import logging
from datetime import datetime

# ================= CONFIGURATION =================
REPO_DIR = "/opt/myapp"
IMAGE_NAME = "myapp:latest"
CONTAINER_NAME = "myapp_container"
LOG_FILE = "/var/log/auto_deploy.log"
# =================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_cmd(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logging.error(result.stderr)
        raise RuntimeError(result.stderr)
    return result.stdout

def main():
    logging.info("Starting automated deployment")

    logging.info("Pulling latest code")
    run_cmd(f"cd {REPO_DIR} && git pull")

    logging.info("Building Docker image")
    run_cmd(f"cd {REPO_DIR} && docker build -t {IMAGE_NAME} .")

    logging.info("Stopping old container")
    run_cmd(f"docker stop {CONTAINER_NAME} || true")

    logging.info("Removing old container")
    run_cmd(f"docker rm {CONTAINER_NAME} || true")

    logging.info("Starting new container")
    run_cmd(
        f"docker run -d --name {CONTAINER_NAME} "
        f"-p 80:80 {IMAGE_NAME}"
    )

    logging.info("Deployment completed successfully")

if __name__ == "__main__":
    main()

