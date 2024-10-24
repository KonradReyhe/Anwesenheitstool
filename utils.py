# utils.py

import streamlit as st
import zipfile
import os
from datetime import datetime
import pytz
import time
from email_utils import send_documents_to_accounting
from config import VERSION
from text_utils import get_text  
import asyncio


local_tz = pytz.timezone('Europe/Berlin')

def create_zip_file(files, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))

def end_get_together():
    from attendance import save_attendance
    zip_file_name = save_attendance()
    if zip_file_name:
        email_sent = send_documents_to_accounting(zip_file_name)
        if email_sent:
            st.success(get_text("GetTogether wurde beendet und E-Mail wurde gesendet.", "GetTogether has been ended and email was sent."))
        else:
            st.warning(get_text("GetTogether wurde beendet, aber E-Mail wurde nicht gesendet.", "GetTogether has been ended, but email was not sent."))
        os.remove(zip_file_name)
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern.", "No attendance data to save."))
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.rerun()

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

async def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()
    await asyncio.sleep(0)  

@st.cache_data(ttl=60)  
def display_countdown_timer():
    if 'scheduled_end_time' in st.session_state and st.session_state.scheduled_end_time:
        now = datetime.now()
        time_left = st.session_state.scheduled_end_time - now
        if time_left.total_seconds() > 0:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return get_text("Zeit abgelaufen", "Time's up")
    return ""

def cancel_scheduled_end():
    st.session_state.scheduled_end_time = None

def trigger_rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def toggle_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'
    
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'
    st.rerun()

def update_last_activity():
    st.session_state.last_activity_time = time.time()




