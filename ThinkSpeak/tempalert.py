import smtplib
import subprocess
import time
from email.mime.text import MIMEText
from getpass import getpass

GMAIL_USER = "chrisdavid.ssu.test@gmail.com"
RECIPIENT = "chrisdavid.ssu.test@gmail.com"
GMAIL_APP_PASSWORD = getpass("Gmail App Password: ")

THRESHOLD_C = 38.0
CHECK_EVERY_SECONDS = 30
alert_sent = False


def get_cpu_temperature():
    # Reads the Pi's SoC temperature, for example: temp=45.2'C
    result = subprocess.run(
        ["vcgencmd", "measure_temp"],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.split("=")[1].split("'")[0])


def send_alert(temperature):
    message = MIMEText(
        f"The Raspberry Pi CPU temperature is {temperature:.1f}°C, "
        f"above the {THRESHOLD_C:.1f}°C limit."
    )
    message["From"] = GMAIL_USER
    message["To"] = RECIPIENT
    message["Subject"] = "Raspberry Pi temperature alert"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(message)


while True:
    try:
        temperature = get_cpu_temperature()
        print(f"CPU temperature: {temperature:.1f}°C")

        if temperature > THRESHOLD_C and not alert_sent:
            send_alert(temperature)
            print("Temperature alert email sent.")
            alert_sent = True

        elif temperature <= THRESHOLD_C:
            alert_sent = False

    except Exception as error:
        print(f"Error: {error}")

    time.sleep(CHECK_EVERY_SECONDS)
