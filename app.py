import streamlit as st
import pandas as pd
import os
import requests

# Webseite Farben und Design anpassen
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .sub-header {
        color: #FFCC00;
        font-size: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 12px;
        font-size: 16px;
        padding: 8px 16px;
        width: 100%;
        height: 40px;
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        font-size: 16px;
        padding: 8px;
    }
    .banner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .gear-button {
        position: fixed;
        bottom: 20px;
        left: 20px; /* Untere linke Ecke */
        background-color: #f0f0f0;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .options-panel {
        position: fixed;
        bottom: 80px;
        left: 20px;
        background-color: white;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
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
    if 'entered_pin' not in st.session_state:
        st.session_state.entered_pin = ''

initialize_session_state()

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
    # Senden der Anwesenheitsdaten an den Backend-Server
    data = {
        'name': employee,
        'company': st.session_state.selected_company
    }
    try:
        response = requests.post('http://localhost:5000/add', json=data)
        if response.status_code == 200:
            st.success(f"Anwesenheit von {employee} erfolgreich erfasst!")
        else:
            st.error("Fehler beim Speichern der Anwesenheit.")
    except Exception as e:
        st.error(f"Fehler beim Verbinden mit dem Server: {e}")

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
    if guest_name:
        # Senden der Anwesenheitsdaten an den Backend-Server
        data = {
            'name': guest_name,
            'company': 'Gast'
        }
        try:
            response = requests.post('http://localhost:5000/add', json=data)
            if response.status_code == 200:
                st.success(f"Anwesenheit von Gast '{guest_name}' erfolgreich erfasst!")
            else:
                st.error("Fehler beim Speichern der Anwesenheit.")
        except Exception as e:
            st.error(f"Fehler beim Verbinden mit dem Server: {e}")

        # Zurück zur Firmenauswahl
        st.session_state.page = 'select_company'
        st.session_state.selected_company = None
        st.session_state.guest_name = None
    else:
        st.error("Bitte geben Sie Ihren Namen ein.")

# Callback function zum Beenden des GetTogether
def end_get_together():
    st.success("GetTogether wurde beendet.")
    # Zurücksetzen der Session State Variablen
    st.session_state.page = 'home'
    st.session_state.get_together_started = False
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.pin = None
    st.session_state.show_options_panel = False

# Callback function zum Zurückkehren zur Firmenauswahl
def go_back_to_company():
    st.session_state.page = 'select_company'
    st.session_state.selected_company = None
    st.session_state.selected_team = None

# Callback function zum Zurückkehren zum Team-Auswahl
def go_back_to_team_from_employee():
    st.session_state.page = 'select_team'
    st.session_state.selected_team = None

# Funktionen für die verschiedenen Seiten
def home():
    # Banner auf der Startseite
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(script_dir, "logos")
    banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")  # Korrigierter Dateiname
    if os.path.exists(banner_path):
        try:
            with open(banner_path, "rb") as f:
                banner_image = f.read()
            st.image(banner_image, use_column_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden des Banners: {e}")
    else:
        st.warning(f"Banner wurde nicht gefunden: {banner_path}")

    st.markdown("<div class='sub-header'>Bitte PIN setzen und GetTogether beginnen:</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Setze einen PIN für das GetTogether:", type="password", key="pin1")
    with col2:
        st.text_input("Bestätige den PIN:", type="password", key="pin2")
    
    st.button("GetTogether beginnen", on_click=start_get_together)

def select_company():
    # Banner anzeigen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(script_dir, "logos")
    banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
    if os.path.exists(banner_path):
        try:
            with open(banner_path, "rb") as f:
                banner_image = f.read()
            st.image(banner_image, use_column_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden des Banners: {e}")
    else:
        st.warning(f"Banner wurde nicht gefunden: {banner_path}")

    st.markdown("<div class='sub-header'>Bitte Firma auswählen:</div>", unsafe_allow_html=True)

    # Firmen mit Logos (ohne "SUB")
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

    # Optionen Zahnrad Button unten links (nur anzeigen, wenn GetTogether gestartet ist)
    if st.session_state.get_together_started:
        # Platzierung des Zahnrads mit eindeutigen Key
        if st.button("⚙️", key="gear_button_toggle_unique"):
            st.session_state.show_options_panel = not st.session_state.show_options_panel

        if st.session_state.show_options_panel:
            # Options Panel anzeigen
            st.markdown(
                """
                <div class='options-panel'>
                """,
                unsafe_allow_html=True
            )
            entered_pin = st.text_input("PIN eingeben", type="password", key="entered_pin_panel")
            if entered_pin:
                if entered_pin == st.session_state.pin:
                    if st.button("GetTogether beenden", key="end_get_together_panel"):
                        end_get_together()
                else:
                    st.error("Falscher PIN.")
            if st.button("Abbrechen", key="cancel_options_panel"):
                st.session_state.show_options_panel = False
            st.markdown("</div>", unsafe_allow_html=True)

# Funktion für die Gästeinformation
def guest_info():
    st.markdown("<div class='sub-header'>Bitte Ihren Namen eingeben:</div>", unsafe_allow_html=True)
    
    st.text_input("Name:", key="guest_name")
    st.button("Anwesenheit erfassen", on_click=submit_guest)

    st.button("Zurück", on_click=go_back_to_company)

# Funktion für die Teamauswahl
def select_team():
    st.markdown(f"<div class='sub-header'>Firma: {st.session_state.selected_company}</div>", unsafe_allow_html=True)

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

# Funktion für die Mitarbeiterauswahl
def select_employee():
    st.markdown(f"<div class='sub-header'>Team: {st.session_state.selected_team}</div>", unsafe_allow_html=True)

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

# Einstellungen Zahnrad anzeigen nur wenn GetTogether gestartet ist
def settings():
    # Da der Gear-Button bereits in select_company platziert ist, brauchen wir hier nichts
    pass

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

# Einstellungen immer anzeigen (hier wird der Gear Button nicht mehr hinzugefügt)
settings()

# Führen Sie die Navigation durch
navigate()
