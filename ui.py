import os

import requests
import streamlit as st

st.title("Multi-Agent Chatbot")

# Read API key from Streamlit secrets or environment variable
api_key = st.secrets.get("internal_api_key") or os.getenv("INTERNAL_API_KEY")

user_input = st.text_input("Enter your question")

if st.button("Send"):
    if not api_key:
        st.error("Internal API key not configured.")
    elif not user_input.strip():
        st.warning("Please enter a question.")
    else:
        headers = {"x-api-key": api_key}
        res = requests.post(
            "http://localhost:8000/chat",
            headers=headers,
            json={"user_input": user_input},
        )
        try:
            json_data = res.json()
            st.write(json_data.get("response", "❌ No 'response' in server reply."))
        except Exception as e:
            st.error(f"Failed to parse response: {e}")
