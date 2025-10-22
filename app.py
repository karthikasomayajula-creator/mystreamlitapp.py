
# Academic Assistant Chatbot
# Purpose: Upload academic files and interact with AI to get suggestions or answers
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import docx

# ------------------------------
# Step 1: Load OpenAI API Key
# ------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Add it to your .env file.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Step 2: Page Setup
# ------------------------------
st.set_page_config(page_title="Academic Assistant", page_icon="📚")
st.title("📚 Academic Assistant Chatbot")

# ------------------------------
# Step 3: Initialize session state
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_text" not in st.session_state:
    st.session_state.file_text = ""  # Store text extracted from uploaded files

# ------------------------------
# Step 4: File Upload Section
# ------------------------------
uploaded_file = st.file_uploader(
    "Upload your academic file (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        st.session_state.file_text = text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.session_state.file_text = text
    elif uploaded_file.type == "text/plain":
        st.session_state.file_text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded and text extracted successfully!")

# ------------------------------
# Step 5: User Input
# ------------------------------
user_input = st.text_input("Ask your question or request suggestions:")

if st.button("Send") and user_input:
    # Include uploaded file text as context if available
    context = st.session_state.file_text
    messages = [{"role": "system", "content": f"You are an academic assistant. Use the following content to answer questions:\n{context}"}]
    # Append previous conversation for context
    messages.extend(st.session_state.messages)
    # Append user question
    messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# ------------------------------
# Step 6: Display Chat History (latest first)
# ------------------------------
st.subheader("Conversation (Latest messages at top)")
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

