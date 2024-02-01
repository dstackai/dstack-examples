from openai import OpenAI

client = OpenAI(
    base_url="https://gateway.my-gateway-domain.dstack.ai", api_key="2879c3d8-4b1e-4c88-a074-d6df62c55a95"
)
resp = client.chat.completions.create(
    model="TheBloke/CodeLlama-70B-Instruct-GPTQ",
    messages=[
        {
            "role": "user",
            "content": "How to kill all SSH tunnells on MacOS via bash?",
        },
    ],
    stream=True,
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="")
print()
