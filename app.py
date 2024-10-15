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
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'custom_message' not in st.session_state:
        st.session_state.custom_message = ''
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'    
    if 'employee_just_added' not in st.session_state:
        st.session_state.employee_just_added = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None    
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

def start_get_together(pin1, pin2, custom_event_name, end_time):
    if pin1 and pin2 and pin1 == pin2:
        st.session_state.pin = pin1
        st.session_state.get_together_started = True
        
        # Set custom event name
        st.session_state.custom_event_name = custom_event_name if custom_event_name else "GetTogether"
        
        # Set end time if provided
        if end_time:
            end_datetime = datetime.combine(datetime.today(), end_time)
            st.session_state.end_time = end_datetime
            # Start a background thread to check for event end time
            threading.Thread(target=check_event_end_time, daemon=True).start()
        else:
            st.session_state.end_time = None
        
        st.success("GetTogether gestartet!")
        return True
    else:
        if not pin1 or not pin2:
            st.error("Bitte beide PIN-Felder ausfüllen.")
        elif pin1 != pin2:
            st.error("Die eingegebenen PINs stimmen nicht überein.")
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

def admin_settings():
    """
    Function to display the Admin Einstellungen with attendance management, 
    PIN change option, event name change, automatic end time adjustment,
    custom message setting, and end GetTogether option.
    """
    # Styled and centered title
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

    # Custom Message Setting
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

    # Event Name Change
    st.markdown(f"<div class='sub-header'>{get_text('Event Name ändern:', 'Change Event Name:')}</div>", unsafe_allow_html=True)
    new_event_name = st.text_input(get_text("Neuer Event Name:", "New Event Name:"), value=st.session_state.custom_event_name)
    if st.button(get_text("Event Name aktualisieren", "Update Event Name")):
        st.session_state.custom_event_name = new_event_name
        st.success(get_text(f"Event Name wurde zu '{new_event_name}' geändert.", f"Event Name has been changed to '{new_event_name}'."))

        # Display the updated event name in yellow
        st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)

    # Automatic End Time Adjustment
    st.markdown(f"<div class='sub-header'>{get_text('Automatisches Ende anpassen:', 'Adjust Automatic End Time:')}</div>", unsafe_allow_html=True)
    new_end_time = st.time_input(
        get_text("Neues automatisches Ende:", "New automatic end time:"),
        value=st.session_state.end_time.time() if st.session_state.end_time else None
    )
    if st.button(get_text("Endzeit aktualisieren", "Update End Time")):
        if new_end_time:
            new_end_datetime = datetime.combine(datetime.today(), new_end_time)
            if new_end_datetime > datetime.now():
                st.session_state.end_time = new_end_datetime
                st.success(get_text(f"Automatisches Ende wurde auf {new_end_time.strftime('%H:%M')} Uhr gesetzt.",
                                    f"Automatic end time has been set to {new_end_time.strftime('%H:%M')}."))
            else:
                st.error(get_text("Die neue Endzeit muss in der Zukunft liegen.", "The new end time must be in the future."))
        else:
            st.session_state.end_time = None
            st.success(get_text("Automatisches Ende wurde entfernt.", "Automatic end time has been removed."))

    # Display current attendees
    st.markdown(f"<div class='sub-header'>{get_text('Aktuelle Anwesenheitsliste:', 'Current Attendance List:')}</div>", unsafe_allow_html=True)
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

    # PIN change option in an expander
    with st.expander(get_text("PIN ändern", "Change PIN")):
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

    # Add some space before the End GetTogether option
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Option to end GetTogether (moved to the bottom)
    if st.session_state.get_together_started:
        st.markdown(f"<div class='sub-header'>{get_text('GetTogether beenden:', 'End GetTogether:')}</div>", unsafe_allow_html=True)
        
        end_pin = st.text_input(get_text("PIN eingeben zum Beenden des GetTogethers:", "Enter PIN to end the GetTogether:"), type="password", key="end_pin")
        
        # Use columns to make the button wider
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(get_text("GetTogether beenden", "End GetTogether"), key="end_gettogether_button", use_container_width=True):
                if end_pin == st.session_state.pin:
                    if end_get_together():
                        st.success(get_text("GetTogether wurde beendet und die Anwesenheitsliste wurde gespeichert.",
                                            "GetTogether has been ended and the attendance list has been saved."))
                        time.sleep(2)  # Give user time to see the success message
                        st.session_state.page = 'home'  # Return to home page after ending
                        st.rerun()
                else:
                    st.error(get_text("Falscher PIN. GetTogether konnte nicht beendet werden.",
                                      "Incorrect PIN. GetTogether could not be ended."))

    # Add some space before the Zurück button
    st.markdown("<br>", unsafe_allow_html=True)

    # Show Zurück button in admin settings
    if st.button(get_text("Zurück", "Back"), key="admin_settings_back", use_container_width=True):
        st.session_state.page = 'select_company'  # Navigate directly to the company selection page
        st.session_state.show_admin_panel = False  # Ensure admin panel is closed
        st.session_state.admin_access_granted = False  # Reset admin access
        st.rerun()  # Trigger rerun to refresh the UI


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
    
    end_time = st.time_input(get_text("Automatisches Ende des Events (optional):", "Automatic end time of the event (optional):"), value=None, key="end_time_input")
    
    if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
        if start_get_together(pin1, pin2, custom_event_name, end_time):
            st.session_state.page = 'select_company'
            st.rerun()

