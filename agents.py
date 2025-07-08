import os
from dotenv import load_dotenv
from typing import cast
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("🔐 OPENAI_API_KEY not found in environment variables. Please set it in .env")

client = OpenAI(api_key=api_key)

def researcher_node(data: dict) -> dict:
    user_input = data["input"]
    print("🔍 Researcher thinking...")

    messages = cast(
        list[ChatCompletionMessageParam],
        [
            ChatCompletionSystemMessageParam(role="system", content="You are a helpful AI research assistant."),
            ChatCompletionUserMessageParam(role="user", content=user_input),
        ],
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    output = response.choices[0].message.content
    print(f"📄 Researcher output: {output}")
    return {"research": output}

def coder_node(data: dict) -> dict:
    research = data["research"]
    print("💻 Coder generating code based on research...")

    messages = cast(
        list[ChatCompletionMessageParam],
        [
            ChatCompletionSystemMessageParam(role="system", content="You are a senior software engineer."),
            ChatCompletionUserMessageParam(role="user", content=f"Write a Python function based on this research:\n\n{research}"),
        ],
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    code_output = response.choices[0].message.content
    print(f"🧠 Coder output:\n{code_output}")
    return {"code": code_output}
