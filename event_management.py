# event_management.py
import streamlit as st
from datetime import datetime
import os
import pandas as pd
from utils import get_text, create_zip_file, generate_pdf

def end_get_together():
    zip_file_name = save_attendance()
    if zip_file_name:
        send_documents_to_accounting(zip_file_name)
        os.remove(zip_file_name)  # Clean up after sending
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.success(get_text("GetTogether wurde beendet.", "GetTogether has been ended."))
    st.experimental_rerun()

def save_attendance():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        df.to_csv(file_name, index=False)
        
        pdf_file_name = f"Anwesenheit_{timestamp}.pdf"
        generate_pdf(st.session_state.attendance_data, pdf_file_name)
        
        zip_file_name = f"Anwesenheit_{timestamp}.zip"
        create_zip_file([file_name, pdf_file_name], zip_file_name)
        
        with open(zip_file_name, "rb") as file:
            btn = st.download_button(
                label="Download Anwesenheitsliste",
                data=file,
                file_name=zip_file_name,
                mime="application/zip"
            )
        
        os.remove(file_name)
        os.remove(pdf_file_name)
        
        return zip_file_name
    return False

def send_documents_to_accounting(zip_file_name):
    # Implement the logic to send documents to accounting
    # This could involve sending an email with the zip file attached
    # or uploading the file to a specific location
    
    # For now, we'll just print a message
    st.info(get_text(
        f"Dokumente ({zip_file_name}) wurden an die Buchhaltung gesendet.",
        f"Documents ({zip_file_name}) have been sent to accounting."
    ))
    
    # In a real implementation, you might want to use something like:
    # send_email(to="accounting@company.com", subject="GetTogether Attendance", attachment=zip_file_name)
    # or
    # upload_to_server(zip_file_name, destination="/accounting/gettogether/")
