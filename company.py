import streamlit as st
from utils import get_text
from attendance import get_companies
from streamlit import experimental_rerun

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
    if company in ["Externe Partner", "External Partners"]:
        st.session_state.selected_company = "Externe Partner"  # Always use the German version for CSV lookup
    else:
        st.session_state.selected_company = company

    if company in [get_text("Gast", "Guest"), "Gast", "Guest"]:  # Check for both German and English versions
        st.session_state.page = 'guest_info'
    else:
        st.session_state.page = 'select_team'


    
