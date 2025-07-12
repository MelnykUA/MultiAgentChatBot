import logging
import os
from typing import Any, Dict, List, Optional, cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

logger = logging.getLogger(__name__)


def use_fake_openai() -> bool:
    return os.getenv("USE_FAKE_OPENAI", "false").lower() == "true"


def get_openai_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if use_fake_openai():
        return None
    if not api_key:
        raise ValueError("🔐 OPENAI_API_KEY not found and fake mode is disabled.")
    return OpenAI(api_key=api_key)


client: Optional[OpenAI] = get_openai_client()


def researcher_node(data: Dict[str, Any]) -> Dict[str, str]:
    user_input = data.get("input", "").strip()
    logger.info("🔍 Researcher thinking...")

    if use_fake_openai():
        output = "This is a mocked response explaining transformer models in machine learning."
    else:
        messages: List[ChatCompletionMessageParam] = cast(
            List[ChatCompletionMessageParam],
            [
                {
                    "role": "system",
                    "content": "You are a helpful AI research assistant.",
                },
                {"role": "user", "content": user_input},
            ],
        )
        if not client:
            raise RuntimeError("OpenAI client not initialized.")
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        output = response.choices[0].message.content or "⚠️ No content from OpenAI."

    logger.info(f"📄 Researcher output: {output}")
    return {"research": output}


def coder_node(data: Dict[str, Any]) -> Dict[str, str]:
    research = data.get("research", "").strip()
    logger.info("💻 Coder generating code based on research...")

    if use_fake_openai():
        code_output = (
            "def transformer_model():\n"
            "    '''Mock function representing a transformer model.'''\n"
            "    return 'This is mock transformer model code.'"
        )
    else:
        messages: List[ChatCompletionMessageParam] = cast(
            List[ChatCompletionMessageParam],
            [
                {"role": "system", "content": "You are a senior software engineer."},
                {
                    "role": "user",
                    "content": f"Write a Python function based on this research:\n\n{research}",
                },
            ],
        )
        if not client:
            raise RuntimeError("OpenAI client not initialized.")
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        code_output = response.choices[0].message.content or "⚠️ No content from OpenAI."

    logger.info(f"🧠 Coder output:\n{code_output}")
    return {"code": code_output}
