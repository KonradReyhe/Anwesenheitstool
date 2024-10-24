# admin.py

import streamlit as st
import pandas as pd
from text_utils import get_text
from utils import end_get_together
from header import display_header
from shared_components import display_styled_admin_page, back_to_admin_settings
from auth import compare_digest

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
            ("change_event_name", get_text("Event-Name ändern", "Change Event Name")),
            ("change_pin", get_text("PIN ändern", "Change PIN")),
            ("change_datenschutz_pin", get_text("Datenschutz PIN ändern", "Change Data Protection PIN")),
            ("remove_participants", get_text("Teilnehmer entfernen", "Remove Participants")),
            ("toggle_signature_requirement", get_text("Unterschriftspflicht ändern", "Toggle Signature Requirement")),
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
        admin_page = st.session_state.admin_page
        if admin_page == "change_event_name":
            change_event_name_page()
        elif admin_page == "change_pin":
            change_pin_page()
        elif admin_page == "change_datenschutz_pin":
            change_datenschutz_pin_page()
        elif admin_page == "remove_participants":
            remove_participants_page()
        elif admin_page == "toggle_signature_requirement":
            toggle_signature_requirement_page()
        elif admin_page == "end_get_together":
            end_get_together_page()
        else:
            st.error(get_text("Unbekannte Admin-Seite", "Unknown admin page"))
            st.session_state.admin_page = None
            st.rerun()

def change_event_name_page():
    display_styled_admin_page(
        get_text('Event-Name ändern', 'Change Event Name'),
        get_text('Hier können Sie den Namen des aktuellen Events ändern.',
                 'Here you can change the name of the current event.')
    )
    current_name = st.session_state.get('custom_event_name', "")
    new_event_name = st.text_input(get_text("Neuer Event-Name", "New Event Name"), value=current_name)
    if st.button(get_text('Speichern', 'Save'), key='save_event_name'):
        st.session_state.custom_event_name = new_event_name.strip()
        st.success(get_text('Der Event-Name wurde aktualisiert.', 'Event name has been updated.'))
        st.session_state.admin_page = None
        st.rerun()
    back_to_admin_settings()

def change_pin_page():
    display_styled_admin_page(
        get_text('PIN ändern', 'Change PIN'),
        get_text('Hier können Sie den Admin-PIN ändern.',
                 'Here you can change the admin PIN.')
    )
    new_pin = st.text_input(get_text("Neuer PIN", "New PIN"), type="password")
    confirm_new_pin = st.text_input(get_text("Neuen PIN bestätigen", "Confirm New PIN"), type="password")
    if st.button(get_text('Speichern', 'Save'), key='save_new_pin'):
        if new_pin and new_pin == confirm_new_pin:
            st.session_state.pin = new_pin
            st.success(get_text('Der PIN wurde erfolgreich geändert.', 'PIN has been changed successfully.'))
            st.session_state.admin_page = None
            st.rerun()
        else:
            st.error(get_text('Die eingegebenen PINs stimmen nicht überein.', 'The entered PINs do not match.'))
    back_to_admin_settings()

def change_datenschutz_pin_page():
    display_styled_admin_page(
        get_text('Datenschutz PIN ändern', 'Change Data Protection PIN'),
        get_text('PIN für den Zugriff auf geschützte Daten', 'PIN for accessing protected data')
    )

    datenschutz_pin_active = st.checkbox(
        get_text("Datenschutz PIN aktivieren", "Enable Data Protection PIN"),
        value=st.session_state.get('datenschutz_pin_active', False)
    )

    if datenschutz_pin_active:
        new_datenschutz_pin = st.text_input(get_text("Neuer Datenschutz PIN", "New Data Protection PIN"), type="password")
        confirm_new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN bestätigen", "Confirm New Data Protection PIN"), type="password")
        if st.button(get_text("Datenschutz PIN aktualisieren", "Update Data Protection PIN")):
            if new_datenschutz_pin and new_datenschutz_pin == confirm_new_datenschutz_pin:
                st.session_state.datenschutz_pin = new_datenschutz_pin
                st.session_state.datenschutz_pin_active = True
                st.success(get_text("Datenschutz PIN wurde aktualisiert und aktiviert.", "Data Protection PIN has been updated and enabled."))
                st.session_state.admin_page = None
                st.rerun()
            else:
                st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
    else:
        if st.button(get_text("Datenschutz PIN deaktivieren", "Disable Data Protection PIN")):
            st.session_state.datenschutz_pin = None
            st.session_state.datenschutz_pin_active = False
            st.success(get_text("Datenschutz PIN wurde deaktiviert.", "Data Protection PIN has been disabled."))
            st.session_state.admin_page = None
            st.rerun()
    back_to_admin_settings()

