from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from k8s_tool import ( get_pod_status, get_pod_logs, get_k8s_events, restart_deployment, verify_deployment, send_alert)

AUTO_REMEDIATE = True

# Get real Kubernetes information
status = get_pod_status.invoke({})
logs = get_pod_logs.invoke({})
events = get_k8s_events.invoke({})


# Create the incident-analysis prompt
prompt = ChatPromptTemplate.from_template(
    """
You are a Kubernetes DevOps incident-response assistant.

Here is the current pod status:

{status}

Here are recent application logs:

{logs}

Kubernetes events

{events}

Analyze this information.

Return exactly in this format:

1. HEALTH: Healthy or Problem
2. RESTART_REQUIRED: YES or NO
3. CAUSE: short explanation
4. Recommended action: short recommended action

only recommend a restart when the evidence suggests restarting the deployment could resonabaly help.

Keep the response short.
"""
)


model = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)

parser = StrOutputParser()

chain = prompt | model | parser


response = chain.invoke({
    "status": status,
    "logs": logs,
    "events": events
})


print("\n===== AI INCIDENT ANALYSIS =====")
print(response)

restart_required = "RESTART_REQUIRED: YES" in response.upper()

if restart_required:
    print("\nAI recommends restarting the deployment.")
    if AUTO_REMEDIATE:
        print("\n=============REMEDIATION========")
        print(restart_deployment.invoke({}))

        print("\n=========Verification========")
        verification = verify_deployment.invoke({})
        print(verification)
        #print(verify_deployment.invoke({}))

        if verification.startswith("UNHEALTHY"):
            print("\n=======ESCALATION========")

            alert_result = send_alert.invoke({
                "message": (
                    "EKS ops platform incidents remains unresolved.\n\n"
                    f"AI analysis:\n{response}\n\n"
                    f"Verification:\n{verification}"
                )
            })
            print(alert_result)

    else:
        print("automatic remediation is disabled")
    #print("automatic restart is disabled for safety purpose")
else:
    print("\nNo restart is required")