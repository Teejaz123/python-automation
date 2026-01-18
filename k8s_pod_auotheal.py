from kubernetes import client, config
import logging
from datetime import datetime

# ================= CONFIGURATION =================
NAMESPACE = "default"
LOG_FILE = "/var/log/k8s_auto_heal.log"
UNHEALTHY_STATES = ["Failed", "Pending"]
# =================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_kube_config():
    try:
        config.load_kube_config()
        logging.info("Loaded local kubeconfig")
    except:
        config.load_incluster_config()
        logging.info("Loaded in-cluster config")

def is_crashloop(pod):
    if not pod.status.container_statuses:
        return False
    for container in pod.status.container_statuses:
        state = container.state
        if state.waiting and state.waiting.reason == "CrashLoopBackOff":
            return True
    return False

def main():
    load_kube_config()
    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=NAMESPACE)
    logging.info(f"Scanning namespace: {NAMESPACE}")

    for pod in pods.items:
        pod_name = pod.metadata.name
        phase = pod.status.phase

        if phase in UNHEALTHY_STATES or is_crashloop(pod):
            logging.warning(f"Unhealthy pod detected: {pod_name} ({phase})")

            v1.delete_namespaced_pod(
                name=pod_name,
                namespace=NAMESPACE
            )

            logging.info(f"De

