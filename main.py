from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from agents import researcher_node, coder_node
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

app = FastAPI()

# Setup CORS for dev (restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Multi-Agent Chatbot API is running."}

@app.post("/chat")
async def chat(request: Request, x_api_key: str = Header(None)):
    if x_api_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        data = await request.json()
        user_input = data.get("user_input", "").strip()

        if not user_input:
            return {"response": "❌ No input provided."}

        logging.info(f"[Request] User input: {user_input}")

        # Run agents chain
        intermediate_result = researcher_node({"input": user_input})
        final_result = coder_node(intermediate_result)

        logging.info(f"[Response] Final output: {final_result}")

        return {"response": final_result["code"]}
    except Exception as e:
        logging.exception("An error occurred in /chat")
        return {"response": f"❌ Internal server error: {str(e)}"}
