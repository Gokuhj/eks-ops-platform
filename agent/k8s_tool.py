import subprocess
import boto3
from langchain_core.tools import tool


@tool
def get_pod_status() -> str:
    """Get the current status of Kubernetes pods."""

    result = subprocess.run(
        ["kubectl", "get", "pods"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

@tool
def get_pod_logs() -> str:
    """Get recent logs from the devops-app Kubernetes pods."""

    result = subprocess.run(
        [
            "kubectl",
            "logs",
            "-l",
            "app=devops-app",
            "--tail=20"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

@tool
def restart_deployment() -> str:
    """Restart the devops-app Kubernetes deployment."""

    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "restart",
            "deployment/devops-app"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

@tool
def get_k8s_events() -> str:
    """Get recent Kubernetes events for diagnosing pod failures."""

    result = subprocess.run(
        [
            "kubectl",
            "get",
            "events",
            "--sort-by=.lastTimestamp"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

@tool
def verify_deployment() -> str:
    """Verify whether the devops-app Kubernetes deployment is healthy."""

    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "status",
            "deployment/devops-app",
            "--timeout=30s"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return "HEALTHY: " + result.stdout.strip()

    return "UNHEALTHY: " + result.stderr.strip()

@tool
def send_alert(message: str) -> str:
    """Send an unresolved Kubernetes incident alert using AWS SNS."""

    try:
        sns = boto3.client("sns", region_name="ap-south-1")

        account_id = boto3.client("sts").get_caller_identity()["Account"]

        topic_arn = (
            f"arn:aws:sns:ap-south-1:{account_id}:eks-incident-alerts"
        )

        response = sns.publish(
            TopicArn=topic_arn,
            Subject="EKS Ops Platform Incident",
            Message=message
        )

        return f"Alert sent successfully. MessageId: {response['MessageId']}"

    except Exception as e:
        return f"Failed to send alert: {e}"


print("Tool name:", get_pod_status.name)
print("Tool description:", get_pod_status.description)

#print("\nKubernetes pod status:")
#print(get_pod_status.invoke({}))

#print("\nKubernetes pod logs:")
#print(get_pod_logs.invoke({}))

print("\nAction tool available:")
print(restart_deployment.name)
print(restart_deployment.description)

#print("\nKubernetes events:")
#print(get_k8s_events.invoke({}))

#print("\nDeployment verification:")
#print(verify_deployment.invoke({}))

