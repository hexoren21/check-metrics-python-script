import psutil
import smtplib
from email.mime.text import MIMEText

# Konfiguracja
CPU_THRESHOLD = 50.0  # Procent
RAM_THRESHOLD = 50.0  # Procent
DISK_THRESHOLD = 50.0  # Procent
EMAIL_SENDER = 'przemyslaw.kapelinski@gmail.com'
EMAIL_RECEIVER = 'kapel21@o2.pl'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_LOGIN = 'przemyslaw.kapelinski'
SMTP_PASSWORD = ''

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

def check_metrics():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    alerts = []
    if cpu_usage > CPU_THRESHOLD:
        alerts.append(f"CPU usage is high: {cpu_usage}%")
    if ram_usage > RAM_THRESHOLD:
        alerts.append(f"RAM usage is high: {ram_usage}%")
    if disk_usage > DISK_THRESHOLD:
        alerts.append(f"Disk usage is high: {disk_usage}%")

    return alerts

def main():
    alerts = check_metrics()
    if alerts:
        body = '\n'.join(alerts)
        send_email("Server Resource Alert", body)

if __name__ == "__main__":
    main()

