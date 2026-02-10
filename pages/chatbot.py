import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="ChatBot", page_icon="💬")

if "pdf_text" not in st.session_state or st.session_state.pdf_text == "":
    st.warning("🚨 No notes found! Please go to the 'Home' page and upload a PDF first.")
    st.stop()

# --- STABLE SETUP (Use this exactly) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"🚨 API Key Error: {e}")
    st.stop()

st.title("💬 Chat with Gemini")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # We use 'gemini-pro' because it is 100% stable
                model = genai.GenerativeModel('gemini-pro')
                
                full_prompt = f"""
                Context: {st.session_state.pdf_text}
                
                Question: {prompt}
                """
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")