import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.application import MIMEApplication
import smtplib
import streamlit as st

def send_email(recipient, subject, body, attachment_path=None, get_text_func=None):
    if get_text_func is None:
        get_text_func = lambda x, y: x  # Default to returning the first argument if no function is provided
    
    message = MIMEMultipart()
    message["From"] = st.session_state.sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read())
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            message.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(st.session_state.sender_email, st.session_state.sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def send_documents_to_accounting(zip_file_path, get_text_func=None):
    if get_text_func is None:
        get_text_func = lambda x, y: x  # Default to returning the first argument if no function is provided
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    accounting_email = st.session_state.accounting_email

    subject = get_text_func("GetTogether Anwesenheitsliste", "GetTogether Attendance List")
    body = get_text_func("Anbei finden Sie die Anwesenheitsliste des GetTogether-Events.",
                        "Please find attached the attendance list for the GetTogether event.")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = accounting_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with open(zip_file_path, "rb") as attachment:
        part = MIMEApplication(attachment.read())
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
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False
