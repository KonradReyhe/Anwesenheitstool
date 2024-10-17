import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="streamlit")
import pandas as pd
import os
from datetime import datetime, timedelta
import threading
import uuid
import time
from math import ceil
import base64
from streamlit_autorefresh import st_autorefresh
import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from streamlit_drawable_canvas import st_canvas
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from streamlit.runtime.scriptrunner import RerunException
import pytz

VERSION = "1.0.0"

local_tz = pytz.timezone('Europe/Berlin')  # German timezone

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
        font-size: 36px;  /* Increased font size */
        font-weight: bold;
        text-align: center;
        margin: 30px 0;  /* Increased margin */
    }
    .sub-header {
        color: #0095be;
        font-size: 28px;  /* Increased font size */
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;  /* Increased margin */
    }
    .important-text {
        color: #000000;
        font-size: 24px;  /* Increased font size */
        text-align: center;
        margin-bottom: 25px;  /* Increased margin */
    }
    /* Button styles */
    .stButton > button {
        border-radius: 15px;  /* Increased border radius */
        font-size: 20px;  /* Increased font size */
        padding: 20px;  /* Increased padding */
        min-height: 70px;  /* Increased minimum height */
        width: 100%;
        border: 2px solid #f9c61e;
        background-color: #FFFFFF;
        color: #0095be;
        text-align: center;
        white-space: normal;
        word-wrap: break-word;
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);  /* Increased shadow */
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #f9c61e;
        color: #ffffff;
        transform: translateY(-2px);  /* Slight lift effect on hover */
    }
    /* Input field styles */
    .stTextInput > div > div > input {
        border-radius: 15px;  /* Increased border radius */
        font-size: 20px;  /* Increased font size */
        padding: 15px;  /* Increased padding */
        border: 2px solid #0095be;
        background-color: #f9f9f9;
        color: #000000;
    }
    .event-name {
        color: #f9c61e; /* Yellow color */
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
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
        max-width: 180px;  /* Increased max width for logos */
        display: block;
        margin: 0 auto 15px;  /* Added bottom margin */
        pointer-events: none;
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
        max-height: 400px;  /* Increased max height */
        overflow-y: auto;
        margin-bottom: 15px;
    }
    /* Header layout */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;  /* Added padding */
    }
    /* Banner style */
    .banner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;  /* Increased margin */
    }
    /* Language toggle button */
    .language-toggle {
        font-size: 18px;  /* Increased font size */
        padding: 10px 15px;  /* Increased padding */
        border-radius: 10px;  /* Rounded corners */
        background-color: #f9c61e;
        color: white;
        border: none;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'pin' not in st.session_state:
        st.session_state.pin = None
    if 'get_together_started' not in st.session_state:
        st.session_state.get_together_started = False
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = None
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None
    if 'selected_employee' not in st.session_state:
        st.session_state.selected_employee = None
    if 'show_options_panel' not in st.session_state:
        st.session_state.show_options_panel = False
    if 'guest_name' not in st.session_state:
        st.session_state.guest_name = None
    if 'guest_company' not in st.session_state:
        st.session_state.guest_company = ''
    if 'entered_pin' not in st.session_state:
        st.session_state.entered_pin = ''
    if 'attendance_data' not in st.session_state:
        st.session_state.attendance_data = []
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'confirmation_needed' not in st.session_state:
        st.session_state.confirmation_needed = False
    if 'admin_access_granted' not in st.session_state:
        st.session_state.admin_access_granted = False
    if 'last_interaction_time' not in st.session_state:
        st.session_state.last_interaction_time = time.time()
    if 'trigger_rerun' not in st.session_state:
        st.session_state.trigger_rerun = False
    if 'show_bottom_back_button' not in st.session_state:
        st.session_state.show_bottom_back_button = True
    if 'show_admin_settings' not in st.session_state:
        st.session_state.show_admin_settings = False
    if 'custom_event_name' not in st.session_state:
        st.session_state.custom_event_name = "GetTogether"
    if 'custom_message' not in st.session_state:
        st.session_state.custom_message = ''
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'    
    if 'employee_just_added' not in st.session_state:
        st.session_state.employee_just_added = False
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'end_thread' not in st.session_state:
        st.session_state.end_thread = None
    if 'cancel_end' not in st.session_state:
        st.session_state.cancel_end = False
    if 'datenschutz_pin' not in st.session_state:
        st.session_state.datenschutz_pin = None
    if 'datenschutz_pin_active' not in st.session_state:
        st.session_state.datenschutz_pin_active = False
    if 'last_activity_time' not in st.session_state:
        st.session_state.last_activity_time = time.time()
    if 'auto_end_hours' not in st.session_state:
        st.session_state.auto_end_hours = 5
    if 'auto_end_minutes' not in st.session_state:
        st.session_state.auto_end_minutes = 0
    if 'accounting_email' not in st.session_state:
        st.session_state.accounting_email = "accounting@example.com"
    if 'signatures' not in st.session_state:
        st.session_state.signatures = {}
    if 'require_signature' not in st.session_state:
        st.session_state.require_signature = False
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None
    if 'added_employees' not in st.session_state:
        st.session_state.added_employees = []
    if 'custom_employee_messages' not in st.session_state:
        st.session_state.custom_employee_messages = {}
    if 'show_custom_message' not in st.session_state:
        st.session_state.show_custom_message = False
initialize_session_state()

# Callback function für die Auswahl einer Firma
def select_company_callback(company):
    if company in ["Externe Partner", "External Partners"]:
        st.session_state.selected_company = "Externe Partner"  # Always use the German version for CSV lookup
    else:
        st.session_state.selected_company = company

    if company in [get_text("Gast", "Guest"), "Gast", "Guest"]:  # Check for both German and English versions
        st.session_state.page = 'guest_info'
    else:
        st.session_state.page = 'select_team'

def trigger_rerun():
    # Custom function to manually rerun the Streamlit app by toggling a state
    st.session_state.trigger_rerun = not st.session_state.trigger_rerun
# Callback function für die Auswahl eines Teams

def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
# Callback function für die Auswahl eines Mitarbeiters

def get_text(de_text, en_text):
    return de_text if st.session_state.language == 'DE' else en_text

def select_employee_callback(employee):
    st.session_state.selected_employee = employee
    
    # Create attendee data
    attendee_data = {
        'Name': employee,
        'Firma': st.session_state.selected_company,
        'Team': st.session_state.selected_team,
        'Zeit': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Event Name': st.session_state.custom_event_name,
    }

    if st.session_state.require_signature:
        attendee_data['Signature'] = st.session_state.signatures.get(employee)
        pdf_path = save_attendee_record(attendee_data)
        attendee_data['RecordPath'] = pdf_path
    
    st.session_state.attendance_data.append(attendee_data)
    
    # Automatically save the updated attendance list
    auto_save_attendance()

def save_attendee_record(attendee_data):
    if not st.session_state.require_signature:
        return  # If signatures are not required, we'll stick with the CSV format

    # Create a directory for attendee records if it doesn't exist
    os.makedirs('attendee_records', exist_ok=True)

    # Create a PDF for the attendee
    file_name = f"attendee_records/{attendee_data['Name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Add attendee information to the PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Attendee Record: {attendee_data['Name']}")
    
    c.setFont("Helvetica", 12)
    y_position = height - 80
    for key, value in attendee_data.items():
        if key != 'Signature':
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 20

    # Add the signature if available
    if 'Signature' in attendee_data and attendee_data['Signature']:
        signature_path = attendee_data['Signature']
        if os.path.exists(signature_path):
            img = ImageReader(signature_path)
            c.drawImage(img, 50, y_position - 100, width=200, height=100, preserveAspectRatio=True)
            c.drawString(50, y_position - 120, "Signature:")

    c.save()
    return file_name

def save_attendance():
    if st.session_state.attendance_data:
        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')
        st.success(f"Anwesenheitsdokument '{file_name}' erfolgreich gespeichert.")
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Anwesenheitsdokument",
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
    else:
        st.warning("Keine Anwesenheitsdaten zum Speichern vorhanden.")

def start_get_together(pin1, pin2, custom_event_name):
    if pin1 and pin2 and pin1 == pin2:
        st.session_state.pin = pin1
        st.session_state.get_together_started = True
        
        # Set custom event name only if it's not empty
        st.session_state.custom_event_name = custom_event_name if custom_event_name else ""
        
        st.success(get_text("GetTogether gestartet!", "GetTogether started!"))
        return True
    else:
        if not pin1 or not pin2:
            st.error(get_text("Bitte beide PIN-Felder ausfüllen.", "Please fill in both PIN fields."))
        elif pin1 != pin2:
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
        return False

