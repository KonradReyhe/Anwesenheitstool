import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid
import platform
import time

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

# Initialize session state
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
        st.session_state.guest_company = ''  # Optionales Feld für Firma
    if 'entered_pin' not in st.session_state:
        st.session_state.entered_pin = ''
    if 'attendance_data' not in st.session_state:
        st.session_state.attendance_data = []
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'confirmation_needed' not in st.session_state:  # Confirmation state for ending event
        st.session_state.confirmation_needed = False
    if 'new_pin' not in st.session_state:  # To track new PIN changes
        st.session_state.new_pin = None
    if 'admin_access_granted' not in st.session_state:  # Add this line to initialize the admin_access_granted variable
        st.session_state.admin_access_granted = False  # Initialize to False
    if 'last_interaction_time' not in st.session_state:  # Add this for handling inactivity
        st.session_state.last_interaction_time = time.time()


initialize_session_state()

def display_header():
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    # Linke Seite: Titel und Banner
    st.markdown("<div class='title'>GetTogether Anwesenheitstool</div>", unsafe_allow_html=True)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(script_dir, "logos")
    banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
    if os.path.exists(banner_path):
        try:
            with open(banner_path, "rb") as f:
                banner_image = f.read()
            # Anzeigen des Bildes mit einheitlicher Breite
            st.image(banner_image, use_column_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden des Banners: {e}")
    else:
        st.warning(f"Banner wurde nicht gefunden: {banner_path}")
    
    # Rechte Seite: Nur anzeigen, wenn GetTogether gestartet wurde
    if st.session_state.get_together_started:
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("⚙️", key="settings_button"):
                st.session_state.show_admin_panel = not st.session_state.show_admin_panel  # Toggle admin panel visibility
    st.markdown("</div>", unsafe_allow_html=True)




# Callback function für die Auswahl einer Firma
def select_company_callback(company):
    st.session_state.selected_company = company
    if company == "Gast":
        st.session_state.page = 'guest_info'
    else:
        st.session_state.page = 'select_team'

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

# Callback function zum Starten des GetTogether
def start_get_together():
    pin1 = st.session_state.pin1
    pin2 = st.session_state.pin2
    if pin1 and pin2:
        if pin1 == pin2:
            # Setze PIN und starte GetTogether
            st.session_state.pin = pin1
            st.session_state.get_together_started = True
            st.session_state.page = 'select_company'
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


# Callback function zum Zurückkehren zur Firmenauswahl
def go_back_to_company():
    st.session_state.page = 'select_company'
    st.session_state.selected_company = None
    st.session_state.selected_team = None

# Callback function zum Zurückkehren zum Team-Auswahl
def go_back_to_team_from_employee():
    st.session_state.page = 'select_team'
    st.session_state.selected_team = None

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
    
    reset_session_state()  # Reset session state after the event ends



# Show admin options after successful PIN entry and hide the company selection and PIN input
def admin_panel():
    # Timeout after inactivity
    timeout_duration = 300
    if st.session_state.admin_access_granted and (time.time() - st.session_state.last_interaction_time > timeout_duration):
        st.warning("Admin-Panel wegen Inaktivität geschlossen.")
        st.session_state.admin_access_granted = False
        st.session_state.show_admin_panel = False
        st.session_state.page = 'select_company'

    if not st.session_state.admin_access_granted:
        entered_pin = st.text_input("Admin PIN eingeben", type="password", key="entered_pin_admin")
        if entered_pin and entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True
            st.session_state.show_company_selection = False  # Hide company logos
            st.session_state.last_interaction_time = time.time()
            st.success("Adminzugang gewährt.")
        elif entered_pin:
            st.error("Falscher Admin PIN.")

    if st.session_state.admin_access_granted:
        st.session_state.entered_pin_admin = None  # Hide the PIN input after success
        st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)

        # Option to end GetTogether with confirmation
        if st.session_state.get_together_started:
            if not st.session_state.confirmation_needed:
                if st.button("GetTogether beenden"):
                    st.session_state.confirmation_needed = True
                    st.session_state.last_interaction_time = time.time()  # Update interaction time

            # Confirm the PIN again before ending the event
            if st.session_state.confirmation_needed:
                confirmation_pin = st.text_input("Bestätigen Sie den PIN zum Beenden", type="password")
                if confirmation_pin and confirmation_pin == st.session_state.pin:
                    end_get_together()
                    st.session_state.confirmation_needed = False
                    st.session_state.admin_access_granted = False  # Reset admin access after ending the event
                elif confirmation_pin:
                    st.error("Falscher PIN. Bitte erneut eingeben.")
                st.session_state.last_interaction_time = time.time()  # Update interaction time

        # Option to change the admin PIN (requires current PIN confirmation)
        st.markdown("<div class='sub-header'>PIN ändern:</div>", unsafe_allow_html=True)
        current_pin = st.text_input("Aktuellen PIN eingeben", type="password", key="current_pin")
        if current_pin == st.session_state.pin:
            new_pin1 = st.text_input("Neuen PIN eingeben", type="password", key="new_pin1")
            new_pin2 = st.text_input("Neuen PIN bestätigen", type="password", key="new_pin2")

            if new_pin1 and new_pin2:
                if new_pin1 == new_pin2:
                    st.session_state.pin = new_pin1
                    st.success("PIN wurde erfolgreich geändert!")
                    st.session_state.last_interaction_time = time.time()  # Update interaction time
                else:
                    st.error("Die neuen PINs stimmen nicht überein.")
        elif current_pin and current_pin != st.session_state.pin:
            st.error("Aktueller PIN ist falsch.")

        # Option to save the attendance data
        st.markdown("<div class='sub-header'>Anwesenheitsdokument speichern:</div>", unsafe_allow_html=True)
        if st.button("Anwesenheit speichern"):
            save_attendance()
            st.session_state.last_interaction_time = time.time()  # Update interaction time

        # Admin panel cancel button
        st.button("Abbrechen", key="cancel_admin_panel", on_click=lambda: setattr(st.session_state, 'admin_access_granted', False))

    # Update last interaction time if any interaction happens
    if st.session_state.admin_access_granted:
        st.session_state.last_interaction_time = time.time()

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

    st.markdown("<div class='important-text'>Bitte Firma auswählen:</div>", unsafe_allow_html=True)

    # Firmen mit Logos (ohne "SUB")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(script_dir, "logos")
    company_logos = {
        "4K Analytics": os.path.join(logo_dir, "4K ANALYTICS.png"),
        "CLINIBOTS": os.path.join(logo_dir, "CLINIBOTS.png"),
        "GREENBAY research": os.path.join(logo_dir, "GREENBAY research.png"),
        "InfAI Management": os.path.join(logo_dir, "InfAI Management.png"),
        "iNNO3": os.path.join(logo_dir, "iNNO3.png"),
        "Lieblingsimmobilien": os.path.join(logo_dir, "Lieblingsimmobilien.png"),
        "Termingo": os.path.join(logo_dir, "TERMINGO.png"),
        "Visgato": os.path.join(logo_dir, "visgato.png"),
        "WIG2": os.path.join(logo_dir, "WIG2.png"),
        "SUV": os.path.join(logo_dir, "SUV.png"),
        "Externe Partner": os.path.join(logo_dir, "Externe Partner.png"),
        "Gast": os.path.join(logo_dir, "Gast.png")
        # "SUB" wurde entfernt
    }

    # Gesamtliste der Firmen (inkl. mit und ohne Logos), "SUB" entfernt
    all_companies = [
        "4K Analytics",
        "CLINIBOTS",
        "GREENBAY research",
        "InfAI Management",
        "iNNO3",
        "Lieblingsimmobilien",
        "Termingo",
        "Visgato",
        "WIG2",
        "SUV",
        "Externe Partner",
        "Gast"
    ]

    # Gitter-Layout: 4 Spalten
    num_cols = 4
    companies_per_row = [all_companies[i:i + num_cols] for i in range(0, len(all_companies), num_cols)]

    # Anzeigen der Firmen in einem Gitter
    for row in companies_per_row:
        cols = st.columns(num_cols)
        for col, company in zip(cols, row):
            with col:
                if company in company_logos and os.path.exists(company_logos[company]):
                    try:
                        with open(company_logos[company], "rb") as f:
                            image = f.read()
                        # Anzeigen des Bildes mit einheitlicher Breite
                        st.image(image, width=150)
                        # Klickbarer Button unter dem Bild
                        st.button("Auswählen", key=f"select_{company}", on_click=select_company_callback, args=(company,))
                    except Exception as e:
                        st.error(f"Fehler beim Laden des Logos für {company}: {e}")
                else:
                    # Firmen ohne Logos (falls vorhanden)
                    st.button("Auswählen", key=f"select_{company}", on_click=select_company_callback, args=(company,))

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

