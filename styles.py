#styles.py
import streamlit as st

VERSION = "1.0.0"

def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* General styles */
        body {
            font-family: Arial, sans-serif;
            background-color: #FFFFFF;
        }
        .title {
            color: #f9c61e;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin: 30px 0;
        }
        .sub-header {
            color: #0095be;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 25px;
        }
        .important-text {
            color: #000000;
            font-size: 24px;
            text-align: center;
            margin-bottom: 25px;
        }
        /* Button styles */
        .stButton > button {
            border-radius: 15px;
            font-size: 20px;
            padding: 20px;
            min-height: 70px;
            width: 100%;
            border: 2px solid #f9c61e;
            background-color: #FFFFFF;
            color: #0095be;
            text-align: center;
            white-space: normal;
            word-wrap: break-word;
            box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #f9c61e;
            color: #ffffff;
            transform: translateY(-2px);
        }
        /* Input field styles */
        .stTextInput > div > div > input {
            border-radius: 15px;
            font-size: 20px;
            padding: 15px;
            border: 2px solid #0095be;
            background-color: #f9f9f9;
            color: #000000;
        }
        .event-name {
            color: #f9c61e;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        /* Add any other styles from app.py here */
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Add version number to the page
    st.markdown(f'<div class="version">v{VERSION}</div>', unsafe_allow_html=True)

# You can add more custom style functions here if needed
