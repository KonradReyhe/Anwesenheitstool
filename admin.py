# admin.py
import streamlit as st
import pandas as pd
from language_utils import toggle_language
from text_utils import get_text

from utils import end_get_together, save_attendance
from attendance import delete_attendance_record, save_current_attendance
from session_state import initialize_session_state

def show_admin_panel():
    st.session_state.show_admin_panel = True

def admin_settings():
    st.subheader(get_text("Admin-Einstellungen", "Admin Settings"))
    
    if st.button(get_text("Sprache ändern", "Change Language")):
        toggle_language()
    
    if st.button(get_text("Anwesenheitsdaten löschen", "Delete Attendance Data")):
        delete_attendance_record()
    
    if st.button(get_text("Aktuelle Anwesenheit speichern", "Save Current Attendance")):
        save_current_attendance()
    
    change_pin()
    update_master_data()
    set_custom_messages()
    update_accounting_email()
    end_get_together_button()
    remove_participants()

    # Add Datenschutz PIN update
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

def change_pin():
    new_pin = st.text_input(get_text("Neuer PIN", "New PIN"), type="password")
    if st.button(get_text("PIN ändern", "Change PIN")):
        st.session_state.pin = new_pin
        st.success(get_text("PIN wurde geändert", "PIN has been changed"))

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

def set_custom_messages():
    st.subheader(get_text("Benutzerdefinierte Nachrichten", "Custom Messages"))
    employee = st.text_input(get_text("Mitarbeiter", "Employee"))
    message = st.text_area(get_text("Nachricht", "Message"))
    if st.button(get_text("Nachricht speichern", "Save Message")):
        st.session_state.custom_employee_messages[employee] = message
        st.success(get_text("Nachricht gespeichert", "Message saved"))

def update_accounting_email():
    st.subheader(get_text("Buchhaltungs-E-Mail aktualisieren", "Update Accounting Email"))
    email = st.text_input(get_text("E-Mail-Adresse", "Email Address"))
    if st.button(get_text("E-Mail aktualisieren", "Update Email")):
        st.session_state.accounting_email = email
        st.success(get_text("E-Mail-Adresse aktualisiert", "Email address updated"))

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
    if st.button(get_text("Admin-Einstellungen", "Admin Settings")):
        st.session_state.page = 'admin_settings'
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
