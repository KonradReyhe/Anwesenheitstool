import streamlit as st
import warnings

# Suppress specific FutureWarnings related to the use of st.experimental_get_query_params
warnings.filterwarnings("ignore", category=FutureWarning, module="streamlit")

# Rest of your imports
import pandas as pd
import os
from datetime import datetime
import uuid
import platform
import time
import base64

# Webseite Farben und Design anpassen
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
    if 'new_pin' not in st.session_state:
        st.session_state.new_pin = None
    if 'admin_access_granted' not in st.session_state:
        st.session_state.admin_access_granted = False
    if 'last_interaction_time' not in st.session_state:
        st.session_state.last_interaction_time = time.time()
    if 'trigger_rerun' not in st.session_state:
        st.session_state.trigger_rerun = False  # Trigger for manual rerun
    if 'show_bottom_back_button' not in st.session_state:  # Initialize the back button visibility state
        st.session_state.show_bottom_back_button = True  # Default to True to show it initially





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

def start_get_together():
    pin1 = st.session_state.pin1
    pin2 = st.session_state.pin2
    if pin1 and pin2:
        if pin1 == pin2:
            # Set the session state PIN
            st.session_state.pin = pin1
            st.session_state.get_together_started = True
            st.session_state.page = 'select_company'
            st.success("GetTogether gestartet!")
        else:
            st.error("Die eingegebenen PINs stimmen nicht überein.")
    else:
        st.error("Bitte beide PIN-Felder ausfüllen.")


