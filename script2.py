import subprocess
import smtplib
import os
from email.mime.text import MIMEText

# Dane SSH
SSH_HOST = "10.97.190.5"
SSH_USER = "devops"
#SSH_KEY_PATH = "/etc/ssh/twojego/klucza/ssh"

# Progi użycia zasobów
CPU_THRESHOLD = 50.0  # Procent
RAM_THRESHOLD = 50.0  # Procent
DISK_THRESHOLD = 50.0  # Procent

# Dane SMTP
EMAIL_SENDER = 'przemyslaw.kapelinski@gmail.com'
EMAIL_RECEIVER = 'kapel21@o2.pl'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_LOGIN = 'przemyslaw.kapelinski'
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD')

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
    # Komendy do wykonania na zdalnym serwerze
    commands = [
        "top -bn1 | grep load | awk '{printf \"%.2f\\n\", $(NF-2)}'",  # CPU
        "free -m | awk 'NR==2{printf \"%s/%sMB (%.2f%%)\\n\", $3,$2,$3*100/$2 }'",  # RAM
        "df -h | awk '$NF==\"/\"{printf \"%d%%\\n\", $5}'"  # Dysk
    ]

    metrics = {
        "cpu": None,
        "ram": None,
        "disk": None
    }

    for key, cmd in zip(metrics.keys(), commands):
        result = subprocess.run(
            ["ssh", f"{SSH_USER}@{SSH_HOST}", cmd],
            capture_output=True, text=True
        )
        metrics[key] = result.stdout.strip()

    alerts = []
    if float(metrics["cpu"]) > CPU_THRESHOLD:
        alerts.append(f"CPU usage is high: {metrics['cpu']}%")
    if float(metrics["ram"].split('(')[-1].replace('%)', '')) > RAM_THRESHOLD:
        alerts.append(f"RAM usage is high: {metrics['ram']}")
    if int(metrics["disk"].replace('%', '')) > DISK_THRESHOLD:
        alerts.append(f"Disk usage is high: {metrics['disk']}")

    return alerts

def main():
    alerts = check_metrics()
    if alerts:
        body = '\n'.join(alerts)
        send_email("Server Resource Alert", body)

if __name__ == "__main__":
    main()

