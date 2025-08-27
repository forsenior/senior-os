import datetime
import os
import smtplib
import ssl
import sys
from email.mime.text import MIMEText

current_dir = os.path.dirname(os.path.abspath(__file__))
sconf_src_path = os.path.abspath(os.path.join(current_dir, '../../../../sconf/src'))
sys.path.append(sconf_src_path)

import sconf.configuration.configuration_provider as dataProvider

CONFIG_FILE_NAME = 'config.json'
config_folder = os.path.abspath(os.path.join(current_dir, '../../../../sconf'))
_dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)


def send_email(recipient, content):
    smail_config = _dataProvider.get_smail_configuration()
    login = smail_config.seniorEmail
    password = smail_config.seniorPassword
    smtp_server = smail_config.smtpServer
    smtp_port = smail_config.smtpPort

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