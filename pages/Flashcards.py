import streamlit as st
from groq import Groq
import pandas as pd
import json
import os

st.set_page_config(page_title="Flashcards", page_icon="⚡")

# 1. CHECK IF NOTES EXIST
if "pdf_text" not in st.session_state or st.session_state.pdf_text == "":
    st.warning("🚨 No notes found! Please go to the 'Home' page and upload a PDF first.")
    st.stop()

st.title("⚡ Smart Flashcards")

# 2. LOAD API KEY SAFELY (The Fix)
try:
    # Try loading from secrets.toml
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    # If that fails, try environment variable
    api_key = os.environ.get("GROQ_API_KEY")

# 3. STOP IF NO KEY FOUND
if not api_key:
    st.error("🚨 API Key not found! Please check that your '.streamlit/secrets.toml' file exists in the main project folder.")
    st.stop()

# 4. INITIALIZE CLIENT
client = Groq(api_key=api_key)

# 5. THE APP LOGIC
if st.button("Generate New Deck"):
    with st.spinner("Extracting concepts..."):
        prompt = """
        Extract 10 key terms and definitions. 
        Return strictly valid JSON in this format:
        {"cards": [{"term": "Concept", "def": "Definition"}]}
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": f"Context: {st.session_state.pdf_text}\n\n{prompt}"}
                ],
                response_format={"type": "json_object"}
            )
            
            data = json.loads(completion.choices[0].message.content)
            df = pd.DataFrame(data["cards"])
            st.data_editor(df, num_rows="dynamic", use_container_width=True)
            
            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "cards.csv", "text/csv")
            
        except Exception as e:
            st.error(f"Error generating cards: {e}")