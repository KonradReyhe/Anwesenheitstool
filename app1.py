# app1.py

"""
app1.py

This is the main application file for the GetTogether attendance system.
It sets up the Streamlit interface, handles the main application flow,
and integrates various components of the system.
"""

# Import required libraries and modules
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pytz
from streamlit.runtime.scriptrunner import RerunException, StopException
import asyncio
import logging

# Import custom modules and functions
from auth import start_get_together_callback, datenschutz_pin_page
from ui_components import (
    select_company, select_team, select_employee, guest_info
)
from header import display_header
from session_state import initialize_session_state
from styles import apply_custom_styles
from utils import check_event_end
from text_utils import get_text
from admin import admin_settings
from attendance import auto_save_attendance

# Set up timezone for Berlin (used throughout the application)
local_tz = pytz.timezone('Europe/Berlin')

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home():
    """
    Display the home page of the GetTogether application.

    This function sets up the main interface for starting a new GetTogether event,
    including PIN setup, event name input, and data protection settings.
    It uses Streamlit components to create an interactive form for user input.
    """
    # Display the header of the application
    display_header()
    
    # Add a subheader for the configuration section
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether konfigurieren:', 'Configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    # Create a form for user input
    with st.form(key='start_gettogether_form'):
        # Create two columns for PIN input
        col1, col2 = st.columns(2)
        with col1:
            pin1 = st.text_input(get_text("Setzen Sie einen PIN:", "Set a PIN:"), type="password", key="pin1")
        with col2:
            pin2 = st.text_input(get_text("Bestätigen Sie den PIN:", "Confirm the PIN:"), type="password", key="pin2")
        
        # Input field for custom event name
        custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
        
        # Input field for data protection PIN
        datenschutz_pin = st.text_input(get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), type="password", key="datenschutz_pin_input")
        
        # Checkbox for requiring employee signature
        require_signature = st.checkbox(get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), value=st.session_state.get('require_signature', False), key="require_signature_checkbox")
        
        # Submit button to start GetTogether
        if st.form_submit_button(get_text("GetTogether beginnen", "Start GetTogether")):
            start_get_together_callback()

def navigate():
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company':
        select_company()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'admin_settings':
        if st.session_state.get('admin_access_granted', False):
            admin_settings()
        else:
            st.session_state.page = 'select_company'
    elif st.session_state.page == 'datenschutz_pin':
        datenschutz_pin_page()
    else:
        st.error("Invalid page")

async def main():
    try:
        initialize_session_state()
        apply_custom_styles()
        
        if not st.session_state.get('get_together_started', False):
            home()
        else:
            navigate()
        
        await check_event_end()
        
        asyncio.create_task(periodic_auto_save())
        
        st_autorefresh(interval=30000, key="datarefresh")
    except (RerunException, StopException):
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        st.error(f"An unexpected error occurred: {str(e)}")
        st.stop()

async def periodic_auto_save():
    while True:
        auto_save_attendance()
        await asyncio.sleep(300) 

if __name__ == "__main__":
    asyncio.run(main())
