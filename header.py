# header.py

"""
This module contains functions for displaying the header of the GetTogether application.
"""

import streamlit as st
from text_utils import get_text
from utils import toggle_language
import os
import base64

def display_header():
    """
    Display the header of the GetTogether application.
    This includes the logo and any other header elements.
    """
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'

    header_container = st.container()

    with header_container:
        title = get_text("GetTogether Anwesenheitstool", "GetTogether Attendance Tool")
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
        subtitle = get_text("Präsenz bei Firmenevents erfassen", "Record presence at company events")
        st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
        if os.path.exists(banner_path):
            try:
                with open(banner_path, "rb") as f:
                    banner_image = f.read()
                
                encoded_image = base64.b64encode(banner_image).decode()
                
                html = f"""
                <div class="banner-container">
                    <img src="data:image/png;base64,{encoded_image}" class="banner-image" alt="Health Innovators Group Leipzig Banner">
                </div>
                """
                
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                error_message = get_text("Fehler beim Laden des Banners:", "Error loading banner:")
                st.error(f"{error_message} {e}")
        else:
            warning_message = get_text("Banner wurde nicht gefunden:", "Banner not found:")
            st.warning(f"{warning_message} {banner_path}")

        col1, col2 = st.columns([9, 1])
        with col2:
            if st.session_state.get('get_together_started', False):
                if st.button("⚙️", key="settings_button", help=get_text("Admin-Einstellungen", "Admin Settings")):
                    st.session_state.show_admin_panel = not st.session_state.get('show_admin_panel', False)
            if st.button("🌐", key="language_toggle", help=get_text("Sprache ändern", "Change Language")):
                toggle_language()

    return header_container

def display_language_toggle():
    current_language = st.session_state.get('language', 'de')
    language_text = "🇬🇧 EN" if current_language == 'de' else "🇩🇪 DE"
    
    with st.form(key="language_form", clear_on_submit=True):
        if st.form_submit_button(language_text, use_container_width=True):
            toggle_language()
