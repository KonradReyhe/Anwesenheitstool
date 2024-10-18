#naigation.py
import streamlit as st

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
