import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.title("🌟 Karthika's AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box at the top
user_input = st.text_input("You:")

# Send button
if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    # Append assistant message
    assistant_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# Chat container
with st.container():
    # Display messages in reverse (latest first)
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

