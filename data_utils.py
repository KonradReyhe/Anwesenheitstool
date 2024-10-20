# data_utils.py
import pandas as pd
import streamlit as st
import os
from utils import get_text

def get_companies():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        companies = sorted(df['Firma'].unique().tolist())
        return companies
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return []

def get_teams_for_company(company):
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        teams = df[df["Firma"] == company]["Team"].unique().tolist()
        return sorted(teams)
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return []

def get_employees_for_team(company, team):
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    if not os.path.exists(file_path):
        st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                           f"The file '{file_path}' was not found. Please check the path and filename."))
        return None
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        employees = df[(df["Firma"] == company) & 
                       (df["Team"] == team)]["Mitarbeiter"].tolist()
        if len(employees) == 0:
            st.warning(get_text("Keine Mitarbeiter*innen für das ausgewählte Team gefunden.",
                                "No employees found for the selected team."))
            return None
        return employees
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return None

def get_employees_for_current_team():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    df = pd.read_csv(file_path)
    df.columns = ['Firma', 'Team', 'Mitarbeiter']
    employees = df[(df["Firma"] == st.session_state.selected_company) & 
                   (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
    return employees

def get_all_employees():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        all_employees = df['Mitarbeiter'].unique().tolist()
        return sorted(all_employees)
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return []
