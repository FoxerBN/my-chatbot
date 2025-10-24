from openai import OpenAI
from src.config import OPENAI_API_KEY
from src.prompt import CHAT_PROMPT
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt: str, context_messages: list = None):
    messages = [{"role": "system", "content": CHAT_PROMPT}]

    if context_messages:
        messages.extend(context_messages)

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=200,
        temperature=0.4,
    )

    return response.choices[0].message.content
