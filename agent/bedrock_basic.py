import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

response = client.converse(
    modelId="amazon.nova-micro-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": "In one sentence, what is a Kubernetes pod?"
                }
            ]
        }
    ],
    inferenceConfig={
        "maxTokens": 50,
        "temperature": 0
    }
)

answer = response["output"]["message"]["content"][0]["text"]

print(answer)