# Callback function zum Einreichen der Gast-Information
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
    This function resets the necessary session state variables and navigates back to the company selection screen
    without needing an experimental rerun.
    """
    # Reset the page state to 'select_company'
    st.session_state.page = 'select_company'

    # Clear admin panel related states if the admin panel was open
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False

    # Reset selected team and employee to start fresh when returning to company selection
    st.session_state.selected_team = None
    st.session_state.selected_employee = None



def close_admin_panel():
    # Reset session state and rerun the app
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'
    trigger_rerun()  # Trigger a rerun after closing the panel






def go_back_to_team_from_employee():
    # Navigate back to the team selection screen
    st.session_state.page = 'select_team'
    st.session_state.selected_employee = None
    st.session_state.show_admin_panel = False  # Close admin panel if open



# Callback function zum Löschen eines Anwesenheitseintrags
def delete_attendance_record(record_id):
    st.session_state.attendance_data = [record for record in st.session_state.attendance_data if record['ID'] != record_id]
    st.success("Anwesenheitseintrag erfolgreich gelöscht!")

def end_get_together():
    if st.session_state.attendance_data:
        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')
        st.success(f"GetTogether beendet und Anwesenheitsdokument '{file_name}' gespeichert.")
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Anwesenheitsdokument",
                data=f,
                file_name=file_name,
                mime="text/csv"
            )
    reset_session_state()
    trigger_rerun()  # Trigger rerun after the event ends




def admin_panel():
    """
    Function to display the Admin Panel with options like deleting attendance, saving CSV, changing PIN, and ending the event.
    It also handles timeouts if the admin panel is left open for too long.
    """
    timeout_duration = 300  # 5-minute timeout for admin panel

    # Check if admin access has timed out
    if st.session_state.admin_access_granted and (time.time() - st.session_state.last_interaction_time > timeout_duration):
        st.warning("Admin-Panel wegen Inaktivität geschlossen.")
        close_admin_panel()

    # Show the Admin PIN input only if access hasn't been granted yet
    if not st.session_state.admin_access_granted and st.session_state.show_admin_panel:
        st.markdown("<div class='sub-header' style='color: #f9c61e;'>Admin Panel</div>", unsafe_allow_html=True)
        
        # Input for admin PIN
        entered_pin = st.text_input("Admin PIN eingeben", type="password", key="entered_pin_admin")
        
        # Check entered PIN against the stored PIN
        if entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True
            st.session_state.last_interaction_time = time.time()  # Reset interaction time
            st.success("Adminzugang gewährt.")
        elif entered_pin:
            st.error("Falscher Admin PIN.")

    # Show admin settings only after successful PIN entry
    if st.session_state.admin_access_granted:
        st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)

        # Display signed-in employees and allow removal
        if st.session_state.attendance_data:
            st.markdown("<div class='sub-header'>Angemeldete Mitarbeiter:</div>", unsafe_allow_html=True)
            for idx, record in enumerate(st.session_state.attendance_data):
                st.write(f"{idx + 1}. **Name:** {record['Name']}, **Firma:** {record['Firma']}, **Zeit:** {record['Zeit']}")
                if st.button(f"Eintrag löschen {idx + 1}", key=f"remove_{record['ID']}"):
                    delete_attendance_record(record['ID'])
        else:
            st.warning("Keine Mitarbeiter angemeldet.")

        # Option to save attendance list as CSV
        if st.session_state.attendance_data:
            with st.expander("Anwesenheitsliste speichern"):
                if st.button("Anwesenheitsliste als CSV speichern"):
                    save_attendance()

        # PIN change option
        with st.expander("PIN ändern"):
            current_pin = st.text_input("Aktuellen PIN eingeben", type="password", key="current_pin_change")
            new_pin1 = st.text_input("Neuen PIN eingeben", type="password", key="new_pin1")
            new_pin2 = st.text_input("Neuen PIN bestätigen", type="password", key="new_pin2")
            
            if st.button("PIN ändern"):
                if current_pin == st.session_state.pin:
                    if new_pin1 == new_pin2:
                        st.session_state.pin = new_pin1
                        st.success("PIN erfolgreich geändert!")
                    else:
                        st.error("Die neuen PINs stimmen nicht überein.")
                else:
                    st.error("Aktueller PIN ist falsch.")

        # End GetTogether event with confirmation
        if st.session_state.get_together_started:
            if not st.session_state.confirmation_needed:
                if st.button("GetTogether beenden"):
                    st.session_state.confirmation_needed = True

            if st.session_state.confirmation_needed:
                confirmation_pin = st.text_input("Bestätigen Sie den PIN zum Beenden", type="password", key="confirmation_pin")
                if confirmation_pin == st.session_state.pin:
                    end_get_together()
                    st.session_state.confirmation_needed = False
                    st.session_state.admin_access_granted = False
                    reset_to_company_selection()
                elif confirmation_pin:
                    st.error("Falscher PIN. Bitte erneut eingeben.")

    # Add Zurück button to return to company selection
    if st.button("Zurück", key="admin_panel_return"):
        go_back_to_company()



def reset_to_company_selection():
    """
    Resets session states related to the admin panel and navigates back to the company selection page.
    """
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'


def reset_admin_state():
    # Reset the necessary session states in the right order
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'
    st.experimental_rerun()  # Force rerun to reflect state change

# This function handles closing the admin panel and resetting relevant session state flags
def close_admin_panel():
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False
    st.session_state.page = 'select_company'



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

    st.markdown("<div class='sub-header'>Bitte PIN setzen und GetTogether beginnen:</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Setze einen PIN für das GetTogether:", type="password", key="pin1")
    with col2:
        st.text_input("Bestätige den PIN:", type="password", key="pin2")

    st.button("GetTogether beginnen", on_click=start_get_together)

def select_company():
    display_header()

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
    elif st.session_state.page == 'select_company' and not st.session_state.admin_access_granted:
        select_company()  # The admin panel is already called in select_company()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()

    # Remove this line:
    # if st.session_state.show_admin_panel:
    #     admin_panel()

    admin_panel_timeout()  # Keep the timeout functionality for the admin panel


def admin_panel_timeout():
    if st.session_state.admin_access_granted:
        # Close admin panel if no interaction happens within 300 seconds (5 minutes)
        if time.time() - st.session_state.last_interaction_time > 300:
            st.warning("Admin-Panel wegen Inaktivität geschlossen.")
            st.session_state.admin_access_granted = False
            st.session_state.show_admin_panel = False
            st.session_state.page = 'select_company'


def show_admin_panel():
    if not st.session_state.admin_access_granted:
        entered_pin = st.text_input("Admin PIN eingeben", type="password", key="entered_pin_admin")
        if entered_pin and entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True  # Grant access
            st.session_state.show_company_selection = False  # Hide company logos
            st.session_state.entered_pin_admin = None  # Clear the PIN input
            st.session_state.last_interaction_time = time.time()  # Reset the interaction timer
            st.success("Adminzugang gewährt.")
        elif entered_pin:
            st.error("Falscher Admin PIN.")

    if st.session_state.admin_access_granted:
        st.session_state.entered_pin_admin = None  # Remove PIN input after success
        st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)

        # Example of options within the admin panel
        if st.session_state.get_together_started:
            if not st.session_state.confirmation_needed:
                if st.button("GetTogether beenden"):
                    st.session_state.confirmation_needed = True
            confirm_end_get_together()  # Handle confirmation for ending the event



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




# Call to start the navigation
initialize_session_state()
navigate()