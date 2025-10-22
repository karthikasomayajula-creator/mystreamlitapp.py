# Academic-Style Streamlit Chatbot Guide
# Author: Karthika
# Purpose: Demonstrate how to create a simple AI chatbot using Streamlit and OpenAI API

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ------------------------------
# Step 1: Load environment variables
# ------------------------------
# The API key for OpenAI is stored securely in a .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if API key exists
if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

# ------------------------------
# Step 2: Initialize OpenAI client
# ------------------------------
client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Step 3: Set up Streamlit page
# ------------------------------
st.set_page_config(page_title="AI Chatbot Guide", page_icon="🤖")
st.title("🌟 Academic AI Chatbot Example")

# ------------------------------
# Step 4: Initialize chat history
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store conversation history

# ------------------------------
# Step 5: User input section
# ------------------------------
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input:
    # Step 5a: Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Step 5b: Call OpenAI API for assistant response
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Change model if needed
        messages=st.session_state.messages
    )

    # Step 5c: Extract assistant response
    assistant_message = response.choices[0].message.content

    # Step 5d: Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# ------------------------------
# Step 6: Display chat history
# ------------------------------
st.subheader("Conversation (Latest messages at top)")

# Display messages in reverse order: latest first
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