# Auswahl der Teams
def select_team():
    display_header()
    st.markdown(f"<div class='important-text'>Firma: {st.session_state.selected_company}</div>", unsafe_allow_html=True)

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


def admin_panel():
    # Define timeout in seconds (e.g., 300 seconds = 5 minutes)
    timeout_duration = 300

    # Check if the admin access has timed out
    if st.session_state.admin_access_granted and (time.time() - st.session_state.last_interaction_time > timeout_duration):
        st.warning("Admin-Panel wegen Inaktivität geschlossen.")
        st.session_state.admin_access_granted = False
        st.session_state.show_admin_panel = False

    # Show the PIN input only if admin access has not been granted yet
    if not st.session_state.admin_access_granted:
        entered_pin = st.text_input("Admin PIN eingeben", type="password", key="entered_pin_admin")

        # Check if the entered PIN matches the current event PIN
        if entered_pin and entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True  # Grant admin access
            st.session_state.last_interaction_time = time.time()  # Reset the interaction time
            st.success("Adminzugang gewährt.")

    # Once admin access is granted, hide the PIN input field and show admin options
    if st.session_state.admin_access_granted:
        st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)

        # Option to end GetTogether with confirmation
        if st.session_state.get_together_started:
            if not st.session_state.confirmation_needed:
                if st.button("GetTogether beenden"):
                    st.session_state.confirmation_needed = True
                    st.session_state.last_interaction_time = time.time()  # Update interaction time

            # Confirm the PIN again before ending the event
            if st.session_state.confirmation_needed:
                confirmation_pin = st.text_input("Bestätigen Sie den PIN zum Beenden", type="password")
                if confirmation_pin and confirmation_pin == st.session_state.pin:
                    end_get_together()
                    st.session_state.confirmation_needed = False
                    st.session_state.admin_access_granted = False  # Reset admin access after ending the event
                elif confirmation_pin:
                    st.error("Falscher PIN. Bitte erneut eingeben.")
                st.session_state.last_interaction_time = time.time()  # Update interaction time

        # Option to change the admin PIN (requires current PIN confirmation)
        st.markdown("<div class='sub-header'>PIN ändern:</div>", unsafe_allow_html=True)
        current_pin = st.text_input("Aktuellen PIN eingeben", type="password", key="current_pin")
        if current_pin == st.session_state.pin:
            new_pin1 = st.text_input("Neuen PIN eingeben", type="password", key="new_pin1")
            new_pin2 = st.text_input("Neuen PIN bestätigen", type="password", key="new_pin2")

            if new_pin1 and new_pin2:
                if new_pin1 == new_pin2:
                    st.session_state.pin = new_pin1
                    st.success("PIN wurde erfolgreich geändert!")
                    st.session_state.last_interaction_time = time.time()  # Update interaction time
                else:
                    st.error("Die neuen PINs stimmen nicht überein.")
        elif current_pin and current_pin != st.session_state.pin:
            st.error("Aktueller PIN ist falsch.")

        # Option to save the attendance data
        st.markdown("<div class='sub-header'>Anwesenheitsdokument speichern:</div>", unsafe_allow_html=True)
        if st.button("Anwesenheit speichern"):
            save_attendance()
            st.session_state.last_interaction_time = time.time()  # Update interaction time

        # Admin panel cancel button
        st.button("Abbrechen", key="cancel_admin_panel", on_click=lambda: setattr(st.session_state, 'admin_access_granted', False))

    # Update last interaction time if any interaction happens
    if st.session_state.admin_access_granted:
        st.session_state.last_interaction_time = time.time()


def navigate():
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company' and not st.session_state.admin_access_granted:
        select_company()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()

    # Always display the admin panel when it's toggled (whether admin access is granted or not)
    if st.session_state.show_admin_panel:
        admin_panel()  # This will ensure that the admin panel PIN input is shown if not already granted

    # Call timeout after each interaction
    admin_panel_timeout()



def admin_panel_timeout():
    if st.session_state.admin_access_granted:
        # Close admin panel if no interaction happens within 300 seconds (5 minutes)
        if time.time() - st.session_state.last_interaction_time > 300:
            st.warning("Admin-Panel wegen Inaktivität geschlossen.")
            st.session_state.admin_access_granted = False
            st.session_state.show_admin_panel = False
            st.session_state.page = 'select_company'  # Return to company selection

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
    st.session_state.pin = None  # Reset the PIN after the event ends
    st.session_state.admin_access_granted = False  # Reset admin access
    st.session_state.show_admin_panel = False  # Close admin panel



# Call to start the navigation
initialize_session_state()
navigate()
