import streamlit as st
from utils import get_text
from language_utils import toggle_language
from attendance import add_employee_to_attendance, submit_guest
from timer import start_timer
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import math
from math import ceil
from shared_functions import get_companies, get_teams_for_company, undo_last_employee_selection

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



def display_company_team_info():
    st.markdown(f"<div class='important-text'>{get_text('Firma:', 'Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='important-text'>{get_text('Team:', 'Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)
