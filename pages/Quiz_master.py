import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Quiz Master", page_icon="❓")

# --- 1. SAFETY CHECKS ---
if "pdf_text" not in st.session_state:
    st.warning("🚨 No notes found! Please upload a PDF on the Home page first.")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API Key Error. Please check your secrets.toml file.")
    st.stop()

st.title("❓ Quiz Master")
st.markdown("Test your knowledge before the exams.")

# --- 2. GENERATE QUIZ BUTTON ---
if st.button("🚀 Generate New Quiz"):
    with st.spinner("Analyzing notes and creating questions..."):
        
        # PROMPT DESIGN
        # We limit text to 15,000 characters to prevent "Rate Limit" crashes
        truncated_text = st.session_state.pdf_text[:15000]
        
        prompt = """
        Create 5 multiple choice questions based on the text provided.
        Format the output strictly as a JSON array of objects.
        
        Example Format:
        [
            {
                "q": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "answer": "C",
                "explanation": "Paris is the capital of France."
            }
        ]
        """
        
        try:
            # Call Gemini
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Context: {truncated_text}\n\n{prompt}")
            
            # Clean up the response (remove markdown backticks if Gemini adds them)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            # Save to Session State
            st.session_state.quiz_data = json.loads(clean_text)
            st.session_state.quiz_generated = True
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating quiz: {e}")

# --- 3. DISPLAY QUIZ (With The Logic Fix) ---
if "quiz_generated" in st.session_state:
    
    # Loop through each question
    for i, q in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}: {q['q']}")
        
        # Display Options
        # The 'choice' variable will hold the text user clicked (e.g., "Paris")
        choice = st.radio("Select an answer:", q["options"], key=f"q_{i}", index=None)
        
        # CHECK ANSWER LOGIC
        if choice:
            # 1. Find the index of the user's choice (0, 1, 2, or 3)
            user_index = q["options"].index(choice)
            
            # 2. Convert index to Letter (0->A, 1->B, 2->C, 3->D)
            letter_map = ['A', 'B', 'C', 'D']
            user_letter = letter_map[user_index]
            
            # 3. Compare user_letter with the correct answer key
            if user_letter == q['answer']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer was **Option {q['answer']}**.")
                st.info(f"💡 **Explanation:** {q['explanation']}")
        
        st.divider()