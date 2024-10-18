#ui_components.py
import streamlit as st
from utils import get_text
from language_utils import toggle_language
from attendance import get_companies, get_teams_for_company, undo_last_employee_selection, add_employee_to_attendance, submit_guest
from timer import start_timer
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import math
from math import ceil

def display_employee_buttons(employees):
    num_cols = min(3, len(employees))
    num_rows = ceil(len(employees) / num_cols)
    
    container = st.container()
    with container:
        for row in range(num_rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                idx = row * num_cols + col
                if idx < len(employees):
                    with cols[col]:
                        employee = employees[idx]
                        is_added = employee in st.session_state.added_employees
                        button_key = f"employee_{employee}_{idx}"
                        
                        if st.button(employee, key=button_key, use_container_width=True, 
                                     disabled=is_added):
                            handle_employee_selection(employee)
                        
                        if is_added:
                            apply_selected_button_style(button_key)

def handle_employee_selection(employee):
    if employee not in st.session_state.added_employees:
        add_employee_to_attendance(employee)
        st.session_state.current_employee = employee
        
        if st.session_state.require_signature:
            st.session_state.show_signature_modal = True
        else:
            add_success_message(employee)
        
        if employee in st.session_state.custom_employee_messages:
            show_custom_employee_message(employee)
        
        start_timer()
        st.rerun()

def display_success_messages():
    with st.container():
        for message in st.session_state.success_messages:
            st.success(message)
    
    current_time = time.time()
    if st.session_state.last_message_time and current_time - st.session_state.last_message_time > 5:
        st.session_state.success_messages = []
        st.session_state.last_message_time = None

def handle_undo_last_selection():
    if st.session_state.added_employees:
        if st.button(get_text("Letzte Auswahl rückgängig machen", "Undo last selection"), 
                     key="undo_last_selection",
                     use_container_width=True):
            undo_last_employee_selection()

def show_custom_employee_message(employee):
    if employee in st.session_state.custom_employee_messages:
        st.markdown("### " + get_text("Wichtige Mitteilung", "Important Notice"))
        st.write(st.session_state.custom_employee_messages[employee])
        if st.button(get_text("Schließen", "Close"), key="close_custom_message"):
            st.session_state.show_custom_message = False
            st.rerun()

def select_team():
    display_header()
    display_company_team_info()
    
    teams = get_teams_for_company(st.session_state.selected_company)
    st.markdown(f"<div class='sub-header'>{get_text('Team auswählen:', 'Select team:')}</div>", unsafe_allow_html=True)
    
    num_columns = 3
    columns = st.columns(num_columns)
    
    for i, team in enumerate(teams):
        with columns[i % num_columns]:
            if st.button(team, key=f"team_{team}", use_container_width=True):
                select_team_callback(team)
    
    display_back_button()

def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
    st.experimental_rerun()

def apply_selected_button_style(button_key):
    st.markdown(f"""
        <style>
        #{button_key} {{
            background-color: #f9c61e !important;
            color: #ffffff !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def signature_modal():
    if st.session_state.show_signature_modal:
        with st.form(key='signature_form'):
            st.write(get_text("Bitte unterschreiben Sie hier:", "Please sign here:"))
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#000000",
                background_color="#ffffff",
                height=150,
                width=400,
                drawing_mode="freedraw",
                key="canvas",
            )
            submitted = st.form_submit_button(get_text("Unterschrift bestätigen", "Confirm Signature"))
            
        if submitted and canvas_result.image_data is not None:
            # Save the signature
            signature_path = f"signatures/{st.session_state.current_employee}_{int(time.time())}.png"
            Image.fromarray(canvas_result.image_data.astype('uint8')).save(signature_path)
            st.session_state.signatures[st.session_state.current_employee] = signature_path
            
            # Add employee to attendance
            add_employee_to_attendance(st.session_state.current_employee)
            
            st.session_state.show_signature_modal = False
            st.rerun()

def display_header():
    st.markdown(f"<div class='header'>{get_text('GetTogether Anwesenheitserfassung', 'GetTogether Attendance Tracking')}</div>", unsafe_allow_html=True)
    if st.button(get_text("Sprache ändern", "Change Language")):
        toggle_language()

def handle_signature_modal():
    if st.session_state.get('show_signature_modal', False):
        signature_modal()

def select_company():
    companies = get_companies()
    st.markdown(f"<div class='sub-header'>{get_text('Firma auswählen:', 'Select company:')}</div>", unsafe_allow_html=True)
    
    num_columns = 3
    columns = st.columns(num_columns)
    
    for i, company in enumerate(companies):
        with columns[i % num_columns]:
            if st.button(company, key=f"company_{company}", use_container_width=True):
                select_company_callback(company)
    
    if st.button(get_text("Gast hinzufügen", "Add Guest"), key="add_guest"):
        st.session_state.page = 'guest_info'
        st.experimental_rerun()

def select_company_callback(company):
    st.session_state.selected_company = company
    st.session_state.selected_team = None
    st.session_state.page = 'select_team'
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None
    st.experimental_rerun()

def display_back_button():
    if st.button(get_text("Zurück", "Back"), key="back_button"):
        st.session_state.page = 'home'
        st.experimental_rerun()

def display_company_team_info():
    if st.session_state.selected_company:
        st.markdown(f"<div class='company-info'>{get_text('Ausgewählte Firma:', 'Selected Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    if st.session_state.selected_team:
        st.markdown(f"<div class='team-info'>{get_text('Ausgewähltes Team:', 'Selected Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)

def guest_info():
    st.title(get_text("Gast-Information", "Guest Information"))
    st.session_state.guest_name = st.text_input(get_text("Name des Gastes", "Guest Name"))
    st.session_state.guest_company = st.text_input(get_text("Firma des Gastes", "Guest Company"))
    if st.button(get_text("Bestätigen", "Confirm")):
        submit_guest()
