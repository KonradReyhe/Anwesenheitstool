# admin.py

import streamlit as st
import pandas as pd
from text_utils import get_text
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

    # Custom CSS for styling
    st.markdown("""
    <style>
    .admin-block {
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #d0d7de;
    }
    .admin-block-title {
        color: #f9c61e;
        font-size: 20px;
        font-weight: bold;
    }
    .stButton > button {
        width: 100%;
        background-color: #f9c61e;
        color: white;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        border-radius: 5px;
    }
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border: none !important;
    }
    .streamlit-expanderContent {
        background-color: white;
        border-top: 1px solid #d0d7de;
    }
    </style>
    """, unsafe_allow_html=True)

    # Event Name Change
    with st.expander(get_text("Event-Name ändern", "Change Event Name"), expanded=False):
        st.markdown('<div class="admin-block">', unsafe_allow_html=True)
        with st.form(key='change_event_name_form'):
            new_event_name = st.text_input(get_text("Neuer Event-Name", "New Event Name"), value=st.session_state.get('custom_event_name', ''))
            submit_event_name = st.form_submit_button(get_text("Event-Name aktualisieren", "Update Event Name"))
            if submit_event_name:
                st.session_state.custom_event_name = new_event_name
                st.success(get_text("Event-Name wurde aktualisiert.", "Event Name has been updated."))
        st.markdown('</div>', unsafe_allow_html=True)

    # PIN Change
    with st.expander(get_text("PIN ändern", "Change PIN"), expanded=False):
        st.markdown('<div class="admin-block">', unsafe_allow_html=True)
        with st.form(key='change_pin_form'):
            new_pin = st.text_input(get_text("Neuer PIN", "New PIN"), type="password")
            confirm_new_pin = st.text_input(get_text("Neuen PIN bestätigen", "Confirm New PIN"), type="password")
            submit_pin = st.form_submit_button(get_text("PIN aktualisieren", "Update PIN"))
            if submit_pin:
                if new_pin and new_pin == confirm_new_pin:
                    st.session_state.pin = new_pin
                    st.success(get_text("PIN wurde aktualisiert.", "PIN has been updated."))
                elif not new_pin:
                    st.error(get_text("Bitte geben Sie einen gültigen PIN ein.", "Please enter a valid PIN."))
                else:
                    st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
        st.markdown('</div>', unsafe_allow_html=True)

    # Datenschutz PIN update
    with st.expander(get_text("Datenschutz PIN ändern", "Change Data Protection PIN"), expanded=False):
        st.markdown('<div class="admin-block">', unsafe_allow_html=True)
        with st.form(key='change_datenschutz_pin_form'):
            new_datenschutz_pin = st.text_input(get_text("Neuer Datenschutz PIN", "New Data Protection PIN"), type="password")
            confirm_new_datenschutz_pin = st.text_input(get_text("Neuen Datenschutz PIN bestätigen", "Confirm New Data Protection PIN"), type="password")
            submit_datenschutz_pin = st.form_submit_button(get_text("Datenschutz PIN aktualisieren", "Update Data Protection PIN"))
            if submit_datenschutz_pin:
                if new_datenschutz_pin and new_datenschutz_pin == confirm_new_datenschutz_pin:
                    st.session_state.datenschutz_pin = new_datenschutz_pin
                    st.session_state.datenschutz_pin_active = True
                    st.success(get_text("Datenschutz PIN wurde aktualisiert und aktiviert.", "Data Protection PIN has been updated and enabled."))
                elif not new_datenschutz_pin:
                    st.error(get_text("Bitte geben Sie einen gültigen PIN ein.", "Please enter a valid PIN."))
                else:
                    st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
        st.markdown('</div>', unsafe_allow_html=True)

    # Remove participants
    with st.expander(get_text("Teilnehmer entfernen", "Remove Participants"), expanded=False):
        st.markdown('<div class="admin-block">', unsafe_allow_html=True)
        remove_participants()
        st.markdown('</div>', unsafe_allow_html=True)

    # End GetTogether button
    with st.expander(get_text("GetTogether beenden", "End GetTogether"), expanded=False):
        st.markdown('<div class="admin-block">', unsafe_allow_html=True)
        end_get_together_button()
        st.markdown('</div>', unsafe_allow_html=True)

    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(get_text("Zurück", "Back"), key="admin_settings_back", use_container_width=True):
        st.session_state.page = 'select_company'
        st.session_state.show_admin_panel = False
        st.session_state.admin_access_granted = False


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

def admin_panel():
    admin_content = st.empty()
    with admin_content.container():
        st.markdown(
            f"<div class='sub-header' style='color: #f9c61e;'>{get_text('Admin Panel', 'Admin Panel')}</div>",
            unsafe_allow_html=True
        )

        # Adjust column ratios for better alignment
        col1, col2 = st.columns([3, 1])

        with col1:
            entered_pin = st.text_input(
                get_text("Admin PIN eingeben", "Enter Admin PIN"),
                type="password",
                key="admin_pin_input"
            )

        with col2:
            # Add some padding to vertically center the button
            st.markdown("<br>", unsafe_allow_html=True)
            enter_button = st.button(
                "Enter",
                key="admin_pin_enter",
                use_container_width=True
            )

        if enter_button or (entered_pin and st.session_state.get('_admin_pin_last', '') != entered_pin):
            if entered_pin == st.session_state.pin:
                st.session_state.admin_access_granted = True
                st.session_state.page = 'admin_settings'
                st.success(
                    get_text(
                        "Admin-Zugang gewährt. Sie werden zu den Einstellungen weitergeleitet.",
                        "Admin access granted. You will be redirected to the settings."
                    )
                )

            else:
                st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))

        st.session_state['_admin_pin_last'] = entered_pin

        # Add a cancel button aligned to the right
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            get_text("Abbrechen", "Cancel"),
            key="cancel_admin_panel"
        ):
            st.session_state.show_admin_panel = False

    return admin_content

def remove_participants():
    if st.session_state.attendance_data:
        for record in st.session_state.attendance_data:
            if st.button(f"Remove {record['Name']}", key=f"remove_{record['Name']}"):
                st.session_state.attendance_data.remove(record)
                st.session_state.added_employees.remove(record['Name'])
                st.success(f"{record['Name']} has been removed.")
                st.experimental_rerun()
    else:
        st.info(get_text("Keine Teilnehmer vorhanden.", "No participants available."))




