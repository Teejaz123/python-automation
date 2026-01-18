from kubernetes import client, config

NAMESPACE = "default"
DEPLOYMENT_NAME = "myapp"
MIN_REPLICAS = 2
MAX_REPLICAS = 10
CPU_THRESHOLD = 70  # percent

config.load_kube_config()

apps = client.AppsV1Api()
metrics = client.CustomObjectsApi()

def get_cpu_usage():
    metrics_data = metrics.list_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=NAMESPACE,
        plural="pods"
    )

    total_cpu = 0
    count = 0

    for pod in metrics_data["items"]:
        for container in pod["containers"]:
            cpu = int(container["usage"]["cpu"].replace("n", "")) / 1e6
            total_cpu += cpu
            count += 1

    return total_cpu / count if count else 0

cpu_usage = get_cpu_usage()
deployment = apps.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
replicas = deployment.spec.replicas

if cpu_usage > CPU_THRESHOLD and replicas < MAX_REPLICAS:
    deployment.spec.replicas += 1
elif cpu_usage < CPU_THRESHOLD - 20 and replicas > MIN_REPLICAS:
    deployment.spec.replicas -= 1

apps.patch_namespaced_deployment(
    name=DEPLOYMENT_NAME,
    namespace=NAMESPACE,
    body=deployment
)

