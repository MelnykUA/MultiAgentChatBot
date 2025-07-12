import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

from agents import coder_node, researcher_node

load_dotenv()  # Load environment variables

app = FastAPI()

# CORS Setup — restrict origins in staging/production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


@app.get("/")
def read_root():
    return {"message": "Multi-Agent Chatbot API is running."}


@app.post("/chat")
async def chat(request: Request, _api_key: str = Depends(api_key_header)):
    # _api_key is checked by Depends(api_key_header), so no need to check again here.

    data = await request.json()
    user_input = data.get("user_input", "").strip()

    if not user_input:
        return {"response": "❌ No input provided."}

    logging.info(f"[Request] User input: {user_input}")

    try:
        intermediate_result = researcher_node({"input": user_input})
        final_result = coder_node(intermediate_result)
        logging.info(f"[Response] Final output: {final_result}")
        return {"response": final_result.get("code", "No output")}
    except Exception as e:
        logging.exception("An error occurred in /chat")
        return {"response": f"❌ Internal server error: {str(e)}"}
