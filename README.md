# EKS Ops Platform

An AI-assisted DevOps/SRE platform that combines CI/CD, containers,
Kubernetes, AWS services, Terraform, and a local LLM-based incident
analysis agent.

## Architecture

```text
GitHub
   |
   v
Jenkins
   |
   v
Docker Build
   |
   v
AWS ECR
   |
   v
Kubernetes / Minikube
   |
   +--------------------------+
   |                          |
   v                          v
Application              AI Incident Agent
                              |
                 +------------+------------+
                 |            |            |
              Pod Status     Logs       K8s Events
                 \            |            /
                  \           |           /
                   +----------+----------+
                              |
                              v
                     LangChain + Ollama
                              |
                              v
                       Qwen Local LLM
                              |
                              v
                     Incident Diagnosis
                              |
                       Restart Required?
                         /          \
                       No            Yes
                       |              |
                      Stop      Restart Deployment
                                      |
                                      v
                                    Verify
                                  /        \
                              Healthy    Unresolved
                                |            |
                               Stop       AWS SNS
```

## Technologies

- Python / Flask
- Docker
- Kubernetes
- Minikube
- Jenkins
- AWS ECR
- AWS SNS
- Terraform
- LangChain
- Ollama
- Qwen 2.5
- Git / GitHub

## Application

The Flask application exposes:

- `/` - application status
- `/health` - Kubernetes health endpoint

## CI/CD

The Jenkins pipeline:

1. Checks out source code
2. Builds the Docker image
3. Authenticates with AWS ECR
4. Pushes the image to ECR
5. Loads the image into Minikube
6. Deploys it to Kubernetes
7. Verifies the Kubernetes rollout

## AI Incident Agent

The local incident agent collects:

- Kubernetes pod status
- Application logs
- Kubernetes events

LangChain sends this context to a Qwen model running locally through
Ollama.

The model produces:

- Health status
- Evidence
- Likely cause
- Recommended action
- Restart decision

A controlled remediation path can restart the deployment and verify
whether it recovered.

If an attempted remediation remains unresolved, the platform can
publish an incident alert through AWS SNS.

## Infrastructure as Code

Terraform configuration is included for AWS infrastructure.

Terraform state uses an S3 backend. Local Terraform state and
`.terraform/` files are excluded from Git.

## Running the Local AI Agent

Install dependencies:

```bash
cd agent
pip install -r requirements.txt
```

Make sure Ollama is running and the model is available:

```bash
ollama pull qwen2.5:1.5b
```

Run the incident agent:

```bash
python local_incident_agent.py
```

## Kubernetes

Check the deployment:

```bash
kubectl get pods
kubectl get svc
```

## Safety

Automatic remediation is controlled using the `AUTO_REMEDIATE`
setting.

The agent separates:

Observe -> Diagnose -> Decide -> Remediate -> Verify -> Escalate

This prevents every detected Kubernetes warning from automatically
triggering a restart.

## Project Status

Version 1 demonstrates:

- Containerized application deployment
- Jenkins CI/CD
- AWS ECR integration
- Kubernetes deployment and health checks
- Terraform infrastructure configuration
- Local LLM integration with Ollama
- LangChain-based incident analysis
- Kubernetes diagnostic tools
- Controlled remediation
- Post-remediation verification
- AWS SNS incident escalation

## Future Improvements

Future versions could explore LangGraph, RAG-based runbooks,
human-in-the-loop approvals, observability integrations, and managed
LLM inference through Amazon Bedrock.