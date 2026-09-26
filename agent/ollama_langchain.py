from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


prompt = ChatPromptTemplate.from_template(
    """
    You are a DevOps assistant.

    Explain this Kubernetes problem simply:
    {problem}
    """
)

model = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)

parser = StrOutputParser()

chain = prompt | model | parser

response = chain.invoke({
    "problem": "A Kubernetes pod is in CrashLoopBackOff"
})

print(response)