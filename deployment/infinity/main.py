from functools import partial

from openai import OpenAI

client = OpenAI(
    base_url="https://<run name>.<gateway domain>", api_key="<dstack token>"
)

client.embeddings.create = partial(client.embeddings.create, model="bge-small-en-v1.5")

print(client.embeddings.create(input=["A sentence to encode."]))
