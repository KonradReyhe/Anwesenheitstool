# admin.py

import streamlit as st
import pandas as pd
from text_utils import get_text
from session_state import initialize_session_state
from header import display_header
from utils import end_get_together
import time


def show_admin_panel():
    st.session_state.show_admin_panel = True

def admin_settings():
    display_header()

    if 'admin_page' not in st.session_state or st.session_state.admin_page is None:
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

        options = [
            ("change_event_name", get_text("Event-Name", "Event Name")),
            ("change_pin", get_text("PIN ändern", "Change PIN")),
            ("change_datenschutz_pin", get_text("Datenschutz PIN ändern", "Change Data Protection PIN")),
            ("remove_participants", get_text("Teilnehmer entfernen", "Remove Participants")),
            ("end_get_together", get_text("GetTogether beenden", "End GetTogether")),
        ]

        for option, label in options:
            if st.button(label, key=f"admin_{option}", use_container_width=True):
                st.session_state.admin_page = option
                st.rerun()

        if st.button(get_text("Zurück", "Back"), key="admin_settings_back", use_container_width=True):
            st.session_state.page = 'select_company'
            st.session_state.show_admin_panel = False
            st.session_state.admin_access_granted = False
            st.rerun()
    else:
        if st.session_state.admin_page == 'change_event_name':
            change_event_name_page()
        elif st.session_state.admin_page == 'change_pin':
            change_pin_page()
        elif st.session_state.admin_page == 'change_datenschutz_pin':
            change_datenschutz_pin_page()
        elif st.session_state.admin_page == 'remove_participants':
            remove_participants_page()
        elif st.session_state.admin_page == 'end_get_together':
            end_get_together_page()

def update_master_data():
    st.subheader(get_text("Stammdaten aktualisieren", "Update Master Data"))
    uploaded_file = st.file_uploader(get_text("CSV-Datei hochladen", "Upload CSV file"), type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df.to_csv("Firmen_Teams_Mitarbeiter.csv", index=False)
            st.success(get_text("Stammdaten erfolgreich aktualisiert", "Master data successfully updated"))
        except Exception as e:
            st.error(f"Error: {e}")



def end_get_together_button():
    if st.button(get_text("GetTogether beenden", "End GetTogether"), use_container_width=True):
        end_get_together()

def reset_admin_state():
    st.session_state.show_admin_panel = False
    st.session_state.admin_access_granted = False

def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()

def close_admin_panel():
    st.session_state.show_admin_panel = False

def confirm_end_get_together():
    st.subheader(get_text("GetTogether beenden", "End GetTogether"))
    pin = st.text_input(get_text("PIN eingeben", "Enter PIN"), type="password")
    if st.button(get_text("GetTogether beenden", "End GetTogether")):
        if pin == st.session_state.pin:
            end_get_together()
        else:
            st.error(get_text("Falscher PIN", "Incorrect PIN"))

@st.cache_data(ttl=300)  
def admin_panel():
    st.markdown(f"<div class='sub-header' style='color: #f9c61e;'>{get_text('Admin Panel', 'Admin Panel')}</div>", unsafe_allow_html=True)
    
    with st.form(key='admin_pin_form'):
        entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")
        submit_button = st.form_submit_button("Enter")
    
    if submit_button:
        if entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True
            st.session_state.page = 'admin_settings'
            st.rerun()
        else:
            st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))
    
    if st.button(get_text("Abbrechen", "Cancel"), key="cancel_admin_panel"):
        st.session_state.show_admin_panel = False
        st.rerun()

def remove_participants():
    if st.session_state.attendance_data:
        for record in st.session_state.attendance_data:
            if st.button(f"Remove {record['Name']}", key=f"remove_{record['Name']}"):
                st.session_state.attendance_data.remove(record)
                st.session_state.added_employees.remove(record['Name'])
                st.success(f"{record['Name']} has been removed.")
                st.rerun()
    else:
        st.info(get_text("Keine Teilnehmer vorhanden.", "No participants available."))





def change_event_name_page():
    display_styled_admin_page(
        get_text('Event-Name', 'Event Name'),
        get_text('Wird im Header angezeigt', 'Displayed in the header')
    )
    new_event_name = st.text_input(get_text("Neuer Event-Name", "New Event Name"), value=st.session_state.get('custom_event_name', ''))
    if st.button(get_text("Event-Name aktualisieren", "Update Event Name")):
        st.session_state.custom_event_name = new_event_name
        st.success(get_text("Event-Name wurde aktualisiert.", "Event Name has been updated."))
        st.rerun()
    back_to_admin_settings()

def change_pin_page():
    display_styled_admin_page(
        get_text('PIN ändern', 'Change PIN'),
        get_text('Sicherheits-PIN für den Admin-Zugang', 'Security PIN for admin access')
    )
    new_pin = st.text_input(get_text("Neuer PIN", "New PIN"), type="password")
    confirm_new_pin = st.text_input(get_text("Neuen PIN bestätigen", "Confirm New PIN"), type="password")
    if st.button(get_text("PIN aktualisieren", "Update PIN")):
        if new_pin and new_pin == confirm_new_pin:
            st.session_state.pin = new_pin
            st.success(get_text("PIN wurde aktualisiert.", "PIN has been updated."))
            st.rerun()
        elif not new_pin:
            st.error(get_text("Bitte geben Sie einen gültigen PIN ein.", "Please enter a valid PIN."))
        else:
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
    back_to_admin_settings()

