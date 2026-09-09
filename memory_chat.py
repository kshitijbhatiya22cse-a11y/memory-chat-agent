"""
memory_chat.py
--------------
A small AI chatbot that remembers things about you across a conversation
(and across runs, since memory is stored in Mem0's cloud).

Setup:
    pip install -r requirements.txt
    Copy .env.example to .env and fill in your keys:
      - OPENAI_API_KEY   (https://platform.openai.com/api-keys)
      - MEM0_API_KEY     (https://app.mem0.ai -> free account)

Run:
    python memory_chat.py
"""

import os

from dotenv import load_dotenv
from mem0 import MemoryClient
from openai import OpenAI

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
memory = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

USER_ID = "default_user"


def chat(user_message: str) -> str:
    # 1. Pull relevant memories about this user
    relevant = memory.search(user_message, user_id=USER_ID)
    memory_text = "\n".join(f"- {r['memory']}" for r in relevant) or "(nothing yet)"

    # 2. Ask the LLM, giving it that memory as context
    system_prompt = f"You are a helpful assistant. Known facts about the user:\n{memory_text}"
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    reply = response.choices[0].message.content

    # 3. Save this exchange so the agent learns from it
    memory.add(
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": reply},
        ],
        user_id=USER_ID,
    )

    return reply


if __name__ == "__main__":
    print("Memory Chat — type 'exit' to quit\n")
    while True:
        text = input("You: ").strip()
        if text.lower() in {"exit", "quit"}:
            break
        print(f"AI: {chat(text)}\n")