# Make sure to call initialize_session_state() at the beginning of your main script
initialize_session_state()

def check_event_end_time():
    while True:
        if datetime.now() >= st.session_state.end_time:
            end_get_together()
            break
        time.sleep(60)  # Check every minute           

def select_company():
    display_header()
    
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
        st.markdown(f"<div class='important-text'>{get_text('Bitte Firma auswählen:', 'Please select a company:')}</div>", unsafe_allow_html=True)
        
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
            st.button("SUV", key="SUV", on_click=select_company_callback, args=("SUV",), use_container_width=True)
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.csv')
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.csv')
        if not os.path.exists(file_path):
            st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.")
            return
        try:
            df = pd.read_csv(file_path)
            df.columns = ['Firma', 'Team', 'Mitarbeiter']
            employees = df[(df["Firma"] == st.session_state.selected_company) & 
                           (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
        except Exception as e:
            st.error(f"Fehler beim Lesen der CSV-Datei: {e}")
            return
        if len(employees) == 0:
            st.warning("Keine Mitarbeiter für das ausgewählte Team gefunden.")
            return

        st.markdown("<div class='sub-header'>{}</div>".format(get_text("Mitarbeiter auswählen:", "Select employee:")), unsafe_allow_html=True)
        
        # Initialize session state variables
        if 'added_employees' not in st.session_state:
            st.session_state.added_employees = []
        if 'timer_active' not in st.session_state:
            st.session_state.timer_active = False
        if 'countdown_start_time' not in st.session_state:
            st.session_state.countdown_start_time = None
        if 'current_company_team' not in st.session_state:
            st.session_state.current_company_team = None
        if 'employee_just_added' not in st.session_state:
            st.session_state.employee_just_added = False

        # Check if company or team has changed
        current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
        if st.session_state.current_company_team != current_company_team:
            reset_timer_state()
            st.session_state.current_company_team = current_company_team

        # Custom CSS for the buttons and success message
        st.markdown("""
            <style>
            .stButton > button {
                width: 100%;
            }
            .employee-added {
                background-color: #ffcccb !important;
                color: #000000 !important;
            }
            .success-message {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                margin-bottom: 20px;
                font-size: 18px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Display success message if an employee was just added
        if st.session_state.employee_just_added:
            st.markdown(f"""
                <div class="success-message">
                    {get_text('Mitarbeiter erfolgreich hinzugefügt!', 'Employee successfully added!')}
                </div>
            """, unsafe_allow_html=True)
            st.session_state.employee_just_added = False  # Reset the flag
        
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
                                st.session_state.employee_just_added = True  # Set the flag
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
        
        # Check if timer is active
        if st.session_state.timer_active and st.session_state.countdown_start_time:
            # Calculate remaining time
            elapsed_time = time.time() - st.session_state.countdown_start_time
            remaining_time = max(0, 10 - int(elapsed_time))
            
            # Display countdown
            st.info(f"{get_text('Zurück zur Firmenauswahl in', 'Back to company selection in')} {remaining_time} {get_text('Sekunden...', 'seconds...')}")
            
            # If the countdown is finished, reset and go back to company selection
            if remaining_time == 0:
                reset_timer_state()
                st.session_state.page = 'select_company'
                st.session_state.selected_company = None
                st.session_state.selected_team = None
                st.session_state.selected_employee = None
                st.rerun()
        
        # Automatically refresh the app every second to update the countdown
        if st.session_state.timer_active:
            st_autorefresh(interval=1000, key="timer_autorefresh")

        # Zurück Button
        if st.button(get_text("Zurück", "Back"), key="back_button"):
            reset_timer_state()
            go_back_to_team_from_employee()
            st.rerun()  # Force an immediate rerun


def reset_timer_state():
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.current_company_team = None           


def display_header():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'

    # Create a container for the header
    header_container = st.container()

    with header_container:
        # Title
        title = get_text("GetTogether Anwesenheitstool", "GetTogether Attendance Tool")
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
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
            button_container = st.container()
            with button_container:
                if st.session_state.get_together_started:
                    if st.button("⚙️", key="settings_button", help=get_text("Admin-Einstellungen", "Admin Settings")):
                        st.session_state.show_admin_panel = not st.session_state.show_admin_panel
                        st.rerun()
                else:
                    st.empty()  # Placeholder to maintain layout
                
                # Language toggle button
                language_toggle = "EN" if st.session_state.language == 'DE' else "DE"
                st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    # Add version number at the bottom right
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

    # Input for admin PIN
    entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")

    # Check entered PIN against the stored PIN automatically
    if entered_pin == st.session_state.pin:
        st.session_state.admin_access_granted = True
        st.session_state.page = 'admin_settings'
        st.success(get_text("Admin-Zugang gewährt. Sie werden zu den Einstellungen weitergeleitet.", 
                            "Admin access granted. You will be redirected to the settings."))
        st.rerun()
    elif entered_pin and entered_pin != st.session_state.pin:
        st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))

    # Show Zurück button
    if st.button(get_text("Zurück", "Back"), key="back_from_admin_panel"):
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