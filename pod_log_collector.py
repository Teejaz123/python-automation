from kubernetes import client, config
import os

NAMESPACE = "default"
LOG_DIR = "./pod_logs"
os.makedirs(LOG_DIR, exist_ok=True)

config.load_kube_config()
v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod(NAMESPACE)

for pod in pods.items:
    name = pod.metadata.name
    logs = v1.read_namespaced_pod_log(name=name, namespace=NAMESPACE)

    with open(f"{LOG_DIR}/{name}.log", "w") as f:
        f.write(logs)

print("Logs collected successfully")

