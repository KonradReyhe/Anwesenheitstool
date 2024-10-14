import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="streamlit")
import pandas as pd
import os
from datetime import datetime, timedelta
import threading
import uuid
import time
import base64


st.markdown(
    """
    <style>
    /* Allgemeine Schriftarten und Farben */
    body {
        font-family: Arial, sans-serif;
        background-color: #FFFFFF; /* Weißer Hintergrund */
    }
    /* Titel-Stil */
    .title {
        color: #f9c61e; /* Gelb passend zur Webseite */
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    /* Sub-Header-Stil */
    .sub-header {
        color: #0095be; /* Blauton passend zur Webseite */
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Wichtige Textabschnitte */
    .important-text {
        color: #000000;
        font-size: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Button-Stil - Minimalistisch und Outline */
    .stButton>button {
        border-radius: 12px;
        font-size: 18px;
        padding: 15px;
        width: 100%;
        min-height: 60px; /* Größere Höhe für einfache Bedienung */
        border: 2px solid #f9c61e; /* Gelbe Umrandung */
        background-color: #FFFFFF; /* Weißer Hintergrund */
        color: #0095be; /* Blaue Schrift */
        text-align: center;
        white-space: normal;
        word-wrap: break-word;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Leichter Schatten für Button */
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease; /* Weicher Übergang bei Hover */
    }
    /* Hover-Effekt für Buttons */
    .stButton>button:hover {
        background-color: #f9c61e; /* Gelber Hintergrund beim Hover */
        color: #ffffff; /* Weiße Schrift beim Hover */
        border-color: #f9c61e; /* Gelb bleibt */
    }
    /* TextInput-Stil */
    .stTextInput>div>div>input {
        border-radius: 12px;
        font-size: 18px;
        padding: 12px;
        border: 2px solid #0095be; /* Blaue Umrandung */
        background-color: #f9f9f9; /* Leichtes Grau für Eingabefelder */
        color: #000000;
    }
    /* Optionen-Panel und Admin-Panel-Stil */
    .options-panel {
        background-color: #FFFFFF;
        padding: 20px;
        border: 2px solid #0095be;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
    }
    .options-title {
        font-size: 24px;
        margin-bottom: 10px;
        text-align: center;
        color: #f9c61e;
        font-weight: bold;
    }
    /* Anwesenheits-Tabelle */
    .attendance-table {
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 10px;
    }
    /* Header-Layout */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    /* Banner-Stil */
    .banner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
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
initialize_session_state()

# Callback function für die Auswahl einer Firma
def select_company_callback(company):
    st.session_state.selected_company = company
    if company == "Gast":
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
    st.success(f"Anwesenheit von {employee} erfolgreich erfasst!")
    # Zurück zur Firmenauswahl
    st.session_state.page = 'select_company'
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
# Function to save attendance outside of ending GetTogether

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

def close_admin_panel():
    """
    Resets session state related to the admin panel and navigates back to the company selection.
    """
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'
    trigger_rerun()  # Trigger a rerun after closing the panel

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

def end_get_together():
    if st.session_state.attendance_data:
        # Create a detailed DataFrame
        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        
        # Add extra details
        attendance_df['Event Name'] = st.session_state.custom_event_name
        attendance_df['Event End Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_df['Total Attendees'] = len(attendance_df)
        
        # Reorder columns for better readability
        column_order = ['Event Name', 'Event End Time', 'Total Attendees', 'ID', 'Name', 'Firma', 'Team', 'Zeit']
        attendance_df = attendance_df.reindex(columns=column_order)

        # Generate file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        event_name = st.session_state.custom_event_name.replace(" ", "_")
        file_name = f"Anwesenheit_{event_name}_{timestamp}.csv"
        
        # Save CSV
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')

        # Provide download button for the saved CSV
        with open(file_path, "rb") as f:
            st.download_button(
                label="Anwesenheitsliste herunterladen",
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
        
        return True
    else:
        st.warning("Keine Anwesenheitsdaten zum Speichern vorhanden.")
        return False

# Update the CSS to include styling for the custom event name
st.markdown(
    """
    <style>
    /* ... (previous styles) ... */
    .event-name {
        color: #f9c61e;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def admin_settings():
    """
    Function to display the Admin Einstellungen with attendance management and PIN change option.
    """
    st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)

    # Option to end GetTogether
    if st.session_state.get_together_started:
        st.markdown("<div class='sub-header'>GetTogether beenden:</div>", unsafe_allow_html=True)
        
        # Use columns to place the input and button side by side
        col1, col2 = st.columns([3, 1])
        with col1:
            end_pin = st.text_input("PIN eingeben zum Beenden des GetTogethers:", type="password", key="end_pin")
        with col2:
            if st.button("GetTogether beenden"):
                if end_pin == st.session_state.pin:
                    if end_get_together():
                        st.success("GetTogether wurde beendet und die Anwesenheitsliste wurde gespeichert.")
                        st.rerun()
                else:
                    st.error("Falscher PIN. GetTogether konnte nicht beendet werden.")

    # Display current attendees
    st.markdown("<div class='sub-header'>Aktuelle Anwesenheitsliste:</div>", unsafe_allow_html=True)
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        st.dataframe(df[['Name', 'Firma', 'Team', 'Zeit']])

        # Option to delete an attendee
        st.markdown("<div class='sub-header'>Teilnehmer entfernen:</div>", unsafe_allow_html=True)
        
        # Create a dictionary mapping names to IDs
        name_to_id = {f"{record['Name']} ({record['Firma']})": record['ID'] for record in st.session_state.attendance_data}
        
        # Create a list of names for the dropdown
        attendee_names = list(name_to_id.keys())
        
        selected_name = st.selectbox("Wählen Sie einen Teilnehmer zum Entfernen:", 
                                     options=attendee_names)
        
        if st.button("Teilnehmer entfernen"):
            if selected_name:
                selected_id = name_to_id[selected_name]
                delete_attendance_record(selected_id)
                st.success(f"{selected_name} wurde aus der Anwesenheitsliste entfernt.")
                st.rerun()
            else:
                st.warning("Bitte wählen Sie einen Teilnehmer aus.")

        # Option to save current attendance list
        st.markdown("<div class='sub-header'>Aktuelle Anwesenheitsliste speichern:</div>", unsafe_allow_html=True)
        if st.button("Anwesenheitsliste speichern"):
            save_current_attendance()
    else:
        st.info("Noch keine Teilnehmer angemeldet.")

    # Option to change PIN
    st.markdown("<div class='sub-header'>PIN ändern:</div>", unsafe_allow_html=True)
    current_pin = st.text_input("Aktuellen PIN eingeben", type="password", key="current_pin")
    new_pin = st.text_input("Neuen PIN eingeben", type="password", key="new_pin")
    confirm_new_pin = st.text_input("Neuen PIN bestätigen", type="password", key="confirm_new_pin")

    if st.button("PIN ändern"):
        if current_pin == st.session_state.pin:
            if new_pin == confirm_new_pin:
                st.session_state.pin = new_pin
                st.success("PIN wurde erfolgreich geändert!")
            else:
                st.error("Die neuen PINs stimmen nicht überein.")
        else:
            st.error("Der aktuelle PIN ist falsch.")

    # Show Zurück button in admin settings
    if st.button("Zurück", key="admin_settings_back"):
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

def save_current_attendance():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_Zwischenstand_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        df.to_csv(file_path, index=False, encoding='utf-8')
        st.success(f"Anwesenheitsliste '{file_name}' erfolgreich gespeichert.")
        
        # Provide download button for the saved CSV
        with open(file_path, "rb") as f:
            st.download_button(
                label="Anwesenheitsliste herunterladen",
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
    else:
        st.warning("Keine Anwesenheitsdaten zum Speichern vorhanden.")

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
    st.markdown("<div class='sub-header'>Bitte PIN setzen und GetTogether konfigurieren:</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pin1 = st.text_input("Setze einen PIN für das GetTogether:", type="password", key="pin1")
    with col2:
        pin2 = st.text_input("Bestätige den PIN:", type="password", key="pin2")
    
    # Custom event name input
    custom_event_name = st.text_input("Name des Events (optional):", key="custom_event_name_input")
    
    # Automatic end time input
    end_time = st.time_input("Automatisches Ende des Events (optional):", value=None, key="end_time_input")
    
    if st.button("GetTogether beginnen"):
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
    
    # Always display custom event name
    st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)
    
    # Admin panel (placed above the company selection)
    if st.session_state.show_admin_panel:
        admin_panel()  # Show the admin panel
    
    # Only show the company selection if admin access is not granted
    if not st.session_state.admin_access_granted:
        # Firmen mit Logos
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
        st.markdown("<div class='important-text'>Bitte Firma auswählen:</div>", unsafe_allow_html=True)
        # Custom CSS for making the logos non-clickable and buttons uniform in size
        st.markdown("""
            <style>
            .company-container {
                text-align: center;
                padding: 10px;
                margin: 10px;
            }
            .company-logo {
                width: 100%;
                max-width: 150px;  /* Set max width for logos */
                display: block;
                margin-left: auto;
                margin-right: auto;
                pointer-events: none; /* Prevent clicking on the logo */
            }
                    .event-name {
                color: #f9c61e;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                margin-top: 10px;
                margin-bottom: 20px;
            }        
            .fixed-button {
                width: 100%;  /* Ensures uniform button size */
                height: 60px;  /* Fixed height for the buttons */
                font-size: 16px;
                margin-top: 10px;
            }
            .grid-button {
                text-align: center;
                width: 100%;
            }
            </style>
        """, unsafe_allow_html=True)
        # Display companies with logos in a 3x3 grid
        num_cols = 3
        company_list_with_logos = list(company_logos.keys())
        companies_per_row = [company_list_with_logos[i:i + num_cols] for i in range(0, len(company_list_with_logos), num_cols)]
        # Display companies with logos
        for row in companies_per_row:
            cols = st.columns(num_cols)
            for col, company in zip(cols, row):
                with col:
                    if company in company_logos:  # Display logo for companies with logos
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
        # Align SUV, Externe Partner, and Gast buttons in the next row below
        st.markdown("<hr style='border-top: 1px solid #f9c61e;'>", unsafe_allow_html=True)  # Add a separator line
        st.markdown("<div class='important-text'>Weitere Auswahl:</div>", unsafe_allow_html=True)
        cols = st.columns(3)  # Three buttons in one row, aligned below the 3x3 grid
        with cols[0]:
            st.button("SUV", key="SUV", on_click=select_company_callback, args=("SUV",), use_container_width=True)
        with cols[1]:
            st.button("Externe Partner", key="Externe Partner", on_click=select_company_callback, args=("Externe Partner",), use_container_width=True)
        with cols[2]:
            st.button("Gast", key="Gast", on_click=select_company_callback, args=("Gast",), use_container_width=True)

def guest_info():
    display_header()
    st.markdown("<div class='sub-header'>Bitte Ihren Namen eingeben:</div>", unsafe_allow_html=True)
    st.text_input("Name:", key="guest_name")
    st.text_input("Firma (optional):", key="guest_company")  # Optionales Firmenfeld
    st.button("Anwesenheit erfassen", on_click=submit_guest)
    st.button("Zurück", on_click=go_back_to_company)
# Auswahl der Teams

def select_team():
    display_header()
    st.markdown(f"<div class='important-text'>Firma: {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    # Read the CSV file instead of Excel
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.csv')
    if not os.path.exists(file_path):
        st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.")
        return
    try:
        # Load CSV with 3 columns: Firma, Team, Mitarbeiter
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']  # Assign the columns
        # Filter teams based on the selected company
        teams = df[df["Firma"] == st.session_state.selected_company]["Team"].unique()
    except Exception as e:
        st.error(f"Fehler beim Lesen der CSV-Datei: {e}")
        return
    if len(teams) == 0:
        st.warning("Keine Teams für die ausgewählte Firma gefunden.")
        return
    # Teams as buttons
    st.markdown("<div class='sub-header'>Team auswählen:</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, team in enumerate(teams):
        with cols[idx % 3]:
            st.button(team, key=f"team_{team}", on_click=select_team_callback, args=(team,))
    # Zurück Button
    st.button("Zurück", on_click=go_back_to_company)
# Auswahl der Mitarbeiter

def select_employee():
    display_header()
    st.markdown(f"<div class='important-text'>Team: {st.session_state.selected_team}</div>", unsafe_allow_html=True)
    # Read the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.csv')
    if not os.path.exists(file_path):
        st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.")
        return
    try:
        # Load CSV with 3 columns: Firma, Team, Mitarbeiter
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']  # Assign the columns
        # Filter employees based on selected company and team
        employees = df[(df["Firma"] == st.session_state.selected_company) & 
                       (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
    except Exception as e:
        st.error(f"Fehler beim Lesen der CSV-Datei: {e}")
        return
    if len(employees) == 0:
        st.warning("Keine Mitarbeiter für das ausgewählte Team gefunden.")
        return
    # Mitarbeiterauswahl als Buttons mit Mitarbeiternamen als Beschriftung
    st.markdown("<div class='sub-header'>Mitarbeiter auswählen:</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, employee in enumerate(employees):
        with cols[idx % 3]:
            st.button(employee, key=f"employee_{employee}", on_click=select_employee_callback, args=(employee,))
    # Zurück Button
    st.button("Zurück", on_click=go_back_to_team_from_employee)

def display_header():
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    # Linke Seite: Titel und Banner
    st.markdown("<div class='title'>GetTogether Anwesenheitstool</div>", unsafe_allow_html=True)
    # Adding the banner
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(script_dir, "logos")
    banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
    if os.path.exists(banner_path):
        try:
            with open(banner_path, "rb") as f:
                banner_image = f.read()
            st.image(banner_image, use_column_width=True)  # Display banner centered and full width
        except Exception as e:
            st.error(f"Fehler beim Laden des Banners: {e}")
    else:
        st.warning(f"Banner wurde nicht gefunden: {banner_path}")
    # Show Admin options button only if GetTogether has started
    if st.session_state.get_together_started:
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("⚙️", key="settings_button"):
                # Toggle admin panel visibility and reset admin access if it is hidden
                st.session_state.show_admin_panel = not st.session_state.show_admin_panel
                st.session_state.admin_access_granted = False
    st.markdown("</div>", unsafe_allow_html=True)

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
    elif st.session_state.page == 'admin_panel':
        admin_panel()
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
    """
    Function to display the Admin Panel with PIN prompt.
    Once the correct PIN is entered, it automatically navigates to the Admin Einstellungen page.
    """
    st.markdown("<div class='sub-header' style='color: #f9c61e;'>Admin Panel</div>", unsafe_allow_html=True)

    # Input for admin PIN
    entered_pin = st.text_input("Admin PIN eingeben", type="password", key="admin_pin_input")

    # Check entered PIN against the stored PIN automatically
    if entered_pin == st.session_state.pin:
        st.session_state.admin_access_granted = True
        st.session_state.page = 'admin_settings'
        st.success("Admin-Zugang gewährt. Sie werden zu den Einstellungen weitergeleitet.")
        st.rerun()
    elif entered_pin and entered_pin != st.session_state.pin:
        st.error("Falscher Admin PIN.")

    # Show Zurück button
    if st.button("Zurück", key="back_from_admin_panel"):
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
            
def reset_session_state():
    st.session_state.page = 'home'
    st.session_state.get_together_started = False
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.attendance_data = []
    st.session_state.pin = None
    st.session_state.admin_access_granted = False
    st.session_state.show_admin_panel = False
    # Reset custom event name and end time
    st.session_state.custom_event_name = "GetTogether"
    st.session_state.end_time = None



# Call to start the navigation
initialize_session_state()
navigate()