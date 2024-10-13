from datetime import datetime
import logging
import imaplib
import smtplib
from email.mime.text import MIMEText
import email
import ssl
import re

import chardet
from smail.style import get_guardian_email, resend_active, load_credentials, get_path

logger = logging.getLogger(__file__)

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

            # If the email is sent to email address from which a phishing email was received,
            # it is resent to guardian.
            if recipient in phish_senders:
                resend_reply(recipient,content,server, login)

        logger.info(f"An email has been sent to {recipient}.")
        # Returning 1 if email was send successfully
        return 1

    except smtplib.SMTPAuthenticationError:
        logger.error("Authentication error. Check your email and password.",
                     exc_info=True)
        return -1
    except smtplib.SMTPConnectError:
        logger.error("SMTP connection error. Check your SMTP server and port.",
                     exc_info=True)
        return 0
    except Exception:
        logger.error("Error occurred when trying to send email. ",
                     exc_info=True)
        return -2


def resend_reply(recipient, content, server, login):

    content = f"Senior send reply email to phishing email ({recipient}) with content:\n" + content
    msg = MIMEText(content)
    msg['Subject'] = f"Reply to phish email by {login}"
    msg['From'] = login
    server.sendmail(login, get_guardian_email(), msg.as_string())
    logger.warning(f"An email has been sent to {recipient}! Resending email to guardian: {get_guardian_email()}!")


def imap_connection(login, password, imap_server, imap_port):
    try:
        # Establishing a connection to an IMAP server
        mail = imaplib.IMAP4_SSL(
            imap_server, imap_port, ssl_context=ssl.create_default_context()
        )
        mail.login(login, password)
        logger.info("Successful connection to IMAP server.")
        return mail

    except imaplib.IMAP4.error:
        logger.error("IMAP Error: Failed to connect to the IMAP server.", exc_info=True)
        return 0
    except ConnectionError:
        logger.error("Connection Error: Failed to establish a connection"
                     " to the IMAP server.", exc_info=True)
        return -1
    except Exception as error:
        logger.error("An unexpected error occurred. ", exc_info=True)
        return -2

    return None

def read_mail(login, password, imap_server, imap_port, language, text):

    global resend_emails_g
    lang_subject = text[f"smail_{language}_subjectLabel"]
    lang_from = text[f"smail_{language}_from"]
    lang_date = text[f"smail_{language}_date"]
    lang_message = text[f"smail_{language}_messageLabel"]

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
                                     f"{lang_message}\n\n{message_decode}")


                    # Appends the email into emails list
                    emails.append(email_content)
                    subjects.append(decoded_subject)
                    break

        # If the emails were sent to a guardian, the value is changed to True
        # to ensure that they are only sent once.
        if not resend_emails_g:
            resend_mail_to_guardian(emails)
            resend_emails_g = True

        logger.info(f"{len(emails)} emails successfully loaded")
        return emails, subjects

    except Exception as error:
        logger.error("An unexpected error occured. ", exc_info=True)
    finally:
        mail.close()
        mail.logout()

def resend_mail_to_guardian(emails):

    active, smail, gmail = resend_active()
    if active:
        date = datetime.now().strftime("%d.%m.%Y")
        email_subject = f"Email report from {smail}, date: {date}"
        email_content = ""
        logger.info(f"Sending emails from seniors address {smail} to guardians email address {gmail}.")
        for e in emails:
            email_content += e

        (login, password, smtp_server,
         smtp_port, imap_server, imap_port) = (
            load_credentials(get_path("sconf", "SMAIL_config.json")))

        send_email(gmail, email_subject, email_content, login, password, smtp_server, smtp_port)


def check_content_of_email(content, sender, subject):

    with open(get_path("sconf/phish", "SMAIL_PHISH_1.txt")) as f:
        phish_urls = f.readlines()
    f.close()

    # Strip newline characters and convert to lowercase
    phish_urls = [url.strip().lower() for url in phish_urls]

    url_pattern = r"https?://(?:www\.)?\S+|www\.\S+"

    # Extract urls from email body and subject
    content_urls = re.findall(url_pattern, content)
    subject_urls = re.findall(url_pattern, subject)
    urls = content_urls + subject_urls

    found_phishing_url = False

    for url in urls:
        # Remove newline and convert to lowercase
        clean_url = url.strip().lower()
        for p in phish_urls:
            if clean_url.startswith(p):
                found_phishing_url = True
                phish_senders.append(sender)
                break

    if found_phishing_url:
        logger.warning(f"Found a phishing URL from {sender}")
        return False
    else:
        logger.info(f"Found URL from {sender}")
        return True

def check_email_for_spam(email_messages):

    global index
    safe_emails = []
    phish_emails = []

    # Getting email address
    for email_content in email_messages:
        email_parts = email_content.split("\n")

        # Extract relevant information
        sender = email_parts[1].replace("From: ", "")
        message = "".join([s.strip("\r") for s in email_parts[4:]])

        # Modify sender address
        if '<' in sender and '>' in sender:
            start_index = sender.find('<')
            end_index = sender.find('>')
            if start_index < end_index:
                modified_sender = sender[start_index + 1:end_index]
        else:
            modified_sender = sender

        contentBlock = check_content_of_email(message, modified_sender, email_parts[0])

        if contentBlock:
            safe_emails.append((email_content, index, "safe"))
            index = index + 1
        else:
            phish_emails.append((email_content, index, "phish"))
            index = index + 1

    return safe_emails, phish_emails

