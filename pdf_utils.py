#pdf_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import base64

def generate_pdf(data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "GetTogether Attendance Report")
    c.setFont("Helvetica", 12)

    y = height - 80
    for record in data:
        if y < 50:  # Start a new page if we're near the bottom
            c.showPage()
            y = height - 50

        c.drawString(50, y, f"Name: {record['Name']}")
        y -= 20
        c.drawString(50, y, f"Company: {record['Firma']}")
        y -= 20
        c.drawString(50, y, f"Team: {record['Team']}")
        y -= 20
        c.drawString(50, y, f"Time: {record['Zeit']}")
        y -= 20

        if 'Signature' in record and record['Signature']:
            try:
                signature_data = base64.b64decode(record['Signature'])
                signature_image = Image.open(io.BytesIO(signature_data))
                signature_image = signature_image.convert('RGB')
                
                # Resize the signature if it's too large
                max_width = 200
                max_height = 100
                signature_image.thumbnail((max_width, max_height))
                
                signature_io = io.BytesIO()
                signature_image.save(signature_io, format='PNG')
                signature_io.seek(0)
                
                img = ImageReader(signature_io)
                c.drawImage(img, 50, y - 60, width=200, height=60, preserveAspectRatio=True)
            except Exception as e:
                print(f"Error processing signature: {e}")
                c.drawString(50, y, "Signature: Error processing signature")
        
        y -= 80  # Extra space after each record

    c.save()
    return output_path
