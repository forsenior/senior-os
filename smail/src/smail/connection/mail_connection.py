from datetime import datetime
import imaplib
import smtplib
from email.mime.text import MIMEText
import email
import ssl
import re

import chardet



# Config of the smtp/imap server and other information are taken from
# SMAIL_config.json file, in order to be able to connect to the gmail mailbox,
# it is necessary to enter the email address and password for the application
# (password needs to be generated in google account via:
#   google account -> security -> 2-step verification -> app passwords)

phish_senders = []
resend_emails_g = False
index = 0

def send_email(recipient, subject, content, login, password, smtp_server, smtp_port):

    sslContext = ssl.create_default_context()
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = recipient

    try:
        # Establishing SMTP connection to the SMTP server
        with smtplib.SMTP(
                smtp_server, smtp_port
        ) as server:
            server.starttls(context=sslContext)
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())

        print(f"An email has been sent to {recipient}.")
        # Returning 1 if email was send successfully
        return 1
    except smtplib.SMTPAuthenticationError:
        print("Authentication error. Check your email and password.")
        return -1
    except smtplib.SMTPConnectError:
        print("SMTP connection error. Check your SMTP server and port.")
        return 0
    except Exception as e:
        print(f"Error occurred when trying to send email: {e}")
        return -2


def send_email_with_guardian_copy(recipient, subject, content, login, password, smtp_server, smtp_port, bcc):

    sslContext = ssl.create_default_context()
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = recipient

    to_addresses = [recipient]
    if bcc:
        to_addresses.append(bcc)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=sslContext)
            server.login(login, password)
            server.sendmail(login, to_addresses, msg.as_string())

        print(f"An email has been sent to {recipient}.")
        # Returning 1 if email was send successfully
        return 1
    except smtplib.SMTPAuthenticationError:
        print("Authentication error. Check your email and password.")
        return -1
    except smtplib.SMTPConnectError:
        print("SMTP connection error. Check your SMTP server and port.")
        return 0
    except Exception as e:
        print(f"Error occurred when trying to send email: {e}")
        return -2


def imap_connection(login, password, imap_server, imap_port):
    try:
        # Establishing a connection to an IMAP server
        mail = imaplib.IMAP4_SSL(
            imap_server, imap_port, ssl_context=ssl.create_default_context()
        )
        mail.login(login, password)
        print("Successful connection to IMAP server.")
        return mail

    except imaplib.IMAP4.error:
        print("IMAP Error: Failed to connect to the IMAP server.")
        return 0
    except ConnectionError:
        print("Connection Error: Failed to establish a connection to the IMAP server.")
        return -1
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        return -2

def read_mail(login, password, imap_server, imap_port, language, text, data_provider):
    global resend_emails_g
    lang_subject = getattr(text, f"smail{language.capitalize()}SubjectLabel", None)
    lang_from = getattr(text, f"smail{language.capitalize()}From", None)
    lang_date = getattr(text, f"smail{language.capitalize()}Date", None)
    lang_message = getattr(text, f"smail{language.capitalize()}MessageLabel", None)

    if None in [lang_subject, lang_from, lang_date, lang_message]:
        print("Error: Missing language keys")
        return None

    mail = imap_connection(login, password, imap_server, imap_port)

    try:
        # Selecting folder from which to read e-mails
        mail.select("INBOX")

        # Searches for all emails in INBOX
        # _, discards the first return value from mail.search
        _, selected_mails = mail.search(None, 'ALL')
        email_ids = selected_mails[0].split()

        emails = []
        subjects = []

        for email_id in email_ids:
            _, data = mail.fetch(email_id, '(RFC822)')
            _, bytes_data = data[0]

            email_message = email.message_from_bytes(bytes_data)

            sender = email_message['from']
            date = email_message['date']

            # Decoding subject
            subject = email_message.get('subject', '')
            decoded_subject = email.header.decode_header(subject)[0][0]

            try:
                if isinstance(decoded_subject, bytes):
                    decoded_subject = decoded_subject.decode('utf-8')
            except:
                decoded_subject = decoded_subject.decode("iso-8859-2")

            for part in email_message.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    # Get charset from the email part
                    charset = part.get_content_charset()
                    # Decodes the payload of the email part.
                    message = part.get_payload(decode=True)

                    if charset:
                        message_decode = message.decode(charset)
                    else:
                        # Use chardet
                        detect_charset = chardet.detect(message)
                        char = detect_charset["encoding"]
                        if char:
                            message_decode = message.decode(char)
                        else:
                            # If charset detection fails, use latin-1
                            message_decode = message.decode("latin-1")

                    # Construct an email content string
                    email_content = (f"{lang_subject}{decoded_subject}\n"
                                     f"{lang_from}{sender}\n"
                                     f"{lang_date}{date}\n"
                                     f"{lang_message}\n{message_decode}")


                    # Appends the email into emails list
                    emails.append(email_content)
                    subjects.append(decoded_subject)
                    break

        # If the emails were sent to a guardian, the value is changed to True
        # to ensure that they are only sent once.
        if not resend_emails_g:
            # resend_mail_to_guardian(emails, data_provider)
            resend_emails_g = True

        print(f"{len(emails)} emails successfully loaded")
        return emails, subjects

    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    finally:
        mail.close()
        mail.logout()

# def resend_mail_to_guardian(emails, data_provider):
#     from smail.src.smail.style import resend_active, load_credentials, get_path
#     active, smail, gmail = resend_active(data_provider)
#     if active:
#         date = datetime.now().strftime("%d.%m.%Y")
#         email_subject = f"Email report from {smail}, date: {date}"
#         email_content = ""
#         print(f"Sending emails from senior's address {smail} to guardian's email address {gmail}.")
#         for e in emails:
#             email_content += e
#
#         (login, password, smtp_server,
#          smtp_port, imap_server, imap_port) = (
#             load_credentials(data_provider))
#
#         send_email(gmail, email_subject, email_content, login, password, smtp_server, smtp_port)






