from kubernetes import client, config

NAMESPACE = "default"
DEPLOYMENT_NAME = "myapp"
NEW_IMAGE = "myrepo/myapp:latest"

config.load_kube_config()
apps = client.AppsV1Api()

deployment = apps.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
deployment.spec.template.spec.containers[0].image = NEW_IMAGE

apps.patch_namespaced_deployment(
    name=DEPLOYMENT_NAME,
    namespace=NAMESPACE,
    body=deployment
)

print("Deployment updated successfully")

