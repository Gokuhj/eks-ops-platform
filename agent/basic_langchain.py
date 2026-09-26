from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "You are a DevOps assistant. Explain this Kubernetes problem simply: {problem}"
)

messages = prompt.format_messages(
    problem="A Kubernetes pod keeps restarting"
)

print(messages)