def submit_guest():
    guest_name = st.session_state.guest_name
    guest_company = st.session_state.guest_company.strip()  # Optionales Feld
    if guest_name:
        # Anwesenheitsdaten direkt speichern mit einer eindeutigen ID
        attendance_record = {
            'ID': str(uuid.uuid4()),
            'Name': guest_name,
            'Firma': guest_company if guest_company else 'Gast',
            'Team': 'Gast',
            'Zeit': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.attendance_data.append(attendance_record)
        st.success(f"Anwesenheit von Gast '{guest_name}' erfolgreich erfasst!")
        # Zurück zur Firmenauswahl
        st.session_state.page = 'select_company'
        st.session_state.selected_company = None
        st.session_state.guest_name = None
        st.session_state.guest_company = ''
    else:
        st.error("Bitte geben Sie Ihren Namen ein.")

def go_back_to_company():
    """
    Resets session states and navigates back to the company selection screen.
    Closes both the Admin Panel and Admin Einstellungen.
    """
    st.session_state.page = 'select_company'
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.confirmation_needed = False  # Reset confirmation state
    trigger_rerun()  # Trigger rerun to refresh the UI

def show_admin_panel():
    # Ensure admin panel is visible
    if st.session_state.show_admin_panel:
        # Step 1: Display Admin PIN input if access not yet granted
        if not st.session_state.admin_access_granted:
            entered_pin = st.text_input("Admin PIN eingeben", type="password", key="entered_pin_admin")
            # Zurück button should always be visible here to go back to the main page
            if st.button("Zurück", key="admin_panel_back_pin_input"):
                go_back_to_company()
            if entered_pin and entered_pin == st.session_state.pin:
                st.session_state.admin_access_granted = True  # Grant access
                st.session_state.entered_pin_admin = None  # Clear the PIN input
                st.session_state.last_interaction_time = time.time()  # Reset the interaction timer
                st.success("Adminzugang gewährt.")
            elif entered_pin:
                st.error("Falscher Admin PIN.")
        # Step 2: Once admin access is granted, show admin options
        if st.session_state.admin_access_granted:
            st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)
            # Example: Option to end the GetTogether
            if st.session_state.get_together_started:
                if not st.session_state.confirmation_needed:
                    if st.button("GetTogether beenden"):
                        st.session_state.confirmation_needed = True
                confirm_end_get_together()  # Handle confirmation for ending the event
            # Add Zurück button here to close the admin panel after access is granted
            if st.button("Zurück", key="admin_panel_back"):
                go_back_to_company()

def go_back_to_team_from_employee():
    # Navigate back to the team selection screen
    st.session_state.page = 'select_team'
    st.session_state.selected_employee = None
    st.session_state.show_admin_panel = False  # Close admin panel if open
# Callback function zum Löschen eines Anwesenheitseintrags

