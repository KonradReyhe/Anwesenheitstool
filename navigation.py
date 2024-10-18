import streamlit as st
from utils import get_text

def navigate():
    check_event_end()
    update_last_activity()
    apply_custom_styles()

    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company':
        select_company()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'admin_settings':
        admin_settings()
    elif st.session_state.page == 'update_master_data':
        update_master_data()
    else:
        st.error("Invalid page")


def go_back_to_company():
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.page = 'select_company'

def go_back_to_team_from_employee():
    st.session_state.page = 'select_team'
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None

def return_to_company_selection():
    st.session_state.page = 'select_company'
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.selected_employee = None
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None
    st.rerun()

def reset_to_company_selection():
    st.session_state.selected_company = None
    st.session_state.selected_team = None
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None
    st.session_state.page = 'select_company'

def reset_timer_state():
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None

def display_back_button():
    if st.button(get_text("Zurück", "Back"), key="back_button"):
        st.session_state.page = 'home'
        st.rerun()
