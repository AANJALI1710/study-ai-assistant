import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

st.set_page_config(page_title="Flashcards", page_icon="⚡")

if "pdf_text" not in st.session_state or st.session_state.pdf_text == "":
    st.warning("🚨 Upload notes first!")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API Key Missing")
    st.stop()

st.title("⚡ Smart Flashcards")

if st.button("Generate Deck"):
    with st.spinner("Generating..."):
        # We ask for raw text and parse it manually to be safe
        prompt = """
        Extract 5 terms and definitions.
        Format strictly as JSON: [{"term": "Concept", "def": "Definition"}]
        """
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Context: {st.session_state.pdf_text}\n\n{prompt}")
            
            # clean up response (sometimes Gemini adds ```json markdown)
            clean_text = response.text.replace("```json", "").replace("```", "")
            
            data = json.loads(clean_text)
            df = pd.DataFrame(data)
            st.data_editor(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 CSV", csv, "cards.csv", "text/csv")
        except Exception as e:
            st.error(f"Error: {e}")