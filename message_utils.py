import streamlit as st
from utils import get_text

def show_custom_employee_message(employee):
    if employee in st.session_state.custom_employee_messages:
        message = st.session_state.custom_employee_messages[employee]
        st.info(get_text(f"Hinweis für {employee}: {message}", 
                         f"Note for {employee}: {message}"))
