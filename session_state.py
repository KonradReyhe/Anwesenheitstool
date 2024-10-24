#session_state.py
import streamlit as st
import os
import time

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'language' not in st.session_state:
        st.session_state.language = 'de'  
    if 'get_together_started' not in st.session_state:
        st.session_state.get_together_started = False
    if 'pin' not in st.session_state:
        st.session_state.pin = None
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = None
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None
    if 'attendance_data' not in st.session_state:
        st.session_state.attendance_data = []
    if 'added_employees' not in st.session_state:
        st.session_state.added_employees = []
    if 'signatures' not in st.session_state:
        st.session_state.signatures = {}
    if 'require_signature' not in st.session_state:
        st.session_state.require_signature = False
    if 'show_signature_modal' not in st.session_state:
        st.session_state.show_signature_modal = False
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None
    if 'custom_event_name' not in st.session_state:
        st.session_state.custom_event_name = ""
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'datenschutz_pin' not in st.session_state:
        st.session_state.datenschutz_pin = None
    if 'datenschutz_pin_active' not in st.session_state:
        st.session_state.datenschutz_pin_active = False
    if 'locked' not in st.session_state:
        st.session_state.locked = False
    if 'last_activity_time' not in st.session_state:
        st.session_state.last_activity_time = time.time()
    if 'accounting_email' not in st.session_state:
        st.session_state.accounting_email = None 
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None
    if 'custom_employee_messages' not in st.session_state:
        st.session_state.custom_employee_messages = {}
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'selected_company_temp' not in st.session_state:
        st.session_state.selected_company_temp = None

def initialize_employee_session_state():
    if 'current_company_team' not in st.session_state:
        st.session_state.current_company_team = None
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None


