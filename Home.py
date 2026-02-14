import streamlit as st
import PyPDF2

st.set_page_config(page_title="Study AI", page_icon="🎓", layout="wide")

import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)

# --- HERO SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🎓 AI Study Assistant")
    st.markdown("""
        <div style="padding-bottom: 2rem;">
            <h3>Unlock your potential with smart study tools.</h3>
            <p style="color: #64748b; font-size: 1.1rem;">
                Upload your study materials (PDF) and instantly access an AI-powered Chatbot, 
                Flashcards generator, and Quiz Master to master your subjects.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # You could add an illustration here if you had one, for now, we'll keep it simple or add a placeholder
    st.markdown('<div style="text-align: center; font-size: 5rem;">📚</div>', unsafe_allow_html=True)


# --- 1. FILE UPLOADER SECTION ---
st.markdown("---")
st.markdown("### 1. Upload Your Notes")

# Centering the uploader slightly or making it prominent
with st.container():
    uploaded_file = st.file_uploader("Drop your PDF here to get started", type=["pdf"])

if uploaded_file is not None:
    # --- 2. EXTRACT TEXT ---
    with st.spinner("Processing PDF..."):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Save to Session State (so other pages can use it)
            st.session_state.pdf_text = text
            
            # --- 3. SUCCESS UI ---
            st.success(f"✅ PDF Processed Successfully! Loaded {len(pdf_reader.pages)} pages.")
            
            # Action Cards
            st.markdown("### 2. Choose Your Tool")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.page_link("pages/chatbot.py", label="Chatbot", icon="🤖", use_container_width=True)
                st.caption("Ask questions about your notes.")
            with c2:
                st.page_link("pages/Flashcards.py", label="Flashcards", icon="⚡", use_container_width=True)
                st.caption("Generate cards for memorization.")
            with c3:
                st.page_link("pages/Quiz_master.py", label="Quiz Master", icon="❓", use_container_width=True)
                st.caption("Test your knowledge.")
            
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- 4. SIDEBAR INFO ---
with st.sidebar:
    st.header("Study AI Info")
    st.markdown("---")
    st.markdown("**Model:** Llama-3 (via Groq)")
    
    st.markdown("### Status")
    if "pdf_text" in st.session_state:
        st.success("📂 PDF Loaded & Ready")
    else:
        st.warning("📂 No PDF Loaded")
        
    st.markdown("---")
    st.markdown("Made with ❤️ by Study AI Team")