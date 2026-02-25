import streamlit as st
import PyPDF2

st.set_page_config(page_title="Study AI", page_icon=None, layout="wide")

import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)

# --- HERO SECTION ---
col1, col2 = st.columns([3, 1])

with col1:
    st.title("Study AI Assistant")
    st.markdown("""
        <div style="padding-bottom: 2rem;">
            <h3 style="font-weight: 400; color: #64748b;">Unlock your potential with smart study tools.</h3>
            <p style="font-size: 1.1rem;">
                Upload your study materials and instantly access an AI-powered Chatbot, 
                Flashcards generator, and Quiz Master to master your subjects.
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- 1. FILE UPLOADER SECTION ---
st.divider()
st.subheader("1. Upload Your Notes")

# Centering the uploader slightly or making it prominent
with st.container():
    uploaded_file = st.file_uploader("Upload your PDF document to get started", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    # --- 2. EXTRACT TEXT ---
    with st.spinner("Processing document..."):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Save to Session State (so other pages can use it)
            st.session_state.pdf_text = text
            
            # --- 3. SUCCESS UI ---
            st.success(f"Document processed. {len(pdf_reader.pages)} pages loaded.")
            
            # Action Cards
            st.divider()
            st.subheader("2. Choose Your Tool")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.page_link("pages/chatbot.py", label="Study Chatbot", use_container_width=True)
                st.caption("Ask questions about your notes.")
            with c2:
                st.page_link("pages/Flashcards.py", label="Generate Flashcards", use_container_width=True)
                st.caption("Create cards for memorization.")
            with c3:
                st.page_link("pages/Quiz_master.py", label="Quiz Master", use_container_width=True)
                st.caption("Test your knowledge.")
            
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- 4. SIDEBAR INFO ---
with st.sidebar:
    st.title("Study AI")
    st.divider()
    st.markdown("**Model:** Llama-3 (Groq)")
    
    st.markdown("### Status")
    if "pdf_text" in st.session_state:
        st.info("Document Loaded")
    else:
        st.write("No document uploaded")
        
    st.divider()
    st.caption("Study AI Assistant")
