import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="ChatBot", page_icon="💬")

# --- CHECK IF DATA EXISTS ---
if "pdf_text" not in st.session_state or st.session_state.pdf_text == "":
    st.warning("🚨 No notes found! Please go to the 'Home' page and upload a PDF first.")
    st.stop()

# --- SETUP CLIENT ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.title("💬 Chat with your Notes")

# Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        messages = [{"role": "system", "content": "You are a tutor."}] + st.session_state.messages
        messages.append({"role": "user", "content": f"Context: {st.session_state.pdf_text}\n\nQuestion: {prompt}"})
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})