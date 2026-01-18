from kubernetes import client, config
import yaml
import os

BACKUP_DIR = "./k8s_backup"
os.makedirs(BACKUP_DIR, exist_ok=True)

config.load_kube_config()
apps = client.AppsV1Api()
core = client.CoreV1Api()

deployments = apps.list_deployment_for_all_namespaces()
services = core.list_service_for_all_namespaces()

for d in deployments.items:
    with open(f"{BACKUP_DIR}/{d.metadata.name}-deployment.yaml", "w") as f:
        yaml.dump(d.to_dict(), f)

for s in services.items:
    with open(f"{BACKUP_DIR}/{s.metadata.name}-service.yaml", "w") as f:
        yaml.dump(s.to_dict(), f)

