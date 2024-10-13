import datetime
import json
import logging
import os
import smtplib
import ssl
import sys
from email.mime.text import MIMEText

logger = logging.getLogger(__file__)
def config(path):

    try:
        with open(path, "r") as f:
            data = json.load(f)
        credentials = data["credentials"]

        return (credentials["username"], credentials["password"],
                credentials["smtp_server"], credentials["smtp_port"])
    except Exception as e:
        logger.error("Couldn't load credentials from configuration file. " + e)
        return -1



def send_email(recipient, content):

    login, password, smtp_server, smtp_port = config(os.path.join(os.getcwd().split("smail")[0],
                                       "sconf/SMAIL_config.json"))

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = MIMEText(content)
    msg['Subject'] = f"Report, date: {date}"
    msg['From'] = login
    msg['To'] = recipient

    try:
        # establishing SMTP connection to the SMTP server
        with smtplib.SMTP(
                smtp_server, smtp_port
        ) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())
            print("Email send succesfuly.")

    except Exception as e:
        logger.error("Error occurred when trying to send email. " + e)
        print("Error occurred when trying to send email.")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python command_line_mail.py <recipient_email> <email_content>")
        sys.exit(1)

    recipient_email = sys.argv[1]
    email_content = sys.argv[2]

    send_email(recipient_email, email_content)