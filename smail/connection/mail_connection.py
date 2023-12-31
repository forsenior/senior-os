import logging
import imaplib
import smtplib
from email.mime.text import MIMEText
import email
import ssl
import re
import chardet
from smail.connection.style import load_json_file, get_language

logger = logging.getLogger(__file__)

# config to the smtp/imap server and other information are taken from
# SMAIL_config.json file, in order to be able to connect to the gmail mailbox,
# it is necessary to enter the email address and password for the application
# (password needs to be generated in google account via:
#   google account -> security -> 2-step verification -> app passwords)

data = load_json_file("../sconf/SMAIL_config.json")
credentials = data["credentials"]
login = credentials["username"]
password = credentials["password"]
smtp_server = credentials["smtp_server"]
smtp_port = credentials["smtp_port"]
imap_server = credentials["imap_server"]
imap_port = credentials["imap_port"]
max_emails = credentials["max"]
sslContext = ssl.create_default_context()


def send_email(recipient, subject, content):

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = recipient

    try:
        # establishing SMTP connection to the SMTP server
        with smtplib.SMTP_SSL(
                smtp_server, smtp_port, context=sslContext
        ) as server:
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())
        logger.warning(f"An email has been sent to {recipient}")
        # returning 1 if email was send successfully
        return 1

    except smtplib.SMTPAuthenticationError:
        logger.error("Authentication error. Check your email and password.",
                     exc_info=True)
        return 0
    except smtplib.SMTPConnectError:
        logger.error("SMTP connection error. Check your SMTP server and port.",
                     exc_info=True)
        return 0
    except Exception:
        logger.error("Error occurred when trying to send email. ",
                     exc_info=True)
        return 0


def read_mail():

    language, text = get_language()
    lang_subject = text[f"smail_{language}_subjectLabel"]
    lang_from = text[f"smail_{language}_from"]
    lang_date = text[f"smail_{language}_date"]
    lang_message = text[f"smail_{language}_messageLabel"]

    try:
        # establishing a connection to an IMAP server
        mail = imaplib.IMAP4_SSL(
            imap_server, imap_port, ssl_context=sslContext
        )

        mail.login(login, password)
        logger.info("Successful connection to IMAP server.")

        # selecting folder from which to read e-mails
        mail.select("INBOX")

        # searches for all emails in INBOX
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

            # decoding subject
            subject = email_message.get('subject', '')
            decoded_subject = email.header.decode_header(subject)[0][0]

            try:
                if isinstance(decoded_subject, bytes):
                    decoded_subject = decoded_subject.decode('utf-8')
            except:
                decoded_subject = decoded_subject.decode("iso-8859-2")

            for part in email_message.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    # get charset from the email part
                    charset = part.get_content_charset()
                    # Decodes the payload of the email part.
                    message = part.get_payload(decode=True)

                    if charset:
                        message_decode = message.decode(charset)
                    else:
                        # use chardet
                        detect_charset = chardet.detect(message)
                        char = detect_charset["encoding"]
                        if char:
                            message_decode = message.decode(char)
                        else:
                            # if charset detection fails, use latin-1
                            message_decode = message.decode("latin-1")

                    # construct an email content string
                    email_content = (f"{lang_subject}{decoded_subject}\n"
                                     f"{lang_from}{sender}\n"
                                     f"{lang_date}{date}\n"
                                     f"{lang_message}\n\n{message_decode}")
                    # appends the email into emails list
                    emails.append(email_content)
                    subjects.append(decoded_subject)
                    break

        logger.info(f"{len(emails)} emails successfully loaded")
        return emails, subjects

    except imaplib.IMAP4.error:
        logger.error("IMAP Error: Failed to connect to the IMAP server.", exc_info=True)
    except ConnectionError:
        logger.error("Connection Error: Failed to establish a connection"
                     " to the IMAP server.", exc_info=True)
    except Exception as error:
        logger.error("An unexpected error occurred. ", exc_info=True)
    finally:
        mail.close()
        mail.logout()


def check_content_of_email(content, sender):

    with open("../sconf/phish/SMAIL_PHISH_1.txt") as f:
        phish_urls = f.readlines()
    f.close()

    # Strip newline characters and convert to lowercase
    phish_urls = [url.strip().lower() for url in phish_urls]

    url_pattern = r"https?://(?:www\.)?\S+|www\.\S+"
    urls = re.findall(url_pattern, content)

    found_phishing_url = False

    for url in urls:
        # Remove newline and convert to lowercase
        clean_url = url.strip().lower()
        if clean_url in phish_urls:
            logger.warning(f"Found a phishing URL from {sender}, url: {url}")
            found_phishing_url = True
            break
        else:
            logger.info(f"Found URL from {sender}, url: {url}")

    if found_phishing_url:
        return False
    else:
        return True

def check_email_for_spam(email_messages):

    safe_emails = []
    phish_emails = []

    # getting email address
    for email_content in email_messages:
        email_parts = email_content.split("\n")

        # Extract relevant information
        sender = email_parts[1].replace("From: ", "")
        message = "".join([s.strip("\r") for s in email_parts[4:]])

        # modify sender address
        if '<' in sender and '>' in sender:
            start_index = sender.find('<')
            end_index = sender.find('>')
            if start_index < end_index:
                modified_sender = sender[start_index + 1:end_index]
        else:
            modified_sender = sender

        contentBlock = check_content_of_email(message, modified_sender)

        if contentBlock:
            safe_emails.append(email_content)
        else:
            phish_emails.append(email_content)


    return safe_emails, phish_emails
