import streamlit as st
from groq import Groq
import os
import json

st.set_page_config(page_title="Quiz Master", page_icon="❓", layout="wide")

import styles
import sys

# Ensure we can import styles if it's in the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)


# --- 1. SETUP GROQ CLIENT ---
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ API Key Error: {e}")
    st.stop()

if "pdf_text" not in st.session_state:
    st.warning("🚨 No notes found! Please upload a PDF on the Home page first.")
    st.stop()

st.title("❓ Quiz Master")
st.markdown("### *Customize your practice session.*")

# --- 2. QUIZ SETTINGS ---
with st.expander("⚙️ Quiz Settings", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
    
    with col2:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        
    with col3:
        quiz_type = st.selectbox("Question Type", ["Multiple Choice", "True/False"])

# --- 3. GENERATE QUIZ ---
if st.button("🚀 Generate Quiz", use_container_width=True):
    with st.spinner("🧠 Analyzing notes and crafting questions..."):
        try:
            # SAFETY TRUNCATION
            safe_text = st.session_state.pdf_text[:15000] 
            
            # Dynamic Prompt Construction
            type_instruction = ""
            if quiz_type == "True/False":
                type_instruction = "The 'options' array must ONLY contain ['True', 'False']."
            else:
                type_instruction = "The 'options' array must contain 4 distinct choices."

            prompt = f"""
            Create {num_questions} {difficulty} questions based on this text:
            {safe_text}
            
            Question Type: {quiz_type}
            
            Return a JSON Array ONLY. No markdown. Format:
            [
                {{"q": "Question?", "options": ["Option1", "Option2"], "answer": "Option1", "explanation": "Why..."}}
            ]
            
            Constraint: {type_instruction}
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                stop=None
            )
            
            raw_json = completion.choices[0].message.content
            clean_json = raw_json.replace("```json", "").replace("```", "").strip()
            
            st.session_state.quiz_data = json.loads(clean_json)
            st.session_state.quiz_generated = True
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. DISPLAY QUIZ ---
if "quiz_generated" in st.session_state:
    score = 0
    total = len(st.session_state.quiz_data)
    
    for i, q in enumerate(st.session_state.quiz_data):
        st.markdown(f"""
        <div class="custom-card">
            <h4 style="color: #4f46e5;">Question {i+1}</h4>
            <p style="font-size: 1.1rem; font-weight: 500;">{q['q']}</p>
        </div>
        """, unsafe_allow_html=True)

        
        choice = st.radio(f"Select answer for Q{i+1}:", q["options"], key=f"q_{i}", index=None, label_visibility="collapsed")
        
        if choice:
            # Flexible checking: "Option A" OR just "True" matches
            if choice == q['answer'] or choice.startswith(q['answer']):
                st.markdown('<div class="success-box">✅ <b>Correct!</b></div>', unsafe_allow_html=True)
                score += 1
            else:
                st.markdown(f'<div class="error-box">❌ <b>Incorrect.</b><br>Answer: {q["answer"]}</div>', unsafe_allow_html=True)
                with st.expander("💡 View Explanation"):
                    st.info(q['explanation'])
        st.divider()

    if st.button("🏁 Check Final Score"):
        if score == total:
            st.success(f"🎉 Perfect Score! {score}/{total}")
        else:
            st.info(f"You got {score}/{total} correct.")