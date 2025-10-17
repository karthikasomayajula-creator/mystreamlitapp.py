import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=sk-...2moA
)

st.title("🌟 Karthika's AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:", "")

if st.button("Send") or user_input:
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        # Extract assistant message
        assistant_message = response.choices[0].message.content

        # Append assistant message
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Clear input box
        st.experimental_rerun()

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

