import streamlit as st
from text_utils import get_text

def display_styled_admin_page(title, description):
    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h2 style="
                color: #f9c61e;
                margin-bottom: 5px;
            ">{title}</h2>
            <p style="
                color: #666;
                font-style: italic;
                margin-bottom: 20px;
            ">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def back_to_admin_settings():
    if st.button(get_text("Zurück zu Admin-Einstellungen", "Back to Admin Settings")):
        st.session_state.admin_page = None
        st.rerun()