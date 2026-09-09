# Memory Chat

A tiny AI chatbot that remembers facts about you across a conversation
(and future runs), using [Mem0](https://mem0.ai) for long-term memory.

## How it works

Every message you send:
1. Gets checked against memory for relevant facts about you
2. Is answered by GPT-4o-mini using those facts as context
3. Gets saved back to memory — so the agent keeps learning

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI + Mem0 keys (both free to get)
python memory_chat.py
```

## Example

```
You: I'm a backend developer and I prefer Python over Java.
AI: Got it! ...

You: What language should I use for my new project?
AI: Since you prefer Python, I'd recommend...
```

## Get your keys

- OpenAI: https://platform.openai.com/api-keys
- Mem0 (free tier): https://app.mem0.ai
