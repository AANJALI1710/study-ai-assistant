# Study AI Assistant 🎓

An AI-powered application to help students study smarter. Upload your PDF notes and get instant access to a chatbot, flashcards, and quizzes.
## 🔗 Live Demo
**Access the application here:** [https://study-ai-assistant.streamlit.app/](https://study-ai-assistant.streamlit.app/)

## Features

- **🤖 Chatbot**: Ask questions about your notes and get processed answers using Llama-3.
- **⚡ Flashcards**: Automatically generate flashcards from your study materials to aid memorization.
- **❓ Quiz Master**: Test your knowledge with AI-generated quizzes (Multiple Choice or True/False).
- **🎨 Modern UI**: Features a clean interface with Light and Dark variants.

## Tech Stack

- **Streamlit**: For the interactive web application.
- **Groq API (Llama-3)**: For fast and accurate AI responses.
- **PyPDF2**: For PDF text extraction.

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your secrets:
   - Create a `.streamlit/secrets.toml` file.
   - Add your Groq API key: `GROQ_API_KEY = "your_key_here"`
4. Run the app:
   ```bash
   streamlit run Home.py
   ```

## Usage

1. **Upload**: Drag and drop your PDF notes on the Home page.
2. **Select Tool**: Choose from Chatbot, Flashcards, or Quiz Master from the sidebar or the home page links.
3. **Study**: Interact with the AI to master your subject!
