from kubernetes import client, config
import subprocess
import logging

# ================= CONFIGURATION =================
LOG_FILE = "/var/log/k8s_node_drain.log"
EXCLUDED_NODES = ["master", "control-plane"]
# =================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    try:
        config.load_kube_config()
        logging.info("Loaded kubeconfig")
    except:
        config.load_incluster_config()
        logging.info("Loaded in-cluster config")

def is_node_ready(node):
    for condition in node.status.conditions:
        if condition.type == "Ready":
            return condition.status == "True"
    return False

def drain_node(node_name):
    logging.warning(f"Draining node: {node_name}")
    subprocess.run(
        [
            "kubectl", "drain", node_name,
            "--ignore-daemonsets",
            "--delete-emptydir-data",
            "--force"
        ],
        check=False
    )

def main():
    load_config()
    v1 = client.CoreV1Api()

    nodes = v1.list_node()

    for node in nodes.items:
        name = node.metadata.name

        if any(x in name for x in EXCLUDED_NODES):
            continue

        if not is_node_ready(node):
            logging.error(f"Node NotReady detected: {name}")
            drain_node(name)

    logging.info("Node scan completed\n")

if __name__ == "__main__":
    main()

