# ui.py (updated)
import logging
import os

import requests
import streamlit as st

# Set up logging
logger = logging.getLogger(__name__)
st.set_page_config(page_title="Multi-Agent Chatbot")
st.title("Multi-Agent Chatbot")

# Read API key from Streamlit secrets or environment variable
api_key = st.secrets.get("internal_api_key") or os.getenv("INTERNAL_API_KEY")
api_url = os.getenv("API_URL", "https://localhost/api/chat")

user_input = st.text_input("Enter your question")

if st.button("Send"):
    if not api_key:
        st.error("Internal API key not configured.")
    elif not user_input.strip():
        st.warning("Please enter a question.")
    else:
        headers = {"x-api-key": api_key}
        try:
            response = requests.post(
                api_url, headers=headers, json={"user_input": user_input}, verify=False
            )
            response.raise_for_status()
            json_data = response.json()
            st.write(json_data.get("response", "❌ No 'response' in server reply."))
        except requests.exceptions.RequestException as e:
            logger.exception("HTTP request failed")
            st.error(f"Failed to reach backend: {e}")
        except ValueError:
            st.error("Invalid response received from the server.")
