def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
# Callback function für die Auswahl eines Mitarbeiters

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