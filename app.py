import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# Optional imports for text documents
try:
    from PyPDF2 import PdfReader
    import docx
except ImportError:
    pass

# ------------------------------
# Load API Key
# ------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Add it to your .env file.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Streamlit Page Setup
# ------------------------------
st.set_page_config(page_title="📸 Academic Improvement Assistant", page_icon="🎓")
st.title("🎓 Academic Improvement Assistant")

st.write("Upload your academic work (PDF, DOCX, TXT, or JPG/PNG) and get personalized suggestions for improvement.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# File Upload
# ------------------------------
uploaded_file = st.file_uploader(
    "📁 Upload your academic file or image:",
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"]
)

extracted_text = ""
image_uploaded = False
base64_image = None

if uploaded_file:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        from PyPDF2 import PdfReader
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(uploaded_file)
        extracted_text = "\n".join([p.text for p in doc.paragraphs])

    elif file_type == "text/plain":
        extracted_text = uploaded_file.read().decode("utf-8")

    elif "image" in file_type:
        image_uploaded = True
        bytes_data = uploaded_file.read()
        base64_image = base64.b64encode(bytes_data).decode("utf-8")
        st.image(bytes_data, caption="Uploaded Image", use_container_width=True)

    if extracted_text:
        st.success("✅ File text extracted successfully!")
    elif image_uploaded:
        st.success("✅ Image uploaded successfully!")

# ------------------------------
# User Prompt
# ------------------------------
user_input = st.text_input("💬 Describe what you want feedback on (e.g., handwriting, content, clarity):")

if st.button("Get Suggestions") and uploaded_file:
    with st.spinner("Analyzing your work..."):

        if not image_uploaded:
            content = extracted_text if extracted_text else "No readable text found."
            messages = [
                {"role": "system", "content": "You are an academic advisor. Analyze the text and give improvement suggestions."},
                {"role": "user", "content": f"Here is my work:\n{content}\nPlease provide detailed feedback about {user_input}."}
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            feedback = response.choices[0].message.content

        else:
            # Use GPT-4 with Vision — correctly encoded image
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Please analyze this image of my academic work and suggest improvements about: {user_input}."},
                            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                        ]
                    }
                ],
            )
            feedback = response.choices[0].message.content

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": feedback})
    st.success("✅ Feedback generated successfully!")

# ------------------------------
# Display Chat
# ------------------------------
st.subheader("🗨️ Conversation (Latest First)")
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**👩‍🎓 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Assistant:** {msg['content']}")

   
