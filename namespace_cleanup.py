from kubernetes import client, config
from datetime import datetime, timezone

MAX_AGE_DAYS = 30

config.load_kube_config()
v1 = client.CoreV1Api()

namespaces = v1.list_namespace()

for ns in namespaces.items:
    name = ns.metadata.name
    created = ns.metadata.creation_timestamp
    age_days = (datetime.now(timezone.utc) - created).days

    if age_days > MAX_AGE_DAYS and name not in ["default", "kube-system"]:
        v1.delete_namespace(name)
        print(f"Deleted namespace: {name}")

