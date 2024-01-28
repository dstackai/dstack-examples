from functools import partial

from openai import OpenAI

url = "https://<run name>.<gateway domain>"
client = OpenAI(api_key="dummy", base_url=url)

client.embeddings.create = partial(client.embeddings.create, model="bge-small-en-v1.5")

print(client.embeddings.create(input=["A sentence to encode."]))
