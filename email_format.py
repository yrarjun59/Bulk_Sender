import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email_validator import validate_email, EmailNotValidError
import os

# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


MY_EMAIL = "your_email@gmail.com"  # Replace with your email
MY_PASSWORD = "your_password_here"  # Replace with your app-specific password or use env variables

# Email subject and body file
SUBJECT = "Subject Text" # Application for [Job Title] at [Company Name] 
BODY = "Cover Letter.txt"  # Replace with the path to your cover letter file within same folder

# Path to the attachment (CV)
ATTACH_CV_PATH = "CV_SAMPLE.pdf"  # Replace with the name of your CV file within same folder or absolute location 

def is_valid_email(email):
    """Validate email address"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        print(f"Invalid email address: {email}. Skipping.")
        return False

def validate_files():
    """Check if required files exist"""
    if not os.path.exists(BODY):
        print(f"Error: Cover letter file '{BODY}' not found!")
        raise SystemExit("Cover letter file missing or misnamed, cannot proceed.")

    if not os.path.exists(ATTACH_CV_PATH):
        print(f"Error: CV file '{ATTACH_CV_PATH}' not found!")
        raise SystemExit("CV file missing, or misnamed cv file cannot proceed.")

def send_email(to_email, importance='1'):
    """Send an email with the specified importance"""
    # Validate email
    if not is_valid_email(to_email):
        return

    # Ensure necessary files are available
    validate_files()

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = to_email
    msg['Subject'] = SUBJECT
    msg['X-Priority'] = importance  # Set email priority

    # Attach the email body and the CV
    msg.attach(MIMEText(generate_body(), 'plain'))
    msg.attach(attach_file(ATTACH_CV_PATH))  # Attach CV

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, to_email, msg.as_string())
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")

def generate_body(file_path=BODY):
    """Generate email body from a text file"""
    try:
        with open(file_path, 'r') as body:
            return body.read()
    except FileNotFoundError:
        print(f"Body file not found at {file_path}. Using default message.")
        return "Hello,\n\nPlease find my application attached.\n\nBest regards."

def attach_file(file_path=ATTACH_CV_PATH):
    """Attach a file to the email"""
    try:
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={file_path}")
            return part
    except FileNotFoundError:
        print(f"Attachment file not found at {file_path}. Skipping attachment.")
        return MIMEBase('application', 'octet-stream')
