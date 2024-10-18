import pandas as pd
import streamlit as st
from utils import get_text
import time
from navigation import return_to_company_selection

def get_companies():
    # Implementation of get_companies function
    pass

def get_teams_for_company(company):
    # Implementation of get_teams_for_company function
    pass

def undo_last_employee_selection():
    # Implementation of undo_last_employee_selection function
    pass

def get_employees_for_company_team(company, team):
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        employees = df[(df['Firma'] == company) & (df['Team'] == team)]['Mitarbeiter'].tolist()
        return sorted(employees)
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return []

def check_company_team_change():
    current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
    if st.session_state.get('current_company_team') != current_company_team:
        st.session_state.added_employees = []
        st.session_state.current_company_team = current_company_team
        st.session_state.timer_active = False
        st.session_state.countdown_start_time = None
        st.session_state.success_messages = []
        st.session_state.last_message_time = None
        st.session_state.all_employees_added_time = None

def check_all_employees_added(employees):
    if st.session_state.all_employees_added_time:
        time_since_all_added = time.time() - st.session_state.all_employees_added_time
        if time_since_all_added <= 5:
            st.info(get_text(f"Alle Teammitglieder wurden hinzugefügt. Kehre in {5 - int(time_since_all_added)} Sekunden zur Firmenauswahl zurück...",
                             f"All team members have been added. Returning to company selection in {5 - int(time_since_all_added)} seconds..."))
        else:
            return_to_company_selection()
    elif set(st.session_state.added_employees) == set(employees):
        st.session_state.all_employees_added_time = time.time()

def get_employees_for_team():
    company = st.session_state.selected_company
    team = st.session_state.selected_team
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    df = pd.read_csv(file_path)
    employees = df[(df['Firma'] == company) & (df['Team'] == team)]['Mitarbeiter'].tolist()
    return employees

# Add other shared functions as needed
