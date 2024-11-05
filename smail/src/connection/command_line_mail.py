import datetime
import json
import os
import smtplib
import ssl
import sys
from email.mime.text import MIMEText


def config(path):

    try:
        with open(path, "r") as f:
            data = json.load(f)
        credentials = data["smailConfiguration"]

        return (credentials["seniorEmail"], credentials["seniorPassword"],
                credentials["smtpServer"], credentials["smtpPort"])
    except Exception as e:
        print(f"Couldn't load credentials from configuration file: {e}")
        return -1



def send_email(recipient, content):
    config_path = os.path.abspath(os.path.join(os.getcwd().split("smail")[0], "sconf/config.json"))
    login, password, smtp_server, smtp_port = config(config_path)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = MIMEText(content)
    msg['Subject'] = f"Report, date: {date}"
    msg['From'] = login
    msg['To'] = recipient

    try:
        # establishing SMTP connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())
            print("Email send succesfuly.")

    except Exception as e:
        print(f"Error occurred when trying to send email: {e}")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""Usage: python command_line_mail.py <recipient_email> "<email_content>" """)
        sys.exit(1)

    recipient_email = sys.argv[1]
    email_content = sys.argv[2]

    send_email(recipient_email, email_content)