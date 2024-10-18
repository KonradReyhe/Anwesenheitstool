from auth import start_get_together

def home():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether konfigurieren:', 'Configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    # PIN setting
    col1, col2 = st.columns(2)
    with col1:
        pin1 = st.text_input(get_text("Setzen Sie einen PIN:", "Set a PIN:"), type="password", key="pin1")
    with col2:
        pin2 = st.text_input(get_text("Bestätigen Sie den PIN:", "Confirm the PIN:"), type="password", key="pin2")
    
    # Event name
    custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
    
    # File selection (allowing selection of other CSV files in the same directory)
    st.markdown(f"<div class='sub-header'>{get_text('Stammdaten-Datei:', 'Master Data File:')}</div>", unsafe_allow_html=True)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List all CSV files in the current directory
    csv_files = [f for f in os.listdir(current_dir) if f.endswith('.csv')]
    
    if csv_files:
        selected_file = st.selectbox(
            get_text("Wählen Sie die Stammdaten-Datei:", "Select the master data file:"),
            options=csv_files,
            index=csv_files.index('Firmen_Teams_Mitarbeiter.csv') if 'Firmen_Teams_Mitarbeiter.csv' in csv_files else 0,
            key="file_selector"
        )
        st.session_state.selected_file = os.path.join(current_dir, selected_file)
    else:
        st.error(get_text("Keine CSV-Dateien im aktuellen Verzeichnis gefunden.", 
                          "No CSV files found in the current directory."))
        st.session_state.selected_file = None
    
    # Optional automatic end
    st.markdown(f"<div class='sub-header'>{get_text('Optionale Einstellungen:', 'Optional Settings:')}</div>", unsafe_allow_html=True)
    enable_auto_end = st.checkbox(get_text("Automatisches Ende aktivieren", "Enable automatic end"), value=False, key="enable_auto_end")
    
    if enable_auto_end:
        col1, col2 = st.columns(2)
        with col1:
            auto_end_hours = st.number_input(
                get_text("Stunden:", "Hours:"), 
                min_value=0, value=5, step=1, key="auto_end_hours_input"
            )
        with col2:
            auto_end_minutes = st.selectbox(
                get_text("Minuten:", "Minutes:"),
                options=[0, 15, 30, 45],
                index=0,
                key="auto_end_minutes_input"
            )
        
        now = datetime.now(local_tz)
        end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
        st.write(get_text(f"Geplantes Ende: {end_time.strftime('%d.%m.%Y %H:%M')}", 
                          f"Scheduled end: {end_time.strftime('%Y-%m-%d %H:%M')}"))
        
        accounting_email = st.text_input(
            get_text("E-Mail-Adresse für Buchhaltung:", "Email address for accounting:"), 
            value=st.session_state.accounting_email, key="accounting_email_input"
        )
    else:
        auto_end_hours = None
        auto_end_minutes = None
        accounting_email = None
    
    # Data protection PIN
    datenschutz_pin = st.text_input(
        get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), 
        type="password", key="datenschutz_pin_input"
    )
    
    # Signature requirement
    require_signature = st.checkbox(
        get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), 
        value=st.session_state.require_signature
    )
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Stammdaten aktualisieren", "Update Master Data")):
            st.session_state.page = 'update_master_data'
            st.rerun()
    
    with col2:
        if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
            if start_get_together(pin1, pin2, custom_event_name):
                st.session_state.auto_end_hours = auto_end_hours if enable_auto_end else None
                st.session_state.auto_end_minutes = auto_end_minutes if enable_auto_end else None
                st.session_state.accounting_email = accounting_email
                st.session_state.require_signature = require_signature
                if enable_auto_end and auto_end_hours is not None and auto_end_minutes is not None:
                    now = datetime.now(local_tz)
                    end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
                    schedule_event_end(end_time)
                if datenschutz_pin:
                    st.session_state.datenschutz_pin = datenschutz_pin
                    st.session_state.datenschutz_pin_active = True
                st.session_state.page = 'select_company'
                st.rerun()

initialize_session_state()
