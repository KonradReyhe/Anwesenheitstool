#styles.py
import streamlit as st

VERSION = "1.0.0"

def apply_custom_styles():
    custom_css = """
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
    /* New styles for company and team info */
    .company-info {
        color: #000000; /* Adjust color to match your theme */
        font-size: 24px; /* Adjust size as needed */
        text-align: center;
        margin-bottom: 15px;
    }

    .team-info {
        color: #000000; /* Adjust color to match your theme */
        font-size: 24px; /* Adjust size as needed */
        text-align: center;
        margin-bottom: 15px;
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
        font-size: 24px;
        font-weight: bold;
        color: #f9c61e;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Company logo styles */
    .company-container {
        text-align: center;
        padding: 15px;
        margin: 15px;
    }
    .company-logo {
        width: 100%;
        max-width: 180px;
        display: block;
        margin: 0 auto 15px;
        pointer-events: none;
    }
    .company-divider {
        border-top: 1px solid #e0e0e0;
        margin: 20px 0;
    }
    /* Custom message styles */
    .custom-message {
        padding: 15px;
        margin-bottom: 25px;
        font-size: 20px;
        color: #0095be;
        text-align: center;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    /* Attendance table styles */
    .attendance-table {
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 15px;
    }
    /* Header layout */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
    }
    /* Banner style */
    .banner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
    }
    /* Language toggle button */
    .language-toggle {
        font-size: 18px;
        padding: 10px 15px;
        border-radius: 10px;
        background-color: #f9c61e;
        color: white;
        border: none;
        cursor: pointer;
    }
    .version-number {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 14px;
        color: #888888;
        opacity: 0.7;
    }
    .subtitle {
        color: #0095be;
        font-size: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .banner-container {
        width: 100%;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .banner-image {
        width: 100%;
        max-width: 100%;
        height: auto;
    }
    /* Flexbox alignment for admin panel */
    .admin-panel-container {
        display: flex;
        align-items: center;
    }

    .admin-panel-container .stTextInput > div > div > input {
        flex: 3;
    }

    .admin-panel-container .stButton > button {
        flex: 1;
        height: 50px; /* Adjust the height as needed */
    }

    /* Ensure the button and input have the same height */
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Add version number to the bottom of the page
    st.markdown(f"<div class='version-number'>v{VERSION}</div>", unsafe_allow_html=True)

# You can add more custom style functions here if needed