def display_countdown_timer():
    if st.session_state.end_time and st.session_state.get_together_started:
        now = datetime.now(local_tz)
        time_remaining = st.session_state.end_time - now
        if time_remaining.total_seconds() > 0:
            days, remainder = divmod(time_remaining.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            countdown_text = get_text(
                f"Verbleibende Zeit: {int(days)} T, {int(hours)} Std, {int(minutes)} Min",
                f"Time remaining: {int(days)}d, {int(hours)}h, {int(minutes)}m"
            )
            
            st.markdown(
                f"""
                <div style="
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background-color: rgba(249, 198, 30, 0.1);
                    color: #888888;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    z-index: 1000;
                ">
                    {countdown_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(get_text("Das Event ist beendet!", "The event has ended!"))
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def cancel_scheduled_end():
    st.session_state.end_time = None
    st.session_state.cancel_end = True
    st.success(get_text("Geplantes Ende wurde abgebrochen.", "Scheduled end has been cancelled."))

def admin_settings():
    """
    Function to display the Admin Einstellungen with improved organization and logical grouping.
    """
    st.markdown(
        f"""
        <div style="
            color: #f9c61e;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0 30px 0;
        ">
            {get_text('Admin Einstellungen', 'Admin Settings')}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Event Settings
    st.markdown(f"<div class='sub-header'>{get_text('Event-Einstellungen:', 'Event Settings:')}</div>", unsafe_allow_html=True)
    
    # Event Name Change
    new_event_name = st.text_input(get_text("Neuer Event Name:", "New Event Name:"), value=st.session_state.custom_event_name)
    if st.button(get_text("Event Name aktualisieren", "Update Event Name")):
        st.session_state.custom_event_name = new_event_name
        st.success(get_text(f"Event Name wurde zu '{new_event_name}' geändert.", f"Event Name has been changed to '{new_event_name}'."))
        st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)

    # Custom Message Setting
    custom_message = st.text_area(
        get_text("Nachricht über der Firmenauswahl eingeben:", "Enter message to display above company selection:"),
        value=st.session_state.get('custom_message', ''),
        help=get_text("Diese Nachricht wird zentriert über der Firmenauswahl angezeigt. Lassen Sie das Feld leer, um keine Nachricht anzuzeigen.",
                      "This message will be displayed centered above the company selection. Leave empty for no message.")
    )
    if st.button(get_text("Nachricht aktualisieren", "Update Message")):
        st.session_state.custom_message = custom_message
        st.success(get_text("Benutzerdefinierte Nachricht wurde aktualisiert.", "Custom message has been updated."))

    # 2. Automatic End and Document Sending
    st.markdown(f"<div class='sub-header'>{get_text('Automatisches Ende und Dokumentenversand:', 'Automatic End and Document Sending:')}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        hours = st.number_input(
            get_text("Stunden:", "Hours:"), 
            min_value=0, value=st.session_state.auto_end_hours, step=1
        )

    with col2:
        minutes = st.selectbox(
            get_text("Minuten:", "Minutes:"),
            options=[0, 15, 30, 45],
            index=0
        )

    accounting_email = st.text_input(get_text("E-Mail-Adresse für Buchhaltung:", "Email address for accounting:"), 
                                     value=st.session_state.accounting_email)

    if st.button(get_text("Automatisches Ende aktualisieren", "Update Automatic End")):
        total_minutes = hours * 60 + minutes
        st.session_state.auto_end_hours = hours
        st.session_state.auto_end_minutes = minutes
        st.session_state.accounting_email = accounting_email
        end_time = datetime.now() + timedelta(minutes=total_minutes)
        st.session_state.end_time = end_time
        schedule_event_end(end_time)
        
        document_types = "CSV und PDF" if st.session_state.require_signature else "CSV"
        success_message = get_text(
            f"Event wird in {hours} Stunden und {minutes} Minuten automatisch beendet und {document_types}-Dokumente an {accounting_email} versendet.",
            f"Event will automatically end and send {document_types} documents to {accounting_email} in {hours} hours and {minutes} minutes."
        )
        st.success(success_message)

    # Display current end time if set
    if 'end_time' in st.session_state and st.session_state.end_time:
        st.info(get_text(f"Aktuelles geplantes Ende: {st.session_state.end_time.strftime('%d.%m.%Y %H:%M')}", 
                         f"Current scheduled end: {st.session_state.end_time.strftime('%Y-%m-%d %H:%M')}"))

    # Option to cancel scheduled end
    if 'end_time' in st.session_state and st.session_state.end_time:
        if st.button(get_text("Geplantes Ende abbrechen", "Cancel Scheduled End")):
            cancel_scheduled_end()
            st.rerun()

    # 3. Security Settings
    st.markdown(f"<div class='sub-header'>{get_text('Sicherheitseinstellungen:', 'Security Settings:')}</div>", unsafe_allow_html=True)
    
    # PIN Change
    current_pin = st.text_input(get_text("Aktuellen PIN eingeben", "Enter current PIN"), type="password", key="current_pin")
    new_pin = st.text_input(get_text("Neuen PIN eingeben", "Enter new PIN"), type="password", key="new_pin")
    confirm_new_pin = st.text_input(get_text("Neuen PIN bestätigen", "Confirm new PIN"), type="password", key="confirm_new_pin")

    if st.button(get_text("PIN ändern", "Change PIN")):
        if current_pin == st.session_state.pin:
            if new_pin == confirm_new_pin:
                st.session_state.pin = new_pin
                st.success(get_text("PIN wurde erfolgreich geändert!", "PIN has been successfully changed!"))
            else:
                st.error(get_text("Die neuen PINs stimmen nicht überein.", "The new PINs do not match."))
        else:
            st.error(get_text("Der aktuelle PIN ist falsch.", "The current PIN is incorrect."))

    # Datenschutz PIN Settings
    st.markdown(f"<div class='sub-header'>{get_text('Datenschutz PIN Einstellungen:', 'Data Protection PIN Settings:')}</div>", unsafe_allow_html=True)
    
    if st.session_state.datenschutz_pin_active:
        st.info(get_text("Datenschutz PIN ist derzeit aktiv.", "Data Protection PIN is currently active."))
        if st.button(get_text("Datenschutz PIN deaktivieren", "Disable Data Protection PIN"), key="disable_datenschutz_pin"):
            st.session_state.datenschutz_pin_active = False
            st.session_state.datenschutz_pin = None
            st.success(get_text("Datenschutz PIN wurde deaktiviert.", "Data Protection PIN has been disabled."))
            st.rerun()
    else:
        st.info(get_text("Datenschutz PIN ist derzeit nicht aktiv.", "Data Protection PIN is currently not active."))
    
    new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN setzen:", "Set new Data Protection PIN:"), type="password", key="new_datenschutz_pin")
    confirm_new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN bestätigen:", "Confirm new Data Protection PIN:"), type="password", key="confirm_new_datenschutz_pin")
    
    if st.button(get_text("Datenschutz PIN aktualisieren", "Update Data Protection PIN")):
        if new_datenschutz_pin and new_datenschutz_pin == confirm_new_datenschutz_pin:
            st.session_state.datenschutz_pin = new_datenschutz_pin
            st.session_state.datenschutz_pin_active = True
            st.success(get_text("Datenschutz PIN wurde aktualisiert und aktiviert.", "Data Protection PIN has been updated and enabled."))
            st.rerun()
        elif not new_datenschutz_pin:
            st.error(get_text("Bitte geben Sie einen gültigen PIN ein.", "Please enter a valid PIN."))
        else:
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))

    # 4. Attendance Management
    st.markdown(f"<div class='sub-header'>{get_text('Anwesenheitsverwaltung:', 'Attendance Management:')}</div>", unsafe_allow_html=True)
    st.info(get_text("Hinweis: Eine CSV-Datei wird automatisch nach jeder neuen Anmeldung gespeichert.",
                     "Note: A CSV file is automatically saved after each new attendee registration."))
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        st.dataframe(df[['Name', 'Firma', 'Team', 'Zeit']])

        # Option to delete an attendee
        st.markdown(f"<div class='sub-header'>{get_text('Teilnehmer entfernen:', 'Remove Participant:')}</div>", unsafe_allow_html=True)
        
        # Create a unique identifier for each record
        name_to_id = {f"{record['Name']} ({record['Firma']})": record.get('ID', f"{record['Name']}_{record['Firma']}") 
                      for record in st.session_state.attendance_data}
        attendee_names = list(name_to_id.keys())
        
        selected_name = st.selectbox(get_text("Wählen Sie einen Teilnehmer zum Entfernen:", "Select a participant to remove:"), 
                                     options=attendee_names)
        
        if st.button(get_text("Teilnehmer entfernen", "Remove Participant")):
            if selected_name:
                selected_id = name_to_id[selected_name]
                delete_attendance_record(selected_id)
                st.success(get_text(f"{selected_name} wurde aus der Anwesenheitsliste entfernt.",
                                    f"{selected_name} has been removed from the attendance list."))
                st.rerun()
            else:
                st.warning(get_text("Bitte wählen Sie einen Teilnehmer aus.", "Please select a participant."))

        # Option to save current attendance list
        st.markdown(f"<div class='sub-header'>{get_text('Aktuelle Anwesenheitsliste speichern:', 'Save Current Attendance List:')}</div>", unsafe_allow_html=True)
        
        custom_save_name = st.text_input(get_text("Name für die Zwischenspeicherung (optional):", "Name for intermediate save (optional):"))
        
        if st.button(get_text("Anwesenheitsliste Zwischenstand speichern", "Save Attendance List Snapshot")):
            save_current_attendance(custom_save_name)
    else:
        st.info(get_text("Noch keine Teilnehmer angemeldet.", "No participants registered yet."))

    # 5. Master Data Management
    st.markdown(f"<div class='sub-header'>{get_text('Stammdaten bearbeiten:', 'Edit Master Data:')}</div>", unsafe_allow_html=True)
    
    main_dir = os.path.dirname(os.path.abspath(__file__))
    csv_files = [f for f in os.listdir(main_dir) if f.endswith('.csv')]
    
    selected_csv = st.selectbox(
        get_text("Wählen Sie die zu bearbeitende Stammdaten-Datei:", "Choose the master data file to edit:"),
        options=csv_files,
        key="admin_selected_csv"
    )
    
    if st.button(get_text("Stammdaten bearbeiten", "Edit Master Data")):
        st.session_state.selected_file = os.path.join(main_dir, selected_csv)
        st.session_state.previous_page = 'admin_settings'  # Store the previous page
        st.session_state.page = 'update_master_data'
        st.rerun()

    # 6. Signature Requirement Setting
    st.markdown(f"<div class='sub-header'>{get_text('Unterschrift-Einstellungen:', 'Signature Settings:')}</div>", unsafe_allow_html=True)
    
    require_signature = st.checkbox(get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), 
                                    value=st.session_state.require_signature)
    
    if st.button(get_text("Unterschrift-Einstellung aktualisieren", "Update Signature Setting")):
        st.session_state.require_signature = require_signature
        st.success(get_text("Unterschrift-Einstellung wurde aktualisiert.", "Signature setting has been updated."))

    # Display current signatures if any
    if st.session_state.signatures:
        st.markdown(f"<div class='sub-header'>{get_text('Aktuelle Unterschriften:', 'Current Signatures:')}</div>", unsafe_allow_html=True)
        for employee, signature_path in st.session_state.signatures.items():
            st.write(f"{employee}:")
            if os.path.exists(signature_path):
                with open(signature_path, "rb") as f:
                    img_bytes = f.read()
                st.image(img_bytes, width=200)
            else:
                st.write(get_text("Unterschrift nicht gefunden", "Signature not found"))

    # 7. Custom Employee Messages
    st.markdown(f"<div class='sub-header'>{get_text('Benutzerdefinierte Mitarbeiternachrichten:', 'Custom Employee Messages:')}</div>", unsafe_allow_html=True)
    
    # Display current custom messages
    if st.session_state.custom_employee_messages:
        st.write(get_text("Aktuelle benutzerdefinierte Nachrichten:", "Current custom messages:"))
        for employee, message in st.session_state.custom_employee_messages.items():
            st.text(f"{employee}: {message}")
    
    # Fetch all employees from the CSV file
    all_employees = get_all_employees()
    
    # Add or edit custom message
    available_employees = [""] + [emp for emp in all_employees if emp not in st.session_state.custom_employee_messages]
    new_employee = st.selectbox(
        get_text("Mitarbeitername:", "Employee name:"),
        options=available_employees,
        key="new_employee_selectbox"
    )
    new_message = st.text_area(
        get_text("Nachricht für Mitarbeiter bei der Anmeldung:", "Message for employee upon sign-in:"),
        help=get_text("Diese Nachricht wird dem Mitarbeiter nach der Anmeldung angezeigt. Lassen Sie das Feld leer, um keine Nachricht anzuzeigen.",
                      "This message will be shown to the employee after signing in. Leave empty for no message.")
    )
    
    if st.button(get_text("Mitarbeiternachricht hinzufügen/aktualisieren", "Add/Update Employee Message")):
        if new_employee and new_message:
            st.session_state.custom_employee_messages[new_employee] = new_message
            st.success(get_text(f"Benutzerdefinierte Nachricht für {new_employee} wurde aktualisiert.", 
                                f"Custom message for {new_employee} has been updated."))
            st.rerun()
        elif new_employee:
            st.warning(get_text("Bitte geben Sie eine Nachricht ein.", "Please enter a message."))
        else:
            st.warning(get_text("Bitte wählen Sie einen Mitarbeiternamen aus.", "Please select an employee name."))
    
    # Remove custom message
    remove_employee = st.selectbox(
        get_text("Mitarbeiternachricht entfernen:", "Remove employee message:"),
        options=[""] + list(st.session_state.custom_employee_messages.keys())
    )
    if remove_employee and st.button(get_text("Nachricht entfernen", "Remove Message")):
        del st.session_state.custom_employee_messages[remove_employee]
        st.success(get_text(f"Benutzerdefinierte Nachricht für {remove_employee} wurde entfernt.",
                            f"Custom message for {remove_employee} has been removed."))
        st.rerun()

    # 8. End GetTogether Option and Accounting Email
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether beenden und Dokumente an die Buchhaltung schicken:', 'End GetTogether and Send Documents to Accounting:')}</div>", unsafe_allow_html=True)
    
    # Add option to update accounting email
    current_accounting_email = st.session_state.get('accounting_email', '')
    new_accounting_email = st.text_input(
        get_text("E-Mail-Adresse für Buchhaltung:", "Email address for accounting:"),
        value=current_accounting_email,
        key="new_accounting_email_input"  # Add this unique key
    )
    if st.button(get_text("E-Mail-Adresse aktualisieren", "Update Email Address")):
        st.session_state.accounting_email = new_accounting_email
        st.success(get_text("E-Mail-Adresse für Buchhaltung wurde aktualisiert.", "Accounting email address has been updated."))
    
    end_pin = st.text_input(get_text("PIN eingeben zum Beenden des GetTogethers:", "Enter PIN to end the GetTogether:"), type="password", key="end_gettogether_pin")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text("GetTogether beenden", "End GetTogether"), key="end_gettogether_button", use_container_width=True):
            if end_pin == st.session_state.pin:
                if end_get_together():
                    st.success(get_text("GetTogether wurde beendet. Die Anwesenheitsdokumente wurden gespeichert und an die Buchhaltung gesendet.",
                                        "GetTogether has been ended. The attendance documents have been saved and sent to accounting."))
                    time.sleep(2)
                    st.session_state.page = 'home'
                    st.rerun()
            else:
                st.error(get_text("Falscher PIN. GetTogether konnte nicht beendet werden.",
                                  "Incorrect PIN. GetTogether could not be ended."))

    # Back Button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(get_text("Zurück", "Back"), key="admin_settings_back", use_container_width=True):
        st.session_state.page = 'select_company'
        st.session_state.show_admin_panel = False
        st.session_state.admin_access_granted = False
        st.rerun()

