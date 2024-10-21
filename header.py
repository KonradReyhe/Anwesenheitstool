# header.py

import streamlit as st
from text_utils import get_text
from utils import toggle_language
import os
import base64

def display_header():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'

    header_container = st.container()

    with header_container:
        title = get_text("GetTogether Anwesenheitstool", "GetTogether Attendance Tool")
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
        # Updated subtitle
        subtitle = get_text("Präsenz bei Firmenevents erfassen", "Record presence at company events")
        st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)
        
        # Banner
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
        if os.path.exists(banner_path):
            try:
                # Read the image file as binary data
                with open(banner_path, "rb") as f:
                    banner_image = f.read()
                
                # Encode the image data to base64
                encoded_image = base64.b64encode(banner_image).decode()
                
                # Create HTML for the image
                html = f"""
                <style>
                    .banner-container {{
                        width: 100%;
                        margin-bottom: 20px;
                    }}
                    .banner-image {{
                        width: 100%;
                        max-width: 100%;
                        height: auto;
                    }}
                </style>
                <div class="banner-container">
                    <img src="data:image/png;base64,{encoded_image}" class="banner-image" alt="Health Innovators Group Leipzig Banner">
                </div>
                """
                
                # Display the HTML
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                error_message = get_text("Fehler beim Laden des Banners:", "Error loading banner:")
                st.error(f"{error_message} {e}")
        else:
            warning_message = get_text("Banner wurde nicht gefunden:", "Banner not found:")
            st.warning(f"{warning_message} {banner_path}")

        # Admin settings button and language toggle
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.session_state.get_together_started:
                if st.button("⚙️", key="settings_button", help=get_text("Admin-Einstellungen", "Admin Settings")):
                    st.session_state.show_admin_panel = not st.session_state.show_admin_panel
                    st.rerun()
            
            language_toggle = "EN" if st.session_state.language == 'DE' else 'DE'
            st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    return header_container
