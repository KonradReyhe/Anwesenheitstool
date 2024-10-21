#utils.py
import streamlit as st
import zipfile
import os
from datetime import datetime, timedelta
import pandas as pd
import base64
import io
from PIL import Image
import time
from session_state import initialize_session_state
from pdf_utils import generate_pdf
import pytz
from save_operations import save_attendance
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from text_utils import get_text
from email_utils import send_documents_to_accounting
from config import VERSION
from app_functions import admin_panel


local_tz = pytz.timezone('Europe/Berlin')

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
                    st.rerun()
            
            language_toggle = "EN" if st.session_state.language == 'DE' else "DE"
            st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    st.markdown(f"<div class='version-number'>v{VERSION}</div>", unsafe_allow_html=True)

    if st.session_state.get('show_admin_panel', False):
        admin_panel()

    return header_container


def auto_save_attendance():
    if st.session_state.attendance_data:
        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')
        st.session_state.last_auto_save = datetime.now()

def create_zip_file(files, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))

def end_get_together():
    """
    End the current GetTogether event.
    
    This function saves the attendance data, resets the session state,
    and displays a success message to the user.
    """
    zip_file_name = save_attendance()
    if zip_file_name:
        send_documents_to_accounting(zip_file_name)
        os.remove(zip_file_name)  # Clean up after sending
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.success(get_text("GetTogether wurde beendet.", "GetTogether has been ended."))
    st.experimental_rerun()



def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.experimental_rerun()

def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def display_countdown_timer():
    if 'scheduled_end_time' in st.session_state and st.session_state.scheduled_end_time:
        now = datetime.now()
        time_left = st.session_state.scheduled_end_time - now
        if time_left.total_seconds() > 0:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.write(f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            st.write(get_text("Zeit abgelaufen", "Time's up"))

def cancel_scheduled_end():
    st.session_state.scheduled_end_time = None

def trigger_rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def toggle_language():
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'
    st.success(get_text("Sprache wurde geändert.", "Language has been changed."))
    st.rerun()

def save_attendance():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        df.to_csv(file_name, index=False)
        
        pdf_file_name = f"Anwesenheit_{timestamp}.pdf"
        generate_pdf(st.session_state.attendance_data, pdf_file_name)
        
        zip_file_name = f"Anwesenheit_{timestamp}.zip"
        create_zip_file([file_name, pdf_file_name], zip_file_name)
        
        with open(zip_file_name, "rb") as file:
            btn = st.download_button(
                label="Download Anwesenheitsliste",
                data=file,
                file_name=zip_file_name,
                mime="application/zip"
            )
        
        os.remove(file_name)
        os.remove(pdf_file_name)
        os.remove(zip_file_name)
        
        return zip_file_name
    return False

def update_last_activity():
    st.session_state.last_activity_time = time.time()

def show_custom_employee_message(employee):
    if employee in st.session_state.custom_employee_messages:
        st.markdown("### " + get_text("Wichtige Mitteilung", "Important Notice"))
        st.write(st.session_state.custom_employee_messages[employee])
        if st.button(get_text("Schließen", "Close"), key="close_custom_message"):
            st.session_state.show_custom_message = False
            st.rerun()