def update_master_data():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('Stammdaten aktualisieren', 'Update Master Data')}</div>", unsafe_allow_html=True)
    
    file_path = st.session_state.selected_file
    
    if not os.path.exists(file_path):
        st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                          f"The file '{file_path}' was not found. Please check the path and filename."))
        return

    df = pd.read_csv(file_path)
    
    # Display current data
    st.dataframe(df)
    
    # Check column names
    columns = df.columns.tolist()
    st.write(get_text("Verfügbare Spalten:", "Available columns:"), columns)

    # Get existing company and team names if the columns exist
    existing_companies = sorted(df[columns[0]].unique().tolist()) if len(columns) > 0 else []
    existing_teams = sorted(df[columns[1]].unique().tolist()) if len(columns) > 1 else []

    # Add new entry
    st.markdown(f"<div class='sub-header'>{get_text('Neuen Eintrag hinzufügen:', 'Add New Entry:')}</div>", unsafe_allow_html=True)
    new_entry = {}
    for i, col in enumerate(columns):
        if i == 0:  # First column (assumed to be company)
            new_entry[col] = st.selectbox(
                get_text(f"{col} (wählen oder neu eingeben):", f"{col} (select or enter new):"),
                options=existing_companies + [''],
                index=len(existing_companies),
                key=f"new_entry_{col}"
            )
        elif i == 1:  # Second column (assumed to be team)
            new_entry[col] = st.selectbox(
                get_text(f"{col} (wählen oder neu eingeben):", f"{col} (select or enter new):"),
                options=existing_teams + [''],
                index=len(existing_teams),
                key=f"new_entry_{col}"
            )
        else:
            new_entry[col] = st.text_input(f"{col}:", key=f"new_entry_{col}")
    
    if st.button(get_text("Hinzufügen", "Add")):
        new_row = pd.DataFrame([new_entry])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success(get_text("Neuer Eintrag hinzugefügt.", "New entry added."))
        st.rerun()
    
    # Edit existing entry
    st.markdown(f"<div class='sub-header'>{get_text('Bestehenden Eintrag bearbeiten:', 'Edit Existing Entry:')}</div>", unsafe_allow_html=True)
    
    # Create a unique identifier for each row
    df['identifier'] = df.apply(lambda row: " - ".join(str(row[col]) for col in columns), axis=1)
    
    selected_entry = st.selectbox(
        get_text("Wählen Sie einen Eintrag zum Bearbeiten:", "Select an entry to edit:"),
        options=df['identifier'].tolist(),
        format_func=lambda x: x,
        key="edit_entry_select"
    )
    
    if selected_entry:
        selected_row = df[df['identifier'] == selected_entry].iloc[0]
        edit_column = st.selectbox(get_text("Zu bearbeitende Spalte:", "Column to edit:"), options=columns, key="edit_column_select")
        
        if edit_column == columns[0]:  # First column (assumed to be company)
            new_value = st.selectbox(
                get_text("Neuer Wert (wählen oder eingeben):", "New value (select or enter):"),
                options=existing_companies + [selected_row[edit_column], ''],
                index=existing_companies.index(selected_row[edit_column]) if selected_row[edit_column] in existing_companies else len(existing_companies),
                key="edit_company_value"
            )
        elif edit_column == columns[1]:  # Second column (assumed to be team)
            new_value = st.selectbox(
                get_text("Neuer Wert (wählen oder eingeben):", "New value (select or enter):"),
                options=existing_teams + [selected_row[edit_column], ''],
                index=existing_teams.index(selected_row[edit_column]) if selected_row[edit_column] in existing_teams else len(existing_teams),
                key="edit_team_value"
            )
        else:
            new_value = st.text_input(get_text("Neuer Wert:", "New value:"), value=str(selected_row[edit_column]), key="edit_other_value")
        
        if st.button(get_text("Aktualisieren", "Update")):
            df.loc[df['identifier'] == selected_entry, edit_column] = new_value
            df = df.drop('identifier', axis=1)  # Remove the temporary identifier column
            df.to_csv(file_path, index=False)
            st.success(get_text("Eintrag aktualisiert.", "Entry updated."))
            st.rerun()
    
    # Modify the 'Zurück' button behavior
    if st.button(get_text("Zurück", "Back")):
        if st.session_state.get_together_started:
            # If GetTogether is running, go back to admin settings
            st.session_state.page = 'admin_settings'
        else:
            # If GetTogether is not running, go back to home
            st.session_state.page = 'home'
        st.rerun()

def reset_to_company_selection():
    """
    Resets session states related to the admin panel and navigates back to the company selection page.
    """
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'

def reset_admin_state():
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    trigger_rerun()  # Trigger rerun to refresh the UI

def close_admin_panel():
    """
    Resets session state related to the admin panel and navigates back to the company selection.
    """
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'
    trigger_rerun()  # Trigger a rerun after closing the panel


def delete_attendance_record(identifier):
    """
    Deletes an attendance record based on the record's ID.
    """
    st.session_state.attendance_data = [
        record for record in st.session_state.attendance_data 
        if record.get('ID', f"{record['Name']}_{record['Firma']}") != identifier
    ]
    # Automatically save the updated attendance list
    auto_save_attendance()

def save_current_attendance(custom_save_name=None):
    """
    Manually saves the current attendance list to a new file.
    This function creates a new file each time it's called, with an optional custom name and timestamp.
    """
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        
        # Remove the 'ID' column
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        event_name = st.session_state.custom_event_name.replace(" ", "_")
        
        if custom_save_name:
            custom_save_name = custom_save_name.replace(" ", "_")
            file_name = f"Anwesenheit_{event_name}_{custom_save_name}_{timestamp}.csv"
        else:
            file_name = f"Anwesenheit_{event_name}_Zwischenstand_{timestamp}.csv"
        
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        
        df.to_csv(file_path, index=False, encoding='utf-8')
        st.success(get_text(f"Anwesenheitsliste '{file_name}' erfolgreich gespeichert.",
                            f"Attendance list '{file_name}' successfully saved."))
        
        # Provide download button for the saved CSV
        with open(file_path, "rb") as f:
            st.download_button(
                label=get_text("Anwesenheitsliste herunterladen", "Download Attendance List"),
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern vorhanden.",
                            "No attendance data available to save."))



def show_options_wheel():
    """
    Displays the options wheel and navigates to the Admin Panel page when clicked.
    """
    if st.session_state.get_together_started:
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("⚙️", key="settings_button"):
                st.session_state.page = 'admin_panel'  # Navigate to the admin panel page
                trigger_rerun()  # Trigger rerun to show the admin panel

def change_pin():
    st.markdown("<div class='sub-header'>PIN ändern:</div>", unsafe_allow_html=True)
    current_pin = st.text_input("Aktuellen PIN eingeben", type="password", key="current_pin")
    if current_pin == st.session_state.pin:
        new_pin1 = st.text_input("Neuen PIN eingeben", type="password", key="new_pin1")
        new_pin2 = st.text_input("Neuen PIN bestätigen", type="password", key="new_pin2")
        if new_pin1 and new_pin2:
            if new_pin1 == new_pin2:
                st.session_state.pin = new_pin1
                st.success("PIN wurde erfolgreich geändert!")
            else:
                st.error("Die neuen PINs stimmen nicht überein.")
    elif current_pin and current_pin != st.session_state.pin:
        st.error("Aktueller PIN ist falsch.")

