import os
from huggingface_hub import InferenceClient

token = os.environ["HF_TOKEN"]

# Featherless AI is one of the providers on your enabled list, and HF's
# own documentation confirms this exact model works through it for chat.
client = InferenceClient(provider="featherless-ai", api_key=token)

response = client.chat_completion(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Explain AI engineering in one sentence."}],
    max_tokens=100,
)

print(response.choices[0].message.content)