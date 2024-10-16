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

VERSION = "1.0.0"


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
    # Anwesenheitsdaten direkt speichern mit einer eindeutigen ID
    attendance_record = {
        'ID': str(uuid.uuid4()),
        'Name': employee,
        'Firma': st.session_state.selected_company,
        'Team': st.session_state.selected_team,
        'Zeit': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.attendance_data.append(attendance_record)
    
    # Automatically save the updated attendance list
    auto_save_attendance()

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
        time_remaining = st.session_state.end_time - datetime.now()
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
            st.experimental_rerun()

def admin_settings():
    """
    Function to display the Admin Einstellungen with improved organization, automatic CSV sending feature,
    and Stammdaten editing option.
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

    # 1. Stammdaten Editing
    st.markdown(f"<div class='sub-header'>{get_text('Stammdaten bearbeiten:', 'Edit Master Data:')}</div>", unsafe_allow_html=True)
    
    main_dir = r"C:\Users\Konrad.Reyhe\Projektarbeit"
    csv_files = [f for f in os.listdir(main_dir) if f.endswith('.csv')]
    
    selected_csv = st.selectbox(
        get_text("Wählen Sie die zu bearbeitende Stammdaten-Datei:", "Choose the master data file to edit:"),
        options=csv_files,
        key="admin_selected_csv"
    )
    
    if st.button(get_text("Stammdaten bearbeiten", "Edit Master Data")):
        st.session_state.selected_file = os.path.join(main_dir, selected_csv)
        st.session_state.page = 'update_master_data'
        st.rerun()

    # 2. Event Name Change
    st.markdown(f"<div class='sub-header'>{get_text('Event Name ändern:', 'Change Event Name:')}</div>", unsafe_allow_html=True)
    new_event_name = st.text_input(get_text("Neuer Event Name:", "New Event Name:"), value=st.session_state.custom_event_name)
    if st.button(get_text("Event Name aktualisieren", "Update Event Name")):
        st.session_state.custom_event_name = new_event_name
        st.success(get_text(f"Event Name wurde zu '{new_event_name}' geändert.", f"Event Name has been changed to '{new_event_name}'."))
        st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)

    # 3. Custom Message Setting
    st.markdown(f"<div class='sub-header'>{get_text('Benutzerdefinierte Nachricht:', 'Custom Message:')}</div>", unsafe_allow_html=True)
    custom_message = st.text_area(
        get_text("Nachricht über der Firmenauswahl eingeben:", "Enter message to display above company selection:"),
        value=st.session_state.get('custom_message', ''),
        help=get_text("Diese Nachricht wird zentriert über der Firmenauswahl angezeigt. Lassen Sie das Feld leer, um keine Nachricht anzuzeigen.",
                      "This message will be displayed centered above the company selection. Leave empty for no message.")
    )
    if st.button(get_text("Nachricht aktualisieren", "Update Message")):
        st.session_state.custom_message = custom_message
        st.success(get_text("Benutzerdefinierte Nachricht wurde aktualisiert.", "Custom message has been updated."))

    # 4. Automatic CSV Sending Feature
    st.markdown(f"<div class='sub-header'>{get_text('Automatisches Ende und CSV-Versand:', 'Automatic End and CSV Sending:')}</div>", unsafe_allow_html=True)
    
    hours = st.number_input(get_text("In wie vielen Stunden soll das Event enden und die CSV versendet werden?", 
                                     "In how many hours should the event end and send the CSV?"), 
                            min_value=1, value=5, step=1)
    
    if st.button(get_text("Automatisches Ende setzen", "Set Automatic End")):
        end_time = datetime.now() + timedelta(hours=hours)
        st.session_state.end_time = end_time
        schedule_event_end(end_time)
        st.success(get_text(f"Event wird in {hours} Stunden automatisch beendet und CSV versendet.", 
                            f"Event will automatically end and send CSV in {hours} hours."))

    # Display current end time if set
    if 'end_time' in st.session_state and st.session_state.end_time:
        st.info(get_text(f"Aktuelles geplantes Ende: {st.session_state.end_time.strftime('%d.%m.%Y %H:%M')}", 
                         f"Current scheduled end: {st.session_state.end_time.strftime('%Y-%m-%d %H:%M')}"))

    # Option to cancel scheduled end
    if 'end_time' in st.session_state and st.session_state.end_time:
        if st.button(get_text("Geplantes Ende abbrechen", "Cancel Scheduled End")):
            st.session_state.end_time = None
            cancel_scheduled_end()
            st.success(get_text("Geplantes Ende wurde abgebrochen.", "Scheduled end has been cancelled."))

    # 5. PIN Change
    st.markdown(f"<div class='sub-header'>{get_text('PIN ändern:', 'Change PIN:')}</div>", unsafe_allow_html=True)
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

    # 6. Attendance Management
    st.markdown(f"<div class='sub-header'>{get_text('Anwesenheitsverwaltung:', 'Attendance Management:')}</div>", unsafe_allow_html=True)
    st.info(get_text("Hinweis: Eine CSV-Datei wird automatisch nach jeder neuen Anmeldung gespeichert.",
                     "Note: A CSV file is automatically saved after each new attendee registration."))
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        st.dataframe(df[['Name', 'Firma', 'Team', 'Zeit']])

        # Option to delete an attendee
        st.markdown(f"<div class='sub-header'>{get_text('Teilnehmer entfernen:', 'Remove Participant:')}</div>", unsafe_allow_html=True)
        
        name_to_id = {f"{record['Name']} ({record['Firma']})": record['ID'] for record in st.session_state.attendance_data}
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

    # 7. End GetTogether Option
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether beenden und CSV an die Buchhaltung schicken:', 'End GetTogether and Send CSV to Accounting:')}</div>", unsafe_allow_html=True)
    
    end_pin = st.text_input(get_text("PIN eingeben zum Beenden des GetTogethers:", "Enter PIN to end the GetTogether:"), type="password", key="end_pin")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text("GetTogether beenden", "End GetTogether"), key="end_gettogether_button", use_container_width=True):
            if end_pin == st.session_state.pin:
                if end_get_together():
                    st.success(get_text("GetTogether wurde beendet. Die Anwesenheitsliste wurde gespeichert und an die Buchhaltung gesendet.",
                                        "GetTogether has been ended. The attendance list has been saved and sent to accounting."))
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
    
    if st.button(get_text("Zurück", "Back")):
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


def delete_attendance_record(record_id):
    """
    Deletes an attendance record based on the record's ID.
    """
    st.session_state.attendance_data = [record for record in st.session_state.attendance_data if record['ID'] != record_id]
    # Note: Success message is now in the admin_settings function for immediate feedback

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
# Funktionen für die verschiedenen Seiten

def home():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('Bitte PIN setzen und GetTogether konfigurieren:', 'Please set PIN and configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pin1 = st.text_input(get_text("Setze einen PIN für das GetTogether:", "Set a PIN for the GetTogether:"), type="password", key="pin1")
    with col2:
        pin2 = st.text_input(get_text("Bestätige den PIN:", "Confirm the PIN:"), type="password", key="pin2")
    
    custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
    
    # File selection
    default_file = r"C:\Users\Konrad.Reyhe\Projektarbeit\Firmen_Teams_Mitarbeiter.csv"

    # Custom file uploader with localized text
    st.markdown(
        f"""
        <style>
        .custom-file-upload {{
            border: 1px solid #ccc;
            display: inline-block;
            padding: 6px 12px;
            cursor: pointer;
            background-color: #f0f0f0;
        }}
        </style>
        <input type="file" id="fileUpload" style="display:none" accept=".csv" />
        <label for="fileUpload" class="custom-file-upload">
            {get_text("Datei auswählen oder hierher ziehen", "Choose a file or drag it here")}
        </label>
        <p id="fileName">{get_text("Keine Datei ausgewählt", "No file chosen")}</p>
        <script>
            const fileUpload = document.getElementById('fileUpload');
            const fileName = document.getElementById('fileName');
            fileUpload.addEventListener('change', function(e) {{
                if (e.target.files.length > 0) {{
                    fileName.textContent = e.target.files[0].name;
                }} else {{
                    fileName.textContent = '{get_text("Keine Datei ausgewählt", "No file chosen")}';
                }}
            }});
        </script>
        """,
        unsafe_allow_html=True
    )

    # Use the default file if no file is uploaded
    if 'selected_file' not in st.session_state or st.session_state.selected_file is None:
        st.session_state.selected_file = default_file

    st.write(get_text(f"Ausgewählte Datei: {st.session_state.selected_file}", 
                      f"Selected file: {st.session_state.selected_file}"))
    
    if st.button(get_text("Stammdaten aktualisieren", "Update Master Data")):
        st.session_state.page = 'update_master_data'
        st.rerun()
    
    if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
        if start_get_together(pin1, pin2, custom_event_name):
            st.session_state.page = 'select_company'
            st.rerun()
initialize_session_state()

def check_event_end_time():
    while st.session_state.get_together_started:
        if datetime.now() >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.experimental_rerun()
        time.sleep(60)  # Check every minute     

def select_company():
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

def select_employee():
    display_header()
    st.markdown(f"<div class='important-text'>{get_text('Firma:', 'Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='important-text'>{get_text('Team:', 'Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        file_path = r"C:\Users\Konrad.Reyhe\Projektarbeit\Firmen_Teams_Mitarbeiter.csv"
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
                            # Check if employee is already added
                            is_added = employee in st.session_state.added_employees
                            button_key = f"employee_{employee}"
                            
                            if st.button(employee, key=button_key, use_container_width=True, 
                                         disabled=is_added):
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
                undo_message = get_text(
                    f'Mitarbeiter "{last_employee}" wurde von der Anwesenheitsliste entfernt.',
                    f'Employee "{last_employee}" has been removed from the attendance list.'
                )
                st.session_state.success_messages.append(undo_message)
                st.session_state.last_message_time = time.time()
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
                with open(banner_path, "rb") as f:
                    banner_image = f.read()
                st.image(banner_image, use_column_width=True)
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
    # Cancel any existing scheduled end
    cancel_scheduled_end()
    
    # Schedule new end
    thread = threading.Thread(target=wait_and_end_event, args=(end_time,))
    thread.daemon = True
    thread.start()
    st.session_state.end_thread = thread

def cancel_scheduled_end():
    if 'end_thread' in st.session_state and st.session_state.end_thread:
        # There's no direct way to stop a thread, so we'll use a flag
        st.session_state.cancel_end = True
        st.session_state.end_thread = None

def wait_and_end_event(end_time):
    st.session_state.cancel_end = False
    while datetime.now() < end_time:
        time.sleep(60)  # Check every minute
        if st.session_state.cancel_end:
            return  # Exit if cancellation is requested

    # If we've reached here, it's time to end the event
    end_get_together()
    send_csv_to_accounting()
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.experimental_rerun()

def send_csv_to_accounting():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_Final_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        df.to_csv(file_path, index=False, encoding='utf-8')
        
        # Email configuration
        sender_email = "your_email@example.com"  # Replace with your email
        receiver_email = "accounting@example.com"  # Replace with accounting email
        password = "your_email_password"  # Replace with your email password

        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"GetTogether Attendance List - {timestamp}"

        body = "Please find attached the attendance list for the GetTogether event."
        message.attach(MIMEText(body, "plain"))

        # Attach the CSV file
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )
        message.attach(part)

        # Send the email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            st.success("CSV sent to accounting successfully.")
        except Exception as e:
            st.error(f"Failed to send CSV to accounting: {str(e)}")

def end_get_together():
    if st.session_state.attendance_data:
        # Save the final CSV
        event_name = st.session_state.custom_event_name.replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{event_name}_Final_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        
        df = pd.DataFrame(st.session_state.attendance_data)
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        df['Event Name'] = st.session_state.custom_event_name
        df['Event End Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['Total Attendees'] = len(df)
        
        df.to_csv(file_path, index=False, encoding='utf-8')
        
        # Send CSV to accounting via email
        if send_csv_to_accounting(file_path, file_name):
            st.success(get_text("Anwesenheitsliste wurde gespeichert und per E-Mail an die Buchhaltung gesendet.",
                                "Attendance list has been saved and sent via email to accounting."))
        else:
            st.warning(get_text("Anwesenheitsliste wurde gespeichert, konnte aber nicht per E-Mail gesendet werden. Bitte manuell senden.",
                                "Attendance list has been saved but could not be sent via email. Please send manually."))
        
        # Provide download button for the final CSV
        with open(file_path, "rb") as f:
            st.download_button(
                label=get_text("Finale Anwesenheitsliste herunterladen", "Download Final Attendance List"),
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
        
        reset_session_state()
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

def end_get_together():
    if st.session_state.attendance_data:
        event_name = st.session_state.custom_event_name.replace(" ", "_")
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        
        # Try loading the auto-saved file if it exists
        auto_save_file = f"current_attendance_{event_name}.csv"
        auto_save_path = os.path.join(local_data_dir, auto_save_file)
        
        if os.path.exists(auto_save_path):
            df = pd.read_csv(auto_save_path)
        else:
            df = pd.DataFrame(st.session_state.attendance_data)
            if 'ID' in df.columns:
                df = df.drop('ID', axis=1)
        
        # Add extra details and save final file
        df['Event Name'] = st.session_state.custom_event_name
        df['Event End Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['Total Attendees'] = len(df)
        
        file_name = f"Anwesenheit_{event_name}_Final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(local_data_dir, file_name)
        df.to_csv(file_path, index=False, encoding='utf-8')
        
        # Provide download button for the final CSV
        with open(file_path, "rb") as f:
            st.download_button(
                label="Finale Anwesenheitsliste herunterladen",
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
        
        return True
    else:
        st.warning("Keine Anwesenheitsdaten zum Speichern vorhanden.")
        return False

      
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




# Call to start the navigation
initialize_session_state()
navigate()