def home():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether konfigurieren:', 'Configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    # PIN setting
    col1, col2 = st.columns(2)
    with col1:
        pin1 = st.text_input(get_text("Setze einen PIN:", "Set a PIN:"), type="password", key="pin1")
    with col2:
        pin2 = st.text_input(get_text("Bestätige den PIN:", "Confirm the PIN:"), type="password", key="pin2")
    
    # Event name
    custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
    
    # File selection (allowing selection of other CSV files in the same directory)
    st.markdown(f"<div class='sub-header'>{get_text('Stammdaten-Datei:', 'Master Data File:')}</div>", unsafe_allow_html=True)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List all CSV files in the current directory
    csv_files = [f for f in os.listdir(current_dir) if f.endswith('.csv')]
    
    if csv_files:
        selected_file = st.selectbox(
            get_text("Wählen Sie die Stammdaten-Datei:", "Select the master data file:"),
            options=csv_files,
            index=csv_files.index('Firmen_Teams_Mitarbeiter.csv') if 'Firmen_Teams_Mitarbeiter.csv' in csv_files else 0,
            key="file_selector"
        )
        st.session_state.selected_file = os.path.join(current_dir, selected_file)
    else:
        st.error(get_text("Keine CSV-Dateien im aktuellen Verzeichnis gefunden.", 
                          "No CSV files found in the current directory."))
        st.session_state.selected_file = None
    
    # Optional automatic end
    st.markdown(f"<div class='sub-header'>{get_text('Optionale Einstellungen:', 'Optional Settings:')}</div>", unsafe_allow_html=True)
    enable_auto_end = st.checkbox(get_text("Automatisches Ende aktivieren", "Enable automatic end"), value=False, key="enable_auto_end")
    
    if enable_auto_end:
        col1, col2 = st.columns(2)
        with col1:
            auto_end_hours = st.number_input(
                get_text("Stunden:", "Hours:"), 
                min_value=0, value=5, step=1, key="auto_end_hours_input"
            )
        with col2:
            auto_end_minutes = st.selectbox(
                get_text("Minuten:", "Minutes:"),
                options=[0, 15, 30, 45],
                index=0,
                key="auto_end_minutes_input"
            )
        
        now = datetime.now(local_tz)
        end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
        st.write(get_text(f"Geplantes Ende: {end_time.strftime('%d.%m.%Y %H:%M')}", 
                          f"Scheduled end: {end_time.strftime('%Y-%m-%d %H:%M')}"))
        
        accounting_email = st.text_input(
            get_text("E-Mail-Adresse für Buchhaltung:", "Email address for accounting:"), 
            value=st.session_state.accounting_email, key="accounting_email_input"
        )
    else:
        auto_end_hours = None
        auto_end_minutes = None
        accounting_email = None
    
    # Data protection PIN
    datenschutz_pin = st.text_input(
        get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), 
        type="password", key="datenschutz_pin_input"
    )
    
    # Signature requirement
    require_signature = st.checkbox(
        get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), 
        value=st.session_state.require_signature
    )
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Stammdaten aktualisieren", "Update Master Data")):
            st.session_state.page = 'update_master_data'
            st.rerun()
    
    with col2:
        if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
            if start_get_together(pin1, pin2, custom_event_name):
                st.session_state.auto_end_hours = auto_end_hours if enable_auto_end else None
                st.session_state.auto_end_minutes = auto_end_minutes if enable_auto_end else None
                st.session_state.accounting_email = accounting_email
                st.session_state.require_signature = require_signature
                if enable_auto_end and auto_end_hours is not None and auto_end_minutes is not None:
                    now = datetime.now(local_tz)
                    end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
                    schedule_event_end(end_time)
                if datenschutz_pin:
                    st.session_state.datenschutz_pin = datenschutz_pin
                    st.session_state.datenschutz_pin_active = True
                st.session_state.page = 'select_company'
                st.rerun()
initialize_session_state()

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def select_company():
    if not check_datenschutz_pin():
        return

    display_header()
    
    # Display countdown timer
    display_countdown_timer()
    
    if st.session_state.get('custom_message'):
        st.markdown(
            f"""
            <div class='custom-message'>
                {st.session_state.custom_message}
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        company_logos = {
            "4K Analytics": os.path.join(logo_dir, "4K_ANALYTICS.png"),
            "CLINIBOTS": os.path.join(logo_dir, "CLINIBOTS.png"),
            "GREENBAY research": os.path.join(logo_dir, "GREENBAY_research.png"),
            "InfAI Management": os.path.join(logo_dir, "InfAI_Management.png"),
            "iNNO3": os.path.join(logo_dir, "iNNO3.png"),
            "Lieblingsimmobilien": os.path.join(logo_dir, "Lieblingsimmobilien.png"),
            "Termingo": os.path.join(logo_dir, "TERMINGO.png"),
            "Visgato": os.path.join(logo_dir, "visgato.png"),
            "WIG2": os.path.join(logo_dir, "WIG2.png"),
        }
        st.markdown(f"<div class='important-text'>{get_text('Bitte Firma auswählen, um Anwesenheit zu bestätigen:', 'Please select a company to confirm attendance:')}</div>", unsafe_allow_html=True)
        
        num_cols = 3  # You can adjust this to 2 for a more comfortable tablet view if needed
        company_list_with_logos = list(company_logos.keys())
        companies_per_row = [company_list_with_logos[i:i + num_cols] for i in range(0, len(company_list_with_logos), num_cols)]
        
        for row in companies_per_row:
            cols = st.columns(num_cols)
            for col, company in zip(cols, row):
                with col:
                    if company in company_logos:
                        logo_path = company_logos.get(company)
                        if logo_path and os.path.exists(logo_path):
                            logo_base64 = base64.b64encode(open(logo_path, 'rb').read()).decode()
                            st.markdown(
                                f"""
                                <div class="company-container">
                                    <img class="company-logo" src="data:image/png;base64,{logo_base64}" alt="{company}" />
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                    st.button(company, key=company, on_click=select_company_callback, args=(company,), use_container_width=True)
        
        st.markdown("<hr style='border-top: 2px solid #f9c61e; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='important-text'>{get_text('Weitere Auswahl:', 'Additional options:')}</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.button("iLOC", key="iLOC", on_click=select_company_callback, args=("iLOC",), use_container_width=True)
        with cols[1]:
            external_partners = get_text("Externe Partner", "External Partners")
            st.button(external_partners, key="Externe Partner", on_click=select_company_callback, args=(external_partners,), use_container_width=True)
        with cols[2]:
            guest = get_text("Gast", "Guest")
            st.button(guest, key="Guest", on_click=select_company_callback, args=(guest,), use_container_width=True)
    st.session_state.last_activity_time = time.time()

def guest_info():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('Bitte Ihren Namen eingeben:', 'Please enter your name:')}</div>", unsafe_allow_html=True)
    st.text_input(get_text("Name:", "Name:"), key="guest_name")
    st.text_input(get_text("Firma (optional):", "Company (optional):"), key="guest_company")
    st.button(get_text("Anwesenheit erfassen", "Record attendance"), on_click=submit_guest)
    st.button(get_text("Zurück", "Back"), on_click=go_back_to_company)


def toggle_language():
    if st.session_state.language == 'DE':
        st.session_state.language = 'EN'
    else:
        st.session_state.language = 'DE'

def select_team():
    if not check_datenschutz_pin():
        return

    display_header()
    st.markdown(f"<div class='important-text'>{get_text('Firma:', 'Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        file_path = "Firmen_Teams_Mitarbeiter.csv"
        if not os.path.exists(file_path):
            st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                              f"The file '{file_path}' was not found. Please check the path and filename."))
            return
        try:
            df = pd.read_csv(file_path)
            df.columns = ['Firma', 'Team', 'Mitarbeiter']
            teams = df[df["Firma"] == st.session_state.selected_company]["Team"].unique()
        except Exception as e:
            st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                              f"Error reading the CSV file: {e}"))
            return
        if len(teams) == 0:
            st.warning(get_text("Keine Teams für die ausgewählte Firma gefunden.",
                                "No teams found for the selected company."))
            return

        st.markdown(f"<div class='sub-header'>{get_text('Team auswählen:', 'Select a team:')}</div>", unsafe_allow_html=True)
        
        # Calculate the number of columns based on the number of teams
        num_cols = min(3, len(teams))  # Maximum of 3 columns
        num_rows = ceil(len(teams) / num_cols)
        
        # Create a centered container for the buttons
        container = st.container()
        with container:
            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < len(teams):
                        with cols[col]:
                            st.button(teams[idx], key=f"team_{teams[idx]}", on_click=select_team_callback, args=(teams[idx],), use_container_width=True)
        
        # Zurück Button
        st.button(get_text("Zurück", "Back"), on_click=go_back_to_company)
    st.session_state.last_activity_time = time.time()

