# email_utils.py
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import streamlit as st
from text_utils import get_text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_documents_to_accounting(zip_file_path):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    accounting_email = st.session_state.accounting_email

    subject = get_text("GetTogether Anwesenheitsliste", "GetTogether Attendance List")
    body = get_text("Anbei finden Sie die Anwesenheitsliste des GetTogether-Events.",
                    "Please find attached the attendance list for the GetTogether event.")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = accounting_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with open(zip_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(zip_file_path)}",
    )
    message.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        logger.info(f"Email sent successfully to {accounting_email}")
        return True
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        st.error(f"Failed to send email: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        st.error(f"An unexpected error occurred while sending email: {e}")
    return False
