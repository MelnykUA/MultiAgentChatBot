import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()  # Load environment variables


def use_fake_openai() -> bool:
    return os.getenv("USE_FAKE_OPENAI", "false").lower() == "true"


api_key = os.getenv("OPENAI_API_KEY")
if not api_key and not use_fake_openai():
    raise ValueError("🔐 OPENAI_API_KEY not found in environment variables.")

if not use_fake_openai():

    client = OpenAI(api_key=api_key)


def researcher_node(data: dict) -> dict:
    user_input = data["input"]
    print("🔍 Researcher thinking...")

    if use_fake_openai():

        output = "This is a mocked response explaining transformer models in machine learning."
    else:
        messages = cast(
            list[ChatCompletionMessageParam],
            [
                {
                    "role": "system",
                    "content": "You are a helpful AI research assistant.",
                },
                {"role": "user", "content": user_input},
            ],
        )
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        output = response.choices[0].message.content

    print(f"📄 Researcher output: {output}")
    return {"research": output}


def coder_node(data: dict) -> dict:
    research = data["research"]
    print("💻 Coder generating code based on research...")

    if use_fake_openai():

        code_output = (
            "def transformer_model():\n"
            "    '''Mock function representing a transformer model.'''\n"
            "    return 'This is mock transformer model code.'"
        )
    else:
        messages = cast(
            list[ChatCompletionMessageParam],
            [
                {"role": "system", "content": "You are a senior software engineer."},
                {
                    "role": "user",
                    "content": f"Write a Python function based on this research:\n\n{research}",
                },
            ],
        )
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        code_output = response.choices[0].message.content

    print(f"🧠 Coder output:\n{code_output}")
    return {"code": code_output}
