import streamlit as st
from groq import Groq
import os
import json

st.set_page_config(page_title="Quiz Master", page_icon="❓")

# 1. SAFETY CHECKS
if "pdf_text" not in st.session_state or st.session_state.pdf_text == "":
    st.warning("🚨 No notes found! Please go to the 'Home' page and upload a PDF first.")
    st.stop()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("🚨 API Key not found!")
    st.stop()

client = Groq(api_key=api_key)

st.title("❓ Quiz Master")
st.markdown("### *Test your knowledge before the exams.*")

# 2. QUIZ SETTINGS
col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])
with col2:
    num_questions = st.slider("Number of Questions:", 3, 10, 5)

# 3. GENERATE QUIZ BUTTON
if st.button("🚀 Generate New Quiz"):
    with st.spinner(f"Creating {difficulty} questions..."):
        try:
            # STRICT JSON PROMPT
            prompt = f"""
            Create {num_questions} multiple-choice questions (difficulty: {difficulty}) based on the text.
            Return a JSON object strictly in this format:
            {{
                "questions": [
                    {{
                        "q": "Question text here?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "answer": "Option A",
                        "explanation": "Why this is correct."
                    }}
                ]
            }}
            """
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": f"Context: {st.session_state.pdf_text}\n\n{prompt}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Save quiz to session state so it doesn't disappear when you click buttons
            data = json.loads(completion.choices[0].message.content)
            st.session_state.quiz_data = data["questions"]
            st.session_state.quiz_generated = True
            st.rerun() # Refresh to show questions
            
        except Exception as e:
            st.error(f"Error generating quiz: {e}")

# 4. DISPLAY QUIZ (If it exists)
if "quiz_generated" in st.session_state and st.session_state.quiz_generated:
    
    score = 0
    
    for i, q in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Q{i+1}: {q['q']}**")
        
        # Unique key for each question's radio button
        user_choice = st.radio(
            f"Select an answer for Q{i+1}:", 
            q["options"], 
            key=f"q_{i}", 
            index=None # No default selection
        )
        
        # Check Answer logic
        if user_choice:
            if user_choice == q["answer"]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. The answer was: {q['answer']}")
            
            # Show explanation only after answering
            with st.expander("Show Explanation"):
                st.info(q["explanation"])
        
        st.divider()

    # Final Score Button
    if st.button("🏁 Finish Quiz"):
        st.markdown(f"## Your Score: {score}/{len(st.session_state.quiz_data)}")
        if score == len(st.session_state.quiz_data):
            st.balloons()