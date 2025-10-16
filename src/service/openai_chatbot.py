from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[ # type: ignore
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.3,
    )

    reply = response.choices[0].message.content
    print("🧠 GPT answer:", reply)
    return reply