def remove_participants_page():
    display_styled_admin_page(
        get_text('Teilnehmer entfernen', 'Remove Participants'),
        get_text('Hier können Sie Teilnehmer aus der Anwesenheitsliste entfernen.',
                 'Here you can remove participants from the attendance list.')
    )

    if not st.session_state.get('attendance_data'):
        st.info(get_text('Keine Teilnehmer in der Anwesenheitsliste.', 'No participants in the attendance list.'))
        back_to_admin_settings()
        return

    attendance_df = pd.DataFrame(st.session_state.attendance_data)
    participants = attendance_df['Name'].unique()

    participant_to_remove = st.selectbox(get_text('Wählen Sie einen Teilnehmer aus', 'Select a participant'), participants)
    if st.button(get_text('Entfernen', 'Remove'), key='remove_participant'):
        st.session_state.attendance_data = [record for record in st.session_state.attendance_data if record['Name'] != participant_to_remove]
        st.session_state.added_employees.remove(participant_to_remove)
        st.success(get_text(f'{participant_to_remove} wurde entfernt.', f'{participant_to_remove} has been removed.'))
        st.session_state.admin_page = None
        st.rerun()
    back_to_admin_settings()

def toggle_signature_requirement_page():
    display_styled_admin_page(
        get_text('Unterschriftspflicht ändern', 'Toggle Signature Requirement'),
        get_text('Hier können Sie die Unterschriftspflicht für Mitarbeiter aktivieren oder deaktivieren.',
                 'Here you can enable or disable the signature requirement for employees.')
    )
    current_status = st.session_state.get('require_signature', False)
    new_status = st.checkbox(
        get_text('Unterschrift von Mitarbeitern verlangen', 'Require employee signature'),
        value=current_status
    )
    if st.button(get_text('Speichern', 'Save'), key='save_signature_requirement'):
        st.session_state.require_signature = new_status
        st.success(get_text('Die Unterschriftspflicht wurde aktualisiert.', 'Signature requirement has been updated.'))
        st.session_state.admin_page = None
        st.rerun()
    back_to_admin_settings()

def end_get_together_page():
    display_styled_admin_page(
        get_text('GetTogether beenden', 'End GetTogether'),
        get_text('Beendet das aktuelle GetTogether-Event und sendet eine ZIP-Datei mit der CSV-Datei und der Unterschriften-PDF an die Buchhaltungs-E-Mail.',
                 'Ends the current GetTogether event and sends a ZIP file containing the CSV file and signatures PDF to the accounting email.')
    )
    pin_input = st.text_input(get_text("PIN eingeben", "Enter PIN"), type="password", key="end_gathering_pin")
    if st.button(get_text("GetTogether beenden", "End GetTogether"), use_container_width=True):
        if pin_input == st.session_state.pin:
            end_get_together()
            st.success(get_text("GetTogether wurde erfolgreich beendet.", "GetTogether has been successfully ended."))
            st.session_state.admin_page = None
            st.rerun()
        else:
            st.error(get_text("Falscher PIN", "Incorrect PIN"))
    back_to_admin_settings()

def admin_panel():
    display_header()
    st.markdown(
        f"<div class='sub-header' style='color: #f9c61e;'>{get_text('Admin Panel', 'Admin Panel')}</div>",
        unsafe_allow_html=True
    )

    with st.form(key='admin_pin_form'):
        entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")
        submit_button = st.form_submit_button(get_text("Enter", "Enter"))

    if submit_button:
        if compare_digest(entered_pin, st.session_state.pin):
            st.session_state.admin_access_granted = True
            st.session_state.page = 'admin_settings'
            st.rerun()
        else:
            st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))

    if st.button(get_text("Abbrechen", "Cancel"), key="cancel_admin_panel"):
        st.session_state.show_admin_panel = False
        st.rerun()
