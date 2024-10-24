# config.py

"""
This module contains configuration settings for the GetTogether application.
It defines constants and settings used throughout the application.
"""

# Version number of the application
VERSION = "1.0.0"

# Timeout duration for inactivity (in seconds)
INACTIVITY_TIMEOUT = 300  # 5 minutes

# Email configuration
SMTP_SERVER = "your_smtp_server"
SMTP_PORT = 587
SENDER_EMAIL = "sender@example.com"
SENDER_PASSWORD = "your_email_password"
ACCOUNTING_EMAIL = "accounting@example.com"

EMAIL_SENDING_ENABLED = False  



