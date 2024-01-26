from openai import OpenAI


client = OpenAI(base_url="https://gateway.<gateway domain>", api_key="none")

completion = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    messages=[
        {
            "role": "user",
            "content": "Compose a poem that explains the concept of recursion in programming.",
        }
    ],
)

print(completion.choices[0].message)
