# data_utils.py

"""
This module provides utility functions for data manipulation and retrieval
in the GetTogether application.
"""

import pandas as pd
import streamlit as st
from text_utils import get_text

@st.cache_data(ttl=3600)  
def load_master_data():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    df = pd.read_csv(file_path)
    df.columns = ['Firma', 'Team', 'Mitarbeiter']
    return df

def get_companies():
    """
    Retrieve the list of companies from the data source.

    Returns:
        list: A list of company names.
    """
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
    """
    Retrieve the list of teams for a given company.

    Args:
        company (str): The name of the company.

    Returns:
        list: A list of team names for the specified company.
    """
    df = load_master_data()
    teams = df[df["Firma"] == company]["Team"].unique().tolist()
    return sorted(teams)

def get_employees_for_team(company, team):
    """
    Retrieve the list of employees for a given company and team.

    Args:
        company (str): The name of the company.
        team (str): The name of the team.

    Returns:
        list: A list of employee names for the specified company and team.
    """
    df = load_master_data()
    employees = df[(df["Firma"] == company) & 
                   (df["Team"] == team)]["Mitarbeiter"].tolist()
    return employees

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
