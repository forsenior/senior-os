import datetime
import json
import logging
import os


def smail_config_default(path):
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'credentials': {
            "username": "xfiala59@gmail.com",
            "password": "pafotbpfrrlwvund",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_server": "imap.gmail.com",
            "imap_port": 993,
            "max": 20
        },
            "emails": {
            "Person1": "email01@gmail.com",
            "Person2": "email02@gmail.com",
            "Person3": "email03@gmail.com",
            "Person4": "email04@gmail.com",
            "Person5": "email05@gmail.com",
            "Person6": "email06@gmail.com"
        },
        "images": {
            "exit": "../sconf/images/SMAIL-exit-1.png",
            "Person1": "../sconf/images/SMAIL-person-1.png",
            "Person2": "../sconf/images/SMAIL-person-2.png",
            "Person3": "../sconf/images/SMAIL-person-3.png",
            "Person4": "../sconf/images/SMAIL-person-4.png",
            "Person5": "../sconf/images/SMAIL-person-5.png",
            "Person6": "../sconf/images/SMAIL-person-6.png"
        },
        "resend_email": 0,
        "show_url": 1,
        "guardian_email": "241124@vut.cz",
        "timer": 5000,
        "text": {
            "smail_en_sendToButton": "Send To",
            "smail_en_inboxLabel": "Inbox:",
            "smail_en_recipientLabel": "To: ",
            "smail_en_subjectLabel": "Subject: ",
            "smail_en_messageLabel": "Message: ",
            "smail_en_from": "From: ",
            "smail_en_date": "Date: ",
            "smail_en_email_sent": "Email has been sent.",
            "smail_cz_sendToButton": "Komu",
            "smail_cz_inboxLabel": "Doručené: ",
            "smail_cz_recipientLabel": "Příjemce: ",
            "smail_cz_subjectLabel": "Předmět: ",
            "smail_cz_messageLabel": "Zpráva: ",
            "smail_cz_from": "Informace: ",
            "smail_cz_date": "Datum: ",
            "smail_cz_email_sent": "E-mail byl úspěšně odeslán.",
            "smail_de_sendToButton": "Senden An",
            "smail_de_inboxLabel": "Posteingang: ",
            "smail_de_recipientLabel": "An: ",
            "smail_de_subjectLabel": "Betreff: ",
            "smail_de_messageLabel": "Nachricht: ",
            "smail_de_from": "Von: ",
            "smail_de_date": "Datum: ",
            "smail_de_email_sent": "Die E-Mail wurde erfolgreich gesendet."
        },

    }
    json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
    with open(os.path.join(path, 'SMAIL_config.json'), "w+", encoding='utf-8') as f:
        f.write(json_object)


def check_logfile():
    file_path = os.path.join(os.getcwd().split("smail")[0], "sconf/logs/SMAILlog.log")
    date = datetime.date.today()

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
        if lines:
            record = lines[0]
            log_date = datetime.datetime.strptime(' '.join(record.split(maxsplit=2)[:2]), "%b %d").date().replace(year=date.year)
            if log_date < date:
                os.remove(file_path)
                with open(file_path, "a") as file:
                    file.write("")
                print("Log file deleted successfully.")
                print("New log file created.")
            else:
                print("Log file is created for current day.")
        else:
            print("No log file detected.")
    else:
        print("Log file doesn't exist.")

    configure_logger()

def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.join(os.getcwd().split("smail")[0], "sconf/logs/SMAILlog.log"),
        filemode="a",
        format="%(asctime)s:SMAIL-%(levelname)s-%(funcName)s: %(message)s",
        datefmt="%b %d %H:%M:%S",
    )