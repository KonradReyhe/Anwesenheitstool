import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid
import platform

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
        color: #f9c220; /* Gelbfarbe */
        font-size: 32px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Sub-Header-Stil */
    .sub-header {
        color: #000000; /* Schwarze Farbe */
        font-size: 24px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Wichtige Textabschnitte in Schwarz */
    .important-text {
        color: #000000; /* Schwarze Farbe */
        font-size: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Button-Stil mit dünner gelber Umrandung und schwarzer Textfarbe */
    .stButton>button {
        border-radius: 12px;
        font-size: 16px;
        padding: 8px 16px;
        width: 100%;
        min-height: 40px; /* Setze eine minimale Höhe */
        border: 1px solid #f9c220; /* Dünne gelbe Umrandung */
        background-color: #FFFFFF; /* Weißer Hintergrund */
        color: #000000; /* Textfarbe der Buttons in Schwarz */
        white-space: normal; /* Erlaube Textumbruch */
        word-wrap: break-word; /* Erlaube Wortumbruch */
        text-align: center; /* Zentriere den Text */
    }

    /* Hover-Effekt für Buttons */
    .stButton>button:hover {
        background-color: #f0f0f0; /* Leicht grauer Hintergrund beim Hover */
    }

    /* TextInput-Stil */
    .stTextInput>div>div>input {
        border-radius: 12px;
        font-size: 16px;
        padding: 8px;
        border: 1px solid #000000; /* Schwarze Umrandung der Eingabefelder */
    }

    /* Banner-Stil */
    .banner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    /* Einstellungen-Button-Stil */
    .settings-button {
        background-color: #FFFFFF; /* Weißer Hintergrund */
        border: 1px solid #f9c220; /* Gelbe Umrandung */
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #000000; /* Schwarzer Text */
        margin-right: 20px;
    }

    /* Optionen-Panel-Stil */
    .options-panel {
        background-color: #FFFFFF; /* Weißer Hintergrund */
        padding: 20px;
        border: 1px solid #000000; /* Schwarze Umrandung */
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 300px;
    }

    /* Optionen-Titel */
    .options-title {
        font-size: 20px;
        margin-bottom: 10px;
        text-align: center;
        color: #000000; /* Schwarze Farbe */
    }

    /* Anwesenheits-Tabelle */
    .attendance-table {
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 10px;
    }

    /* Header Layout */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session-State Initialisierung
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

initialize_session_state()

# Gemeinsame Header-Funktion für alle Seiten
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
    # Linke Seite schließen
    # Rechte Seite: Einstellungen-Button
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("⚙️", key="settings_button"):
            st.session_state.show_admin_panel = not st.session_state.show_admin_panel
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

# Callback function zum Beenden des GetTogether
def end_get_together():
    # Generiere das detaillierte Anwesenheitsdokument lokal
    if st.session_state.attendance_data:
        # Definiere den lokalen Speicherpfad
        if platform.system() == "Windows":
            local_data_dir = r"C:\Users\Konrad.Reyhe\Projektarbeit\data"
        else:
            local_data_dir = "data"  # Für andere Betriebssysteme oder Streamlit Sharing

        os.makedirs(local_data_dir, exist_ok=True)  # Erstelle den Ordner, falls er nicht existiert

        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        file_path = os.path.join(local_data_dir, file_name)
        try:
            attendance_df.to_csv(file_path, index=False, encoding='utf-8')
            if platform.system() == "Windows":
                st.success(f"Anwesenheitsdokument '{file_name}' erfolgreich in '{local_data_dir}' gespeichert.")
            else:
                st.success(f"Anwesenheitsdokument '{file_name}' erfolgreich erstellt.")

            # Bereitstellen des Dokuments zum Download (funktioniert auch auf Streamlit Sharing)
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download Anwesenheitsdokument",
                    data=f,
                    file_name=file_name,
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Fehler beim Erstellen des Anwesenheitsdokuments: {e}")
    else:
        st.warning("Keine Anwesenheitsdaten zum Speichern vorhanden.")

    # Zurücksetzen der Session State Variablen und zur Startseite navigieren
    st.session_state.page = 'home'
    st.session_state.get_together_started = False
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.pin = None
    st.session_state.show_admin_panel = False
    st.session_state.attendance_data = []

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

# Funktionen für den Admin-Bereich
def admin_panel():
    st.markdown("<div class='options-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)
    entered_pin = st.text_input("PIN eingeben", type="password", key="entered_pin_admin")
    if entered_pin:
        if entered_pin == st.session_state.pin:
            st.button("GetTogether beenden", key="end_get_together_admin", on_click=end_get_together)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='sub-header'>Anwesenheit bearbeiten:</div>", unsafe_allow_html=True)
            # Anzeige der Anwesenheitsdaten mit Löschoption
            if st.session_state.attendance_data:
                st.markdown("<div class='attendance-table'>", unsafe_allow_html=True)
                attendance_df = pd.DataFrame(st.session_state.attendance_data)
                st.dataframe(attendance_df[['Name', 'Firma', 'Team', 'Zeit']])
                st.markdown("</div>", unsafe_allow_html=True)
                for record in st.session_state.attendance_data:
                    st.button(f"Löschen von {record['Name']} am {record['Zeit']}", key=f"delete_{record['ID']}", on_click=delete_attendance_record, args=(record['ID'],))
            else:
                st.warning("Keine Anwesenheitsdaten vorhanden.")
        else:
            st.error("Falscher PIN.")
    st.button("Abbrechen", key="cancel_admin_panel", on_click=lambda: setattr(st.session_state, 'show_admin_panel', False))
    st.markdown("</div>", unsafe_allow_html=True)

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

def select_team():
    display_header()
    st.markdown(f"<div class='important-text'>Firma: {st.session_state.selected_company}</div>", unsafe_allow_html=True)

    # Excel-Datei mit Mitarbeiterdaten laden
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.xlsx')

    if not os.path.exists(file_path):
        st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.")
        return

    try:
        df = pd.read_excel(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
    except Exception as e:
        st.error(f"Fehler beim Lesen der Excel-Datei: {e}")
        return

    teams = df[df["Firma"] == st.session_state.selected_company]["Team"].unique()

    if len(teams) == 0:
        st.warning("Keine Teams für die ausgewählte Firma gefunden.")
        return

    # Teams als Buttons anzeigen mit Teamnamen als Beschriftung
    st.markdown("<div class='sub-header'>Team auswählen:</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, team in enumerate(teams):
        with cols[idx % 3]:
            st.button(team, key=f"team_{team}", on_click=select_team_callback, args=(team,))

    # Zurück Button
    st.button("Zurück", on_click=go_back_to_company)

def select_employee():
    display_header()
    st.markdown(f"<div class='important-text'>Team: {st.session_state.selected_team}</div>", unsafe_allow_html=True)

    # Excel-Datei mit Mitarbeiterdaten laden
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'Firmen_Teams_Mitarbeiter.xlsx')

    if not os.path.exists(file_path):
        st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.")
        return

    try:
        df = pd.read_excel(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
    except Exception as e:
        st.error(f"Fehler beim Lesen der Excel-Datei: {e}")
        return

    employees = df[(df["Firma"] == st.session_state.selected_company) & (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()

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

# Funktionen für den Admin-Bereich
def admin_panel():
    st.markdown("<div class='options-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='options-title'>Admin Einstellungen</div>", unsafe_allow_html=True)
    entered_pin = st.text_input("PIN eingeben", type="password", key="entered_pin_admin")
    if entered_pin:
        if entered_pin == st.session_state.pin:
            st.button("GetTogether beenden", key="end_get_together_admin", on_click=end_get_together)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='sub-header'>Anwesenheit bearbeiten:</div>", unsafe_allow_html=True)
            # Anzeige der Anwesenheitsdaten mit Löschoption
            if st.session_state.attendance_data:
                st.markdown("<div class='attendance-table'>", unsafe_allow_html=True)
                attendance_df = pd.DataFrame(st.session_state.attendance_data)
                st.dataframe(attendance_df[['Name', 'Firma', 'Team', 'Zeit']])
                st.markdown("</div>", unsafe_allow_html=True)
                for record in st.session_state.attendance_data:
                    st.button(f"Löschen von {record['Name']} am {record['Zeit']}", key=f"delete_{record['ID']}", on_click=delete_attendance_record, args=(record['ID'],))
            else:
                st.warning("Keine Anwesenheitsdaten vorhanden.")
        else:
            st.error("Falscher PIN.")
    st.button("Abbrechen", key="cancel_admin_panel", on_click=lambda: setattr(st.session_state, 'show_admin_panel', False))
    st.markdown("</div>", unsafe_allow_html=True)

# Navigation basierend auf dem aktuellen Zustand
def navigate():
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

    # Anzeige des Admin-Panels, wenn aktiviert
    if st.session_state.show_admin_panel:
        admin_panel()

# Führen Sie die Navigation durch
navigate()
