import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Multi-Agent Chatbot")

user_input = st.text_input("Enter your question")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

if st.button("Send"):
    headers = {"x-api-key": INTERNAL_API_KEY} if INTERNAL_API_KEY else {}

    res = requests.post(
        "http://localhost:8000/chat",
        json={"user_input": user_input},
        headers=headers
    )

    try:
        json_data = res.json()
        st.write(json_data.get("response", "❌ No 'response' in server reply."))
    except Exception as e:
        st.error(f"Failed to parse response: {e}")
