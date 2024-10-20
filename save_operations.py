import streamlit as st
import pandas as pd
from datetime import datetime
import os
from pdf_utils import generate_pdf
import zipfile

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
        os.remove(zip_file_name)
        
        return zip_file_name
    return False

def create_zip_file(files, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))
