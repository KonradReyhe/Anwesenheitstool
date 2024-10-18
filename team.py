import streamlit as st
from utils import get_text
from ui_components import display_header, display_company_team_info
from attendance import get_teams_for_company
from navigation import display_back_button
from streamlit import experimental_rerun

def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
    st.session_state.added_employees = []
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.success_messages = []
    st.session_state.last_message_time = None
    st.session_state.all_employees_added_time = None
    experimental_rerun()

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

def select_employee():
    if not check_datenschutz_pin():
        return

    display_header()
    display_company_team_info()
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        employees = get_employees_for_team()
        if not employees:
            return

        st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter*innen auswählen:', 'Select employees:')}</div>", unsafe_allow_html=True)
        
        initialize_employee_session_state()
        check_company_team_change()

        display_employee_buttons(employees)
        
        handle_signature_modal()
        display_success_messages()
        handle_undo_last_selection()
        check_all_employees_added(employees)
        
        # Automatically refresh the app every second to update the countdown and messages
        st_autorefresh(interval=1000, key="autorefresh")
        
        display_back_button()

    st.session_state.last_activity_time = time.time()


def get_employees_for_team():
    file_path = "Firmen_Teams_Mitarbeiter.csv"
    if not os.path.exists(file_path):
        st.error(get_text(f"Die Datei '{file_path}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad und den Dateinamen.",
                           f"The file '{file_path}' was not found. Please check the path and filename."))
        return None
    try:
        df = pd.read_csv(file_path)
        df.columns = ['Firma', 'Team', 'Mitarbeiter']
        employees = df[(df["Firma"] == st.session_state.selected_company) & 
                       (df["Team"] == st.session_state.selected_team)]["Mitarbeiter"].tolist()
        if len(employees) == 0:
            st.warning(get_text("Keine Mitarbeiter*innen für das ausgewählte Team gefunden.",
                                "No employees found for the selected team."))
            return None
        return employees
    except Exception as e:
        st.error(get_text(f"Fehler beim Lesen der CSV-Datei: {e}",
                          f"Error reading the CSV file: {e}"))
        return None

def initialize_employee_session_state():
    if 'added_employees' not in st.session_state:
        st.session_state.added_employees = []
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'current_company_team' not in st.session_state:
        st.session_state.current_company_team = None
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None

def check_company_team_change():
    current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
    if st.session_state.current_company_team != current_company_team:
        st.session_state.added_employees = []
        st.session_state.current_company_team = current_company_team
        st.session_state.timer_active = False
        st.session_state.countdown_start_time = None
        st.session_state.success_messages = []
        st.session_state.last_message_time = None
        st.session_state.all_employees_added_time = No
