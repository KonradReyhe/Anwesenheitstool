import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
from datetime import datetime, timedelta
import pytz
from auth import start_get_together, check_datenschutz_pin, datenschutz_pin_page
from shared_functions import (
    get_employees_for_company_team, get_companies, 
    get_teams_for_company, check_company_team_change, check_all_employees_added, 
    get_employees_for_team, save_attendance, undo_last_employee_selection
)
from attendance import add_employee_to_attendance
from ui_components import (
    display_company_team_info, display_employee_buttons,
    handle_signature_modal, display_success_messages, handle_undo_last_selection,
    admin_panel, display_header, signature_modal
)
from utils import (
    get_text, end_get_together, auto_save_attendance, check_event_end,
    create_zip_file, generate_pdf, send_email, schedule_event_end, add_success_message,
    update_last_activity, trigger_rerun
)
from session_state import initialize_session_state, initialize_employee_session_state
from config import INACTIVITY_TIMEOUT
from styles import apply_custom_styles, VERSION
from timer import start_timer, check_timer, display_back_button
from navigation import return_to_company_selection, go_back_to_team_from_employee
from admin import admin_settings, confirm_end_get_together, update_master_data
from employee import select_employee, select_employee_callback, get_all_employees
from language_utils import toggle_language
from home import home
from company import select_company, select_company_callback
from team import select_team, select_team_callback

local_tz = pytz.timezone('Europe/Berlin')

def main():
    initialize_session_state()
    apply_custom_styles()
    st_autorefresh(interval=1000, key="autorefresh")
    check_event_end()
    navigate()

if __name__ == "__main__":
    main()

