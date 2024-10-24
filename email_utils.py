# email_utils.py

"""
This module handles email-related functionality for the GetTogether application.
It includes functions for sending emails with attachments.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, ACCOUNTING_EMAIL

def send_documents_to_accounting(zip_file_path):
    """
    Send the attendance documents to the accounting email.

    Args:
        zip_file_path (str): The path to the ZIP file containing attendance documents.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Implementation details here