def select_employee():
    if not check_datenschutz_pin():
        return

    display_header()
    st.markdown(f"<div class='important-text'>{get_text('Firma:', 'Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='important-text'>{get_text('Team:', 'Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        file_path = "Firmen_Teams_Mitarbeiter.csv"
        if not os.path.exists(file_path):
            st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                              f"The file '{file_path}' was not found. Please check the path and filename."))
            return
        try:
            df = pd.read_csv(file_path)
            df.columns = ['Firma', 'Team', 'Mitarbeiter']
            employees = df[(df["Firma"] == st.session_state.selected_company) & 
                           (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
        except Exception as e:
            st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                              f"Error reading the CSV file: {e}"))
            return
        if len(employees) == 0:
            st.warning(get_text("Keine Mitarbeiter*innen für das ausgewählte Team gefunden.",
                                "No employees found for the selected team."))
            return

        st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter*innen auswählen:', 'Select employees:')}</div>", unsafe_allow_html=True)
        
        # Initialize session state variables
        if 'added_employees' not in st.session_state:
            st.session_state.added_employees = []
        if 'timer_active' not in st.session_state:
            st.session_state.timer_active = False
        if 'countdown_start_time' not in st.session_state:
            st.session_state.countdown_start_time = None
        if 'current_company_team' not in st.session_state:
            st.session_state.current_company_team = None
        if 'success_messages' not in st.session_state:
            st.session_state.success_messages = []
        if 'last_message_time' not in st.session_state:
            st.session_state.last_message_time = None
        if 'all_employees_added_time' not in st.session_state:
            st.session_state.all_employees_added_time = None

        # Check if company or team has changed
        current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
        if st.session_state.current_company_team != current_company_team:
            st.session_state.added_employees = []
            st.session_state.current_company_team = current_company_team
            st.session_state.timer_active = False
            st.session_state.countdown_start_time = None
            st.session_state.success_messages = []
            st.session_state.last_message_time = None
            st.session_state.all_employees_added_time = None

        # Calculate the number of columns based on the number of employees
        num_cols = min(3, len(employees))  # Maximum of 3 columns
        num_rows = ceil(len(employees) / num_cols)
        
        # Create a centered container for the buttons
        container = st.container()
        with container:
            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < len(employees):
                        with cols[col]:
                            employee = employees[idx]
                            is_added = employee in st.session_state.added_employees
                            button_key = f"employee_{employee}_{idx}"  # Add idx to make the key unique
                            
                            if st.button(employee, key=button_key, use_container_width=True, 
                                         disabled=is_added):
                                if st.session_state.require_signature:
                                    st.session_state.current_employee = employee
                                    st.session_state.show_signature_modal = True
                                else:
                                    select_employee_callback(employee)
                                    if employee not in st.session_state.added_employees:
                                        st.session_state.added_employees.append(employee)
                                    st.session_state.timer_active = True
                                    st.session_state.countdown_start_time = time.time()
                                    
                                    # Add success message
                                    new_message = get_text(
                                        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
                                        f'Employee "{employee}" has been added to the attendance list.'
                                    )
                                    st.session_state.success_messages.append(new_message)
                                    st.session_state.last_message_time = time.time()
                                    
                                    # Check if all employees have been added
                                    if set(st.session_state.added_employees) == set(employees):
                                        st.session_state.all_employees_added_time = time.time()
                                    
                                    # Show custom message if set for this employee
                                    if employee in st.session_state.custom_employee_messages:
                                        st.session_state.show_custom_message = True
                                        st.session_state.current_employee = employee
                                    
                                    st.rerun()  # Refresh the app
                            
                            # Apply custom style to button if already selected
                            if is_added:
                                st.markdown(f"""
                                    <style>
                                    div.stButton > button#{button_key} {{
                                        background-color: #ffcccb !important;
                                        color: #000000 !important;
                                        cursor: not-allowed !important;
                                    }}
                                    </style>
                                """, unsafe_allow_html=True)
        
        # Signature modal
        if st.session_state.get('show_signature_modal', False):
            signature_modal()

        # Display success messages
        with st.container():
            for message in st.session_state.success_messages:
                st.success(message)
        
        # Remove old messages after 5 seconds
        current_time = time.time()
        if st.session_state.last_message_time and current_time - st.session_state.last_message_time > 5:
            st.session_state.success_messages = []
            st.session_state.last_message_time = None
        
        # Add button to revert last selection
        if st.session_state.added_employees:
            if st.button(get_text("Letzte Auswahl rückgängig machen", "Undo last selection"), 
                         key="undo_last_selection",
                         use_container_width=True):
                last_employee = st.session_state.added_employees.pop()
                
                # Remove the last added employee from the attendance data
                st.session_state.attendance_data = [
                    record for record in st.session_state.attendance_data 
                    if record['Name'] != last_employee
                ]
                
                # Remove the signature if it exists
                if last_employee in st.session_state.signatures:
                    del st.session_state.signatures[last_employee]
                
                undo_message = get_text(
                    f'Mitarbeiter "{last_employee}" wurde von der Anwesenheitsliste entfernt.',
                    f'Employee "{last_employee}" has been removed from the attendance list.'
                )
                st.session_state.success_messages.append(undo_message)
                st.session_state.last_message_time = time.time()
                
                # Update the auto-saved attendance list
                auto_save_attendance()
                
                st.rerun()
        
        # Check if all employees have been added and return after 5 seconds
        if st.session_state.all_employees_added_time:
            time_since_all_added = current_time - st.session_state.all_employees_added_time
            if time_since_all_added <= 5:
                st.info(get_text(f"Alle Teammitglieder wurden hinzugefügt. Kehre in {5 - int(time_since_all_added)} Sekunden zur Firmenauswahl zurück...",
                                 f"All team members have been added. Returning to company selection in {5 - int(time_since_all_added)} seconds..."))
            else:
                return_to_company_selection()
        
        # Check if timer is active (only if not all employees have been added)
        if st.session_state.timer_active and st.session_state.countdown_start_time and not st.session_state.all_employees_added_time:
            # Calculate remaining time
            elapsed_time = time.time() - st.session_state.countdown_start_time
            remaining_time = max(0, 30 - int(elapsed_time))  # 30 seconds timer
            
            # Display countdown
            st.info(f"{get_text('Zurück zur Firmenauswahl in', 'Back to company selection in')} {remaining_time} {get_text('Sekunden...', 'seconds...')}")
            
            # If the countdown is finished, reset and go back to company selection
            if remaining_time == 0:
                return_to_company_selection()
        
        # Automatically refresh the app every second to update the countdown and messages
        st_autorefresh(interval=1000, key="autorefresh")
        
        # Zurück Button
        if st.button(get_text("Zurück zur Firmenauswahl", "Back to company selection"), key="back_button"):
            return_to_company_selection()

        # Show custom message if set
        if st.session_state.get('show_custom_message', False):
            show_custom_employee_message(st.session_state.current_employee)

    st.session_state.last_activity_time = time.time()

def return_to_company_selection():
    st.session_state.page = 'select_company'
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None
    st.rerun()

def reset_timer_state():
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.current_company_team = None           


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
                import base64
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
            
            language_toggle = "EN" if st.session_state.language == 'DE' else "DE"
            st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    st.markdown(f"<div class='version-number'>v{VERSION}</div>", unsafe_allow_html=True)

    return header_container

# Add this CSS to your existing styles
st.markdown("""
<style>
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
/* Style for both buttons to ensure they are the same size */
.stButton > button {
    width: 100% !important;
    height: 38px !important;
    padding: 0px 10px !important;
    margin-bottom: 10px !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}

</style>
""", unsafe_allow_html=True)

def navigate():
    if 'trigger_rerun' in st.session_state:
        pass  # This forces Streamlit to refresh upon state changes

    # Handle different pages
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company':
        select_company()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()
    elif st.session_state.page == 'admin_settings':
        admin_settings()
    elif st.session_state.page == 'update_master_data':
        update_master_data()
    else:
        st.error(get_text(f"Unbekannte Seite: {st.session_state.page}", f"Unknown page: {st.session_state.page}"))
        st.session_state.page = 'home'
        st.rerun()

def admin_panel_timeout():
    if st.session_state.admin_access_granted:
        # Close admin panel if no interaction happens within 300 seconds (5 minutes)
        if time.time() - st.session_state.last_interaction_time > 300:
            st.warning("Admin-Panel wegen Inaktivität geschlossen.")
            st.session_state.admin_access_granted = False
            st.session_state.show_admin_panel = False
            st.session_state.page = 'select_company'

