# admin.py

import streamlit as st
import pandas as pd
from text_utils import get_text
from state_management import delete_attendance_record, save_current_attendance
from session_state import initialize_session_state
from header import display_header
from utils import end_get_together


def show_admin_panel():
    st.session_state.show_admin_panel = True

def admin_settings():
    display_header()

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

    # PIN Change
    st.markdown(f"<div class='sub-header'>{get_text('PIN ändern:', 'Change PIN:')}</div>", unsafe_allow_html=True)
   

    # Datenschutz PIN update
    st.markdown(f"<div class='sub-header'>{get_text('Datenschutz PIN:', 'Data Protection PIN:')}</div>", unsafe_allow_html=True)
    new_datenschutz_pin = st.text_input(get_text("Neuer Datenschutz PIN", "New Data Protection PIN"), type="password")
    confirm_new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN bestätigen", "Confirm New Data Protection PIN"), type="password")
    
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

    # Remove participants
    st.markdown(f"<div class='sub-header'>{get_text('Teilnehmer entfernen:', 'Remove Participants:')}</div>", unsafe_allow_html=True)
    remove_participants()

    # End GetTogether button
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether beenden:', 'End GetTogether:')}</div>", unsafe_allow_html=True)
    end_get_together_button()

    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(get_text("Zurück", "Back"), key="admin_settings_back", use_container_width=True):
        st.session_state.page = 'select_company'
        st.session_state.show_admin_panel = False
        st.session_state.admin_access_granted = False
        st.rerun()


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
    if st.button(get_text("GetTogether beenden", "End GetTogether")):
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

def admin_panel():
    st.markdown(f"<div class='sub-header' style='color: #f9c61e;'>{get_text('Admin Panel', 'Admin Panel')}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")

    with col2:
        enter_button = st.button("Enter", key="admin_pin_enter")

    if enter_button:
        if entered_pin == st.session_state.pin:
            st.session_state.admin_access_granted = True
            st.session_state.page = 'admin_settings'
            st.success(get_text("Admin-Zugang gewährt. Sie werden zu den Einstellungen weitergeleitet.", 
                                "Admin access granted. You will be redirected to the settings."))
            st.rerun()
        else:
            st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))

    if st.button(get_text("Abbrechen", "Cancel"), key="cancel_admin_panel"):
        st.session_state.page = 'select_company'
        st.session_state.show_admin_panel = False
        st.session_state.admin_access_granted = False
        st.rerun()

def remove_participants():
    st.subheader(get_text("Teilnehmer entfernen", "Remove Participants"))
    if st.session_state.attendance_data:
        for record in st.session_state.attendance_data:
            if st.button(f"Remove {record['Name']}", key=f"remove_{record['Name']}"):
                st.session_state.attendance_data.remove(record)
                st.session_state.added_employees.remove(record['Name'])
                st.success(f"{record['Name']} has been removed.")
                st.rerun()
    else:
        st.info(get_text("Keine Teilnehmer vorhanden.", "No participants available."))
