# Academic Improvement Assistant
# Author: Karthika
# Description: Upload academic files (PDF, DOCX, TXT, JPG) and get AI suggestions or feedback.

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Optional imports for text documents
try:
    from PyPDF2 import PdfReader
    import docx
except ImportError:
    pass  # We'll handle missing modules gracefully

# ------------------------------
# Step 1: Load OpenAI API Key
# ------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Step 2: Streamlit Page Setup
# ------------------------------
st.set_page_config(page_title="📸 Academic Improvement Assistant", page_icon="🎓")
st.title("🎓 Academic Improvement Assistant")

st.write("Upload your academic work (PDF, DOCX, TXT, or JPG) and get personalized suggestions for improvement.")

# ------------------------------
# Step 3: Initialize Session
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Step 4: File Upload
# ------------------------------
uploaded_file = st.file_uploader(
    "📁 Upload your academic file or image:",
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"]
)

extracted_text = ""
image_uploaded = False
image_path = None

if uploaded_file:
    file_type = uploaded_file.type

    # PDF
    if file_type == "application/pdf":
        from PyPDF2 import PdfReader
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""

    # DOCX
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(uploaded_file)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])

    # TXT
    elif file_type == "text/plain":
        extracted_text = uploaded_file.read().decode("utf-8")

    # Image (JPG/PNG)
    elif "image" in file_type:
        image_uploaded = True
        image_path = f"temp_{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption="Uploaded Image", use_container_width=True)

    if extracted_text:
        st.success("✅ File text extracted successfully!")
    elif image_uploaded:
        st.success("✅ Image uploaded successfully!")

# ------------------------------
# Step 5: User Prompt
# ------------------------------
user_input = st.text_input("💬 Describe what you want feedback on (e.g., handwriting, content, clarity):")

if st.button("Get Suggestions") and uploaded_file:
    with st.spinner("Analyzing your work..."):

        # For text-based files
        if not image_uploaded:
            content = extracted_text if extracted_text else "No readable text found."
            messages = [
                {"role": "system", "content": "You are an academic advisor. Analyze the content and suggest areas of improvement."},
                {"role": "user", "content": f"Here is my work:\n{content}\nPlease give me detailed suggestions for improvement related to {user_input}."}
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            feedback = response.choices[0].message.content

        # For image-based files
        else:
            # Use GPT-4 with vision
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"This is my academic work. Please analyze the image and give suggestions for improvement related to: {user_input}."},
                            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{uploaded_file.getvalue().hex()}"}
                        ],
                    }
                ],
            )
            feedback = response.choices[0].message.content

    # Save and display feedback
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": feedback})
    st.success("✅ Feedback generated successfully!")

# ------------------------------
# Step 6: Display Chat
# ------------------------------
st.subheader("🗨️ Conversation (Latest First)")
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**👩‍🎓 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Assistant:** {msg['content']}")