def admin_panel():
    st.markdown(f"<div class='sub-header' style='color: #f9c61e;'>{get_text('Admin Panel', 'Admin Panel')}</div>", unsafe_allow_html=True)

    # Create columns for PIN input and Enter button
    col1, col2 = st.columns([3, 1])

    with col1:
        entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")

    with col2:
        enter_button = st.button("Enter", key="admin_pin_enter")

    # Check entered PIN against the stored PIN when Enter button is clicked
    if enter_button:
        if entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True
            st.session_state.page = 'admin_settings'
            st.success(get_text("Admin-Zugang gewährt. Sie werden zu den Einstellungen weitergeleitet.", 
                                "Admin access granted. You will be redirected to the settings."))
            st.rerun()
        else:
            st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))

    # Display detailed end time information if admin access is granted
    if st.session_state.admin_access_granted:
        st.markdown("---")
        st.markdown(f"<div class='sub-header'>{get_text('Event-Informationen', 'Event Information')}</div>", unsafe_allow_html=True)
        
        if st.session_state.end_time:
            time_remaining = st.session_state.end_time - datetime.now()
            if time_remaining.total_seconds() > 0:
                days, remainder = divmod(time_remaining.total_seconds(), 86400)
                hours, remainder = divmod(remainder, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                st.markdown(f"**{get_text('Geplantes Ende:', 'Scheduled End:')}** {st.session_state.end_time.strftime('%d.%m.%Y %H:%M')}")
                st.markdown(f"**{get_text('Verbleibende Zeit:', 'Time Remaining:')}** {int(days)} {get_text('Tage', 'days')}, {int(hours)} {get_text('Stunden', 'hours')}, {int(minutes)} {get_text('Minuten', 'minutes')}")
            else:
                st.warning(get_text("Das Event ist beendet!", "The event has ended!"))
        else:
            st.info(get_text("Kein automatisches Ende festgelegt.", "No automatic end time set."))

    # Show Abbrechen button
    if st.button(get_text("Abbrechen", "Cancel"), key="cancel_admin_panel"):
        st.session_state.page = 'select_company'
        st.session_state.show_admin_panel = False
        st.session_state.admin_access_granted = False
        st.rerun()

def confirm_end_get_together():
    if st.session_state.confirmation_needed:
        confirmation_pin = st.text_input("Bestätigen Sie den PIN zum Beenden", type="password")
        if confirmation_pin and confirmation_pin == st.session_state.pin:
            end_get_together()  # Call function to end the event
            reset_session_state()  # Reset everything after the event ends
            st.session_state.confirmation_needed = False
        elif confirmation_pin:
            st.error("Falscher PIN. Bitte erneut eingeben.")

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def display_countdown_timer():
    if st.session_state.end_time and st.session_state.get_together_started:
        now = datetime.now(local_tz)
        time_remaining = st.session_state.end_time - now
        if time_remaining.total_seconds() > 0:
            days, remainder = divmod(time_remaining.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            countdown_text = get_text(
                f"Verbleibende Zeit: {int(days)} T, {int(hours)} Std, {int(minutes)} Min",
                f"Time remaining: {int(days)}d, {int(hours)}h, {int(minutes)}m"
            )
            
            st.markdown(
                f"""
                <div style="
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background-color: rgba(249, 198, 30, 0.1);
                    color: #888888;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    z-index: 1000;
                ">
                    {countdown_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(get_text("Das Event ist beendet!", "The event has ended!"))
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def send_documents_to_accounting(file_path, file_type):
    # Email configuration
    sender_email = "your_email@example.com"  # Replace with your email
    receiver_email = st.session_state.accounting_email
    password = "your_email_password"  # Replace with your email password

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"GetTogether Attendance Documents - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    body = f"Please find attached the attendance {file_type} for the GetTogether event."
    message.attach(MIMEText(body, "plain"))

    # Attach the file
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(file_path)}",
    )
    message.attach(part)

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        st.success(f"{file_type} sent to accounting successfully.")
    except Exception as e:
        st.error(f"Failed to send {file_type} to accounting: {str(e)}")

def end_get_together():
    if st.session_state.attendance_data:
        # Generate timestamp and set up directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)

        # Always create CSV
        csv_file_name = f"Anwesenheit_{timestamp}.csv"
        csv_file_path = os.path.join(local_data_dir, csv_file_name)
        
        df = pd.DataFrame(st.session_state.attendance_data)
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        df['Event Name'] = st.session_state.custom_event_name
        df['Event End Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['Total Attendees'] = len(df)
        
        df.to_csv(csv_file_path, index=False, encoding='utf-8')

        if st.session_state.require_signature:
            # Create a ZIP file containing CSV and all PDFs
            zip_file_name = f"Anwesenheit_mit_Unterschriften_{timestamp}.zip"
            zip_file_path = os.path.join(local_data_dir, zip_file_name)
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(csv_file_path, os.path.basename(csv_file_path))
                for attendee in st.session_state.attendance_data:
                    if 'RecordPath' in attendee and os.path.exists(attendee['RecordPath']):
                        zipf.write(attendee['RecordPath'], os.path.basename(attendee['RecordPath']))
            
            # Send ZIP file to accounting
            send_documents_to_accounting(zip_file_path, "ZIP")
            
            # Provide download button for the ZIP file
            with open(zip_file_path, "rb") as f:
                st.download_button(
                    label=get_text("Anwesenheitsdokumente herunterladen", "Download Attendance Documents"),
                    data=f,
                    file_name=zip_file_name,
                    mime="application/zip"
                )
        else:
            # Send CSV to accounting
            send_documents_to_accounting(csv_file_path, "CSV")
            
            # Provide download button for the CSV
            with open(csv_file_path, "rb") as f:
                st.download_button(
                    label=get_text("Anwesenheitsliste herunterladen", "Download Attendance List"),
                    data=f,
                    file_name=csv_file_name,
                    mime="text/csv"
                )

        # Reset session state
        st.session_state.attendance_data = []
        st.session_state.added_employees = []
        st.session_state.signatures = {}
        st.session_state.get_together_started = False
        st.session_state.custom_event_name = ""

        st.success(get_text("GetTogether wurde beendet und die Anwesenheitsdokumente wurden gespeichert und versendet.",
                            "GetTogether has ended and the attendance documents have been saved and sent."))
        
        # Set a flag to indicate that we need to rerun
        st.session_state.trigger_rerun = True
        
        # Set the page to 'home'
        st.session_state.page = 'home'

        return True
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern vorhanden.",
                            "No attendance data available to save."))
        return False

def auto_save_attendance():
    """
    Automatically saves the current attendance list to a file.
    This file is overwritten each time a new attendee is added.
    The filename includes the custom event name if it was set.
    """
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        
        # Remove the 'ID' column for the CSV
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        
        # Create a filename with the event name
        event_name = st.session_state.custom_event_name.replace(" ", "_")
        file_name = f"current_attendance_{event_name}.csv"
        
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        
        # Save the DataFrame to CSV, overwriting the existing file
        df.to_csv(file_path, index=False, encoding='utf-8')

def reset_session_state():
    """
    Resets all session states related to the GetTogether event and returns to the home page.
    """
    st.session_state.page = 'home'
    st.session_state.get_together_started = False
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.attendance_data = []
    st.session_state.pin = None
    st.session_state.admin_access_granted = False
    st.session_state.show_admin_panel = False
    st.session_state.custom_event_name = "GetTogether"
    st.session_state.end_time = None
    st.session_state.custom_message = ''
    st.session_state.confirmation_needed = False

def check_datenschutz_pin():
    if st.session_state.datenschutz_pin_active:
        current_time = time.time()
        if current_time - st.session_state.last_activity_time > 300:  # 5 minutes of inactivity
            st.session_state.datenschutz_pin_active = False
        
        if not st.session_state.datenschutz_pin_active:
            display_header()  # Display the header with banner
            st.markdown(f"<div class='sub-header'>{get_text('Datenschutz-Sperre', 'Data Protection Lock')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='important-text'>{get_text('Bitte geben Sie den Datenschutz-PIN ein, um fortzufahren.', 'Please enter the Data Protection PIN to continue.')}</div>", unsafe_allow_html=True)
            
            entered_pin = st.text_input(get_text("Datenschutz PIN:", "Data Protection PIN:"), type="password", key="datenschutz_pin_check")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(get_text("Zugriff anfordern", "Request Access"), use_container_width=True):
                    if entered_pin == st.session_state.datenschutz_pin:
                        st.session_state.datenschutz_pin_active = True
                        st.session_state.last_activity_time = current_time
                        st.success(get_text("PIN korrekt. Zugriff gewährt.", "PIN correct. Access granted."))
                        time.sleep(1)  # Give user time to see the success message
                        st.rerun()
                    else:
                        st.error(get_text("Falscher PIN. Zugriff verweigert.", "Incorrect PIN. Access denied."))
            return False
    return True

def signature_modal():
    st.markdown("### " + get_text("Unterschrift erforderlich", "Signature Required"))
    st.write(get_text(f"Bitte unterschreiben Sie für {st.session_state.current_employee}",
                      f"Please sign for {st.session_state.current_employee}"))

    # Create a canvas for drawing the signature
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Color of the drawing
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        height=150,
        drawing_mode="freedraw",
        key="signature_canvas",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Bestätigen", "Confirm")):
            if canvas_result.image_data is not None:
                # Convert the image data to a PNG and save it
                img_array = np.array(canvas_result.image_data)
                img = Image.fromarray(img_array.astype('uint8'), 'RGBA')
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                # Create a signatures directory if it doesn't exist
                os.makedirs('signatures', exist_ok=True)
                
                # Save the signature as a PNG file
                file_name = f"signatures/{st.session_state.current_employee.replace(' ', '_')}.png"
                with open(file_name, "wb") as f:
                    f.write(img_byte_arr)
                
                # Store the file path in session state
                st.session_state.signatures[st.session_state.current_employee] = file_name
                
                select_employee_callback(st.session_state.current_employee)
                if st.session_state.current_employee not in st.session_state.added_employees:
                    st.session_state.added_employees.append(st.session_state.current_employee)
                
                # Add success message
                new_message = get_text(
                    f'Mitarbeiter "{st.session_state.current_employee}" wurde zur Anwesenheitsliste hinzugefügt.',
                    f'Employee "{st.session_state.current_employee}" has been added to the attendance list.'
                )
                st.session_state.success_messages.append(new_message)
                st.session_state.last_message_time = time.time()
                
                # Start or reset the timer
                st.session_state.timer_active = True
                st.session_state.countdown_start_time = time.time()
                
                # Check if all employees have been added
                employees = get_employees_for_current_team()
                if set(st.session_state.added_employees) == set(employees):
                    st.session_state.all_employees_added_time = time.time()
                
                # Show custom message if set for this employee
                if st.session_state.current_employee in st.session_state.custom_employee_messages:
                    st.session_state.show_custom_message = True
                
                st.session_state.show_signature_modal = False
                st.rerun()
            else:
                st.warning(get_text("Bitte unterschreiben Sie bevor Sie bestätigen.", 
                                    "Please sign before confirming."))

    with col2:
        if st.button(get_text("Abbrechen", "Cancel")):
            st.session_state.show_signature_modal = False
            st.rerun()

def get_employees_for_current_team():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    df = pd.read_csv(file_path)
    df.columns = ['Firma', 'Team', 'Mitarbeiter']
    employees = df[(df["Firma"] == st.session_state.selected_company) & 
                   (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
    return employees

def select_employee():
    if not check_datenschutz_pin():
        return

    display_header()
    st.markdown(f"<div class='important-text'>{get_text('Firma:', 'Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='important-text'>{get_text('Team:', 'Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        file_path = "Firmen_Teams_Mitarbeiter.csv"
        if not os.path.exists(file_path):
            st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                               f"The file '{file_path}' was not found. Please check the path and filename."))
            return
        try:
            df = pd.read_csv(file_path)
            df.columns = ['Firma', 'Team', 'Mitarbeiter']
            employees = df[(df["Firma"] == st.session_state.selected_company) & 
                           (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
        except Exception as e:
            st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                              f"Error reading the CSV file: {e}"))
            return
        if len(employees) == 0:
            st.warning(get_text("Keine Mitarbeiter*innen für das ausgewählte Team gefunden.",
                                "No employees found for the selected team."))
            return

        st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter*innen auswählen:', 'Select employees:')}</div>", unsafe_allow_html=True)
        
        # Initialize session state variables
        if 'added_employees' not in st.session_state:
            st.session_state.added_employees = []
        if 'timer_active' not in st.session_state:
            st.session_state.timer_active = False
        if 'countdown_start_time' not in st.session_state:
            st.session_state.countdown_start_time = None
        if 'current_company_team' not in st.session_state:
            st.session_state.current_company_team = None
        if 'success_messages' not in st.session_state:
            st.session_state.success_messages = []
        if 'last_message_time' not in st.session_state:
            st.session_state.last_message_time = None
        if 'all_employees_added_time' not in st.session_state:
            st.session_state.all_employees_added_time = None

        # Check if company or team has changed
        current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
        if st.session_state.current_company_team != current_company_team:
            st.session_state.added_employees = []
            st.session_state.current_company_team = current_company_team
            st.session_state.timer_active = False
            st.session_state.countdown_start_time = None
            st.session_state.success_messages = []
            st.session_state.last_message_time = None
            st.session_state.all_employees_added_time = None

        # Calculate the number of columns based on the number of employees
        num_cols = min(3, len(employees))  # Maximum of 3 columns
        num_rows = ceil(len(employees) / num_cols)
        
        # Create a centered container for the buttons
        container = st.container()
        with container:
            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < len(employees):
                        with cols[col]:
                            employee = employees[idx]
                            is_added = employee in st.session_state.added_employees
                            button_key = f"employee_{employee}_{idx}"  # Add idx to make the key unique
                            
                            if st.button(employee, key=button_key, use_container_width=True, 
                                         disabled=is_added):
                                if st.session_state.require_signature:
                                    st.session_state.current_employee = employee
                                    st.session_state.show_signature_modal = True
                                else:
                                    select_employee_callback(employee)
                                    if employee not in st.session_state.added_employees:
                                        st.session_state.added_employees.append(employee)
                                    st.session_state.timer_active = True
                                    st.session_state.countdown_start_time = time.time()
                                    
                                    # Add success message
                                    new_message = get_text(
                                        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
                                        f'Employee "{employee}" has been added to the attendance list.'
                                    )
                                    st.session_state.success_messages.append(new_message)
                                    st.session_state.last_message_time = time.time()
                                    
                                    # Check if all employees have been added
                                    if set(st.session_state.added_employees) == set(employees):
                                        st.session_state.all_employees_added_time = time.time()
                                    
                                    # Show custom message if set for this employee
                                    if employee in st.session_state.custom_employee_messages:
                                        st.session_state.show_custom_message = True
                                        st.session_state.current_employee = employee
                                    
                                    st.rerun()  # Refresh the app
                            
                            # Apply custom style to button if already selected
                            if is_added:
                                st.markdown(f"""
                                    <style>
                                    div.stButton > button#{button_key} {{
                                        background-color: #ffcccb !important;
                                        color: #000000 !important;
                                        cursor: not-allowed !important;
                                    }}
                                    </style>
                                """, unsafe_allow_html=True)
        
        # Signature modal
        if st.session_state.get('show_signature_modal', False):
            signature_modal()

        # Display success messages
        with st.container():
            for message in st.session_state.success_messages:
                st.success(message)
        
        # Remove old messages after 5 seconds
        current_time = time.time()
        if st.session_state.last_message_time and current_time - st.session_state.last_message_time > 5:
            st.session_state.success_messages = []
            st.session_state.last_message_time = None
        
        # Add button to revert last selection
        if st.session_state.added_employees:
            if st.button(get_text("Letzte Auswahl rückgängig machen", "Undo last selection"), 
                         key="undo_last_selection",
                         use_container_width=True):
                last_employee = st.session_state.added_employees.pop()
                
                # Remove the last added employee from the attendance data
                st.session_state.attendance_data = [
                    record for record in st.session_state.attendance_data 
                    if record['Name'] != last_employee
                ]
                
                # Remove the signature if it exists
                if last_employee in st.session_state.signatures:
                    del st.session_state.signatures[last_employee]
                
                undo_message = get_text(
                    f'Mitarbeiter "{last_employee}" wurde von der Anwesenheitsliste entfernt.',
                    f'Employee "{last_employee}" has been removed from the attendance list.'
                )
                st.session_state.success_messages.append(undo_message)
                st.session_state.last_message_time = time.time()
                
                # Update the auto-saved attendance list
                auto_save_attendance()
                
                st.rerun()
        
        # Check if all employees have been added and return after 5 seconds
        if st.session_state.all_employees_added_time:
            time_since_all_added = current_time - st.session_state.all_employees_added_time
            if time_since_all_added <= 5:
                st.info(get_text(f"Alle Teammitglieder wurden hinzugefügt. Kehre in {5 - int(time_since_all_added)} Sekunden zur Firmenauswahl zurück...",
                                 f"All team members have been added. Returning to company selection in {5 - int(time_since_all_added)} seconds..."))
            else:
                return_to_company_selection()
        
        # Check if timer is active (only if not all employees have been added)
        if st.session_state.timer_active and st.session_state.countdown_start_time and not st.session_state.all_employees_added_time:
            # Calculate remaining time
            elapsed_time = time.time() - st.session_state.countdown_start_time
            remaining_time = max(0, 30 - int(elapsed_time))  # 30 seconds timer
            
            # Display countdown
            st.info(f"{get_text('Zurück zur Firmenauswahl in', 'Back to company selection in')} {remaining_time} {get_text('Sekunden...', 'seconds...')}")
            
            # If the countdown is finished, reset and go back to company selection
            if remaining_time == 0:
                return_to_company_selection()
        
        # Automatically refresh the app every second to update the countdown and messages
        st_autorefresh(interval=1000, key="autorefresh")
        
        # Zurück Button
        if st.button(get_text("Zurück zur Firmenauswahl", "Back to company selection"), key="back_button"):
            return_to_company_selection()

        # Show custom message if set
        if st.session_state.get('show_custom_message', False):
            show_custom_employee_message(st.session_state.current_employee)

    st.session_state.last_activity_time = time.time()

def show_custom_employee_message(employee):
    if employee in st.session_state.custom_employee_messages:
        st.markdown("### " + get_text("Wichtige Mitteilung", "Important Notice"))
        st.write(st.session_state.custom_employee_messages[employee])
        if st.button(get_text("Schließen", "Close"), key="close_custom_message"):
            st.session_state.show_custom_message = False
            st.rerun()

def get_all_employees():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        all_employees = df['Mitarbeiter'].unique().tolist()
        return sorted(all_employees)
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return []

# Call to start the navigation
initialize_session_state()
navigate()