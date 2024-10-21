import streamlit as st
from utils import get_text
import os
import base64

def display_header():
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
                
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                error_message = get_text("Fehler beim Laden des Banners:", "Error loading banner:")
                st.error(f"{error_message} {e}")
        else:
            warning_message = get_text("Banner wurde nicht gefunden:", "Banner not found:")
            st.warning(f"{warning_message} {banner_path}")

    return header_container