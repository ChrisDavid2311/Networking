import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

GMAIL_USER = "chrisdavid.ssu.test@gmail.com"
GMAIL_PASS = getpass("Gmail App Password: ")
recipient_email = "chrisdavid.ssu.test@gmail.com"

subject = "Hello World!"
body = "This is a test message saying Hello, World!"

msg = MIMEMultipart()
msg["From"] = GMAIL_USER
msg["To"] = recipient_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtpserver:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(GMAIL_USER, GMAIL_PASS)
        smtpserver.sendmail(GMAIL_USER, recipient_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
