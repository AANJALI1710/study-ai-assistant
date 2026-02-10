import streamlit as st
import PyPDF2

# Page Config
st.set_page_config(page_title="StudyBuddy Home", page_icon="🏠", layout="wide")

st.title("🏠 Welcome to AI Study Buddy")
st.markdown("### *Step 1: Upload your notes to unlock the tools.*")

# --- INITIALIZE SESSION STATE ---
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# --- HELPER FUNCTION ---
def get_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📂 Upload PDF Notes", type="pdf")

if uploaded_file:
    with st.spinner("Analyzing document..."):
        text = get_pdf_text(uploaded_file)
        st.session_state.pdf_text = text
        st.success("✅ Notes Processed! Select a tool from the sidebar to start.")
        st.balloons()
else:
    st.info("👈 Waiting for file...")

# --- OPTIONAL: SIDEBAR INSTRUCTIONS ---
with st.sidebar:
    st.markdown("### 🤖 Powered by Gemini 1.5")
    st.info("Upload a PDF to enable Chat, Flashcards, and Quizzes.")