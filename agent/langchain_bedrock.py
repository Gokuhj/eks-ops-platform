from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrockConverse

prompt = ChatPromptTemplate.from_template(
    """
    You are a DevOps assistant.

    Analyze this Kubernetes problem:
    {problem}

    Explain:
    1. Likely cause
    2. What to check
    3. Suggested fix

    Keep the answer short.
    """
)

model = ChatBedrockConverse(
    model_id="amazon.nova-micro-v1:0",
    region_name="ap-south-1",
    max_tokens=100,
    temperature=0
)

parser = StrOutputParser()

chain = prompt | model | parser

print("LangChain + Bedrock chain created successfully.")