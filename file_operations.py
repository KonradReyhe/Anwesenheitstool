import zipfile
import io
import pandas as pd
from datetime import datetime
from pdf_utils import generate_pdf

def save_attendance(attendance_data, require_signature):
    if attendance_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_file_name = f"Anwesenheit_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
            # Add CSV file
            csv_data = pd.DataFrame(attendance_data)
            csv_buffer = io.StringIO()
            csv_data.to_csv(csv_buffer, index=False)
            zipf.writestr(f"Anwesenheit_{timestamp}.csv", csv_buffer.getvalue())
            
            # Add PDF file if signatures are required
            if require_signature:
                pdf_buffer = io.BytesIO()
                generate_pdf(attendance_data, pdf_buffer)
                zipf.writestr(f"Anwesenheit_{timestamp}.pdf", pdf_buffer.getvalue())
        
        return zip_file_name
    return None