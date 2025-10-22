# Academic Assistant Chatbot
# Author: Karthika
# Description: Upload academic files (PDF, DOCX, TXT) and get AI-based suggestions or answers.

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Try importing file reader modules safely
try:
    from PyPDF2 import PdfReader
except ImportError:
    st.error("PyPDF2 not found. Please add 'PyPDF2' to requirements.txt or install it with 'pip install PyPDF2'.")
    st.stop()

try:
    import docx
except ImportError:
    st.error("python-docx not found. Please add 'python-docx' to requirements.txt or install it with 'pip install python-docx'.")
    st.stop()

# ------------------------------
# Step 1: Load OpenAI API key
# ------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Step 2: Streamlit page setup
# ------------------------------
st.set_page_config(page_title="📚 Academic Assistant", page_icon="🎓")
st.title("🎓 Academic Assistant Chatbot")

# ------------------------------
# Step 3: Initialize session states
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_text" not in st.session_state:
    st.session_state.file_text = ""

# ------------------------------
# Step 4: File upload and text extraction
# ------------------------------
uploaded_file = st.file_uploader("📁 Upload your academic file (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])

if uploaded_file:
    extracted_text = ""

    if uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.type == "text/plain":
        extracted_text = uploaded_file.read().decode("utf-8")

    st.session_state.file_text = extracted_text
    st.success("✅ File uploaded and content extracted successfully!")

# ------------------------------
# Step 5: User input
# ------------------------------
user_input = st.text_input("💬 Ask a question or request academic suggestions:")

if st.button("Send") and user_input:
    # Create conversation context
    context = st.session_state.file_text
    messages = [{"role": "system", "content": f"You are an academic assistant. Use this document for context:\n{context}"}]
    messages.extend(st.session_state.messages)
    messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

    assistant_message = response.choices[0].message.content

    # Update chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# ------------------------------
# Step 6: Display conversation
# ------------------------------
st.subheader("🗨️ Conversation (Newest messages on top)")

for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**👩‍🎓 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Assistant:** {msg['content']}")
