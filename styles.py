import streamlit as st

def get_theme_colors(theme):
    if theme == "Dark":
        return {
            "bg_gradient": "linear-gradient(to bottom right, #0f172a, #1e293b)",
            "text_color": "#f1f5f9",
            "sidebar_bg": "#1e293b",
            "sidebar_text": "#f8fafc",
            "card_bg": "#334155",
            "card_border": "#475569",
            "input_bg": "#334155",
            "input_border": "#475569",
            "uploader_bg": "#1e293b",
            "uploader_border": "#475569",
            "success_bg": "rgba(16, 185, 129, 0.2)",
            "success_border": "#059669",
            "success_text": "#ecfdf5",
            "error_bg": "rgba(239, 68, 68, 0.2)",
            "error_border": "#b91c1c",
            "error_text": "#fef2f2",
            "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)"
        }
    else: # Light
        return {
            "bg_gradient": "linear-gradient(to bottom right, #f8fafc, #eef2ff)",
            "text_color": "#1e293b",
            "sidebar_bg": "#ffffff",
            "sidebar_text": "#334155",
            "card_bg": "#ffffff",
            "card_border": "#e2e8f0",
            "input_bg": "#ffffff",
            "input_border": "#cbd5e1",
            "uploader_bg": "#f8fafc",
            "uploader_border": "#cbd5e1",
            "success_bg": "#ecfdf5",
            "success_border": "#10b981",
            "success_text": "#065f46",
            "error_bg": "#fef2f2",
            "error_border": "#ef4444",
            "error_text": "#991b1b",
            "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
        }

def display_theme_toggle():
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    with st.sidebar:
        st.session_state.theme = st.selectbox(
            "🎨 Theme", 
            ["Light", "Dark"], 
            index=0 if st.session_state.theme == "Light" else 1
        )
    
    return st.session_state.theme

def apply_custom_styles(theme="Light"):
    colors = get_theme_colors(theme)
    
    st.markdown(f"""
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

            /* Global Styles */
            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif;
            }}

            /* Main Background & Text */
            .stApp {{
                background: {colors["bg_gradient"]};
                color: {colors["text_color"]};
            }}

            p, li, label, .stMarkdown {{
                color: {colors["text_color"]};
            }}

            /* Headings */
            h1, h2, h3, h4, h5, h6 {{
                color: {colors["text_color"]} !important;
                font-weight: 700;
            }}
            
            h1 {{
                background: -webkit-linear-gradient(45deg, #4f46e5, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                padding-bottom: 0.2rem;
            }}

            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {colors["sidebar_bg"]};
                border-right: 1px solid {colors["card_border"]};
                box-shadow: 2px 0 5px rgba(0,0,0,0.02);
            }}
            
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span {{
                 color: {colors["sidebar_text"]} !important;
            }}

            /* Buttons */
            .stButton > button {{
                background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%);
                color: white !important;
                border: none;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2), 0 2px 4px -1px rgba(79, 70, 229, 0.1);
            }}

            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3), 0 4px 6px -2px rgba(79, 70, 229, 0.15);
                color: white !important;
            }}

            /* Inputs */
            .stTextInput > div > div > input, .stSelectbox > div > div {{
                border-radius: 8px;
                border: 1px solid {colors["input_border"]};
                background-color: {colors["input_bg"]};
                color: {colors["text_color"]};
            }}

            /* Cards / Containers */
            /* Custom Card Style Class (to be used with st.markdown specific divs) */
            .custom-card {{
                background-color: {colors["card_bg"]};
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: {colors["shadow"]};
                margin-bottom: 1rem;
                border: 1px solid {colors["card_border"]};
            }}
            
            .custom-card h3, .custom-card h4 {{
                color: {colors["text_color"]} !important;
            }}
            
            .custom-card p {{
                color: {colors["text_color"]};
            }}

            /* File Uploader */
            [data-testid="stFileUploader"] {{
                padding: 2rem;
                border: 2px dashed {colors["uploader_border"]};
                border-radius: 12px;
                background-color: {colors["uploader_bg"]};
                text-align: center;
                transition: border-color 0.3s ease;
            }}
             [data-testid="stFileUploader"]:hover {{
                border-color: #4f46e5;
             }}
             [data-testid="stFileUploader"] section {{
                color: {colors["text_color"]};
             }}
             
            /* Quiz Feedback */
            .success-box {{
                padding: 1rem;
                background-color: {colors["success_bg"]};
                border: 1px solid {colors["success_border"]};
                color: {colors["success_text"]};
                border-radius: 8px;
                margin-top: 0.5rem;
            }}
            .error-box {{
                padding: 1rem;
                background-color: {colors["error_bg"]};
                border: 1px solid {colors["error_border"]};
                color: {colors["error_text"]};
                border-radius: 8px;
                margin-top: 0.5rem;
            }}
            
        </style>
    """, unsafe_allow_html=True)