def change_datenschutz_pin_page():
    display_styled_admin_page(
        get_text('Datenschutz PIN ändern', 'Change Data Protection PIN'),
        get_text('PIN für den Zugriff auf geschützte Daten', 'PIN for accessing protected data')
    )
    new_datenschutz_pin = st.text_input(get_text("Neuer Datenschutz PIN", "New Data Protection PIN"), type="password")
    confirm_new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN bestätigen", "Confirm New Data Protection PIN"), type="password")
    if st.button(get_text("Datenschutz PIN aktualisieren", "Update Data Protection PIN")):
        if new_datenschutz_pin and new_datenschutz_pin == confirm_new_datenschutz_pin:
            st.session_state.datenschutz_pin = new_datenschutz_pin
            st.session_state.datenschutz_pin_active = True
            st.success(get_text("Datenschutz PIN wurde aktualisiert und aktiviert.", "Data Protection PIN has been updated and enabled."))
        elif not new_datenschutz_pin:
            st.error(get_text("Bitte geben Sie einen gültigen PIN ein.", "Please enter a valid PIN."))
        else:
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
    back_to_admin_settings()

def remove_participants_page():
    display_styled_admin_page(
        get_text('Teilnehmer entfernen', 'Remove Participants'),
        get_text('Entfernt ausgewählte Teilnehmer aus der Liste', 'Removes selected participants from the list')
    )
    
    current_time = time.time()
    if 'removal_success_message' in st.session_state and 'removal_success_time' in st.session_state:
        if current_time - st.session_state.removal_success_time < 5:
            st.success(st.session_state.removal_success_message)
        else:
            del st.session_state.removal_success_message
            del st.session_state.removal_success_time

    if st.session_state.attendance_data:
        for record in st.session_state.attendance_data:
            with st.expander(f"{record['Name']} - {record['Firma']}"):
                st.write(f"{get_text('Team:', 'Team:')} {record['Team']}")
                st.write(f"{get_text('Zeit:', 'Time:')} {record['Zeit']}")
                
                confirm_key = f"confirm_remove_{record['Name']}"
                if confirm_key not in st.session_state:
                    st.session_state[confirm_key] = False
                
                if not st.session_state[confirm_key]:
                    if st.button(get_text("Entfernen", "Remove"), key=f"remove_{record['Name']}"):
                        st.session_state[confirm_key] = True
                        st.rerun()
                else:
                    st.warning(get_text(f"Sind Sie sicher, dass Sie {record['Name']} entfernen möchten?", 
                                        f"Are you sure you want to remove {record['Name']}?"))
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(get_text("Ja, entfernen", "Yes, remove"), key=f"confirm_{record['Name']}"):
                            st.session_state.attendance_data.remove(record)
                            st.session_state.added_employees.remove(record['Name'])
                            st.session_state.removal_success_message = get_text(f"{record['Name']} wurde erfolgreich entfernt.", 
                                                                                f"{record['Name']} has been successfully removed.")
                            st.session_state.removal_success_time = time.time()
                            del st.session_state[confirm_key]
                            st.rerun()
                    with col2:
                        if st.button(get_text("Abbrechen", "Cancel"), key=f"cancel_{record['Name']}"):
                            st.session_state[confirm_key] = False
                            st.rerun()
    else:
        st.info(get_text("Keine Teilnehmer vorhanden.", "No participants available."))
    back_to_admin_settings()

def end_get_together_page():
    display_styled_admin_page(
        get_text('GetTogether beenden', 'End GetTogether'),
        get_text('Beendet das aktuelle GetTogether-Event und sendet eine CSV-Datei an die Buchhaltungs-E-Mail',
                 'Ends the current GetTogether event and sends a CSV file to the accounting email')
    )
    pin_input = st.text_input(get_text("PIN eingeben", "Enter PIN"), type="password", key="end_gathering_pin")
    if st.button(get_text("GetTogether beenden", "End GetTogether"), use_container_width=True):
        if pin_input == st.session_state.pin:
            end_get_together()
            st.rerun()
        else:
            st.error(get_text("Falscher PIN", "Incorrect PIN"))
    back_to_admin_settings()

def back_to_admin_settings():
    if st.button(get_text("Zurück zu Admin-Einstellungen", "Back to Admin Settings")):
        st.session_state.admin_page = None
        st.rerun()

def display_styled_admin_page(title, description):
    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h2 style="
                color: #f9c61e;
                margin-bottom: 5px;
            ">{title}</h2>
            <p style="
                color: #666;
                font-style: italic;
                margin-bottom: 20px;
            ">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def confirm_removal(name):
    return st.warning(
        get_text(
            f"Sind Sie sicher, dass Sie {name} entfernen möchten?",
            f"Are you sure you want to remove {name}?"
        ),
        icon="⚠️"
    ) and st.button(
        get_text("Ja, entfernen", "Yes, remove"),
        key=f"confirm_{name}"
    )
















