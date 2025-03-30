from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class LanguageSet:
    smailEnSendToButton: str = "Send To"
    smailEnSendToButtonDisabled: str = "Disabled"
    smailEnInboxLabel: str = "Inbox:"
    smailEnLoadingInbox: str= "Loading..."
    smailEnRecipientLabel: str = "To: "
    smailEnSubjectLabel: str = "Subject: "
    smailEnMessageLabel: str = "Message: "
    smailEnFrom: str = "Information: "
    smailEnDate: str = "Date: "
    smailEnEmailSent: str = "Email has been sent."
    smailEnEmailFail: str = "Email has not been sent."
    smailEnUndeliveredEmail: str = "The email was not delivered to the address {recipient_email}."
    smailEnSensitiveContentWarning: str = "Warning: \nThe email contains sensitive information. \nPress the button a second time to send the email."
    smailEnUnconfirmedEmailWarning: str = "Warning: \nUnconfirmed email in progress. \nPress the button again to cancel."


    smailCzSendToButton: str = "Komu"
    smailCzSendToButtonDisabled: str = "Uzamčeno"
    smailCzInboxLabel: str = "Doručená pošta: "
    smailCzLoadingInbox: str=  "Načítám..."
    smailCzRecipientLabel: str = "Příjemce: "
    smailCzSubjectLabel: str = "Předmět: "
    smailCzMessageLabel: str = "Zpráva: "
    smailCzFrom: str = "Informace: "
    smailCzDate: str = "Datum: "
    smailCzEmailSent: str = "E-mail byl úspěšně odeslán."
    smailCzEmailFail: str = "E-mail nebyl odeslán."
    smailCzUndeliveredEmail: str = "Email nebyl doručen na adresu {recipient_email}."
    smailCzSensitiveContentWarning: str = "Varování: \nEmail obsahuje citlivé údaje. \nStisknutím tlačítka podruhé email odešlete."
    smailCzUnconfirmedEmailWarning: str = "Varování: \nRozpracovaný email nebyl potvrzen. \nDalším stisknutím dojde k jeho zrušení."

    smailDeSendToButton: str = "Senden An"
    smailDeSendToButtonDisabled: str = "Aus"
    smailDeInboxLabel: str = "Posteingang: "
    smailDeLoadingInbox: str= "Laden..."
    smailDeRecipientLabel: str = "An: "
    smailDeSubjectLabel: str = "Betreff: "
    smailDeMessageLabel: str = "Nachricht: "
    smailDeFrom: str = "Information: "
    smailDeDate: str = "Datum: "
    smailDeEmailSent: str = "Die E-Mail wurde erfolgreich gesendet."
    smailDeEmailFail: str = "Die E-Mail wurde nicht gesendet."
    smailDeUndeliveredEmail: str = "Die E-Mail wurde nicht an die Adresse {recipient_email} zugestellt."
    smailDeSensitiveContentWarning: str = "Warnung: \nDie E-Mail enthält sensible Daten. \nDurch erneutes Drücken der Taste wird die E-Mail gesendet."
    smailDeUnconfirmedEmailWarning: str = "Warnung: \nUnbestätigte E-Mail in Bearbeitung. \nDrücken Sie die Taste erneut, um sie abzubrechen."


@dataclass
class SmailConfiguration:
    seniorEmail: str = "xfiala59@gmail.com"
    seniorPassword: str = "pafotbpfrrlwvund"
    smtpServer: str = "smtp.gmail.com"
    smtpPort: int = "587"
    imapServer: str = "imap.gmail.com"
    imapPort: int = "993"
    emailContactsV2: List[dict] = field(default_factory=lambda: [
        {"email1": "sos.smail.person.1@gmail.com", "icon1": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_0.png"},
        {"email2": "sos.smail.person.2@gmail.com", "icon2": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_2.png"},
        {"email3": "sos.smail.person.3@gmail.com", "icon3": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_3.png"},
        {"email4": "sos.smail.person.4@gmail.com", "icon4": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_4.png"},
        {"email5": "sos.smail.person.5@gmail.com", "icon5": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_5.png"},
        {"email6": "sos.smail.person.6@gmail.com", "icon6": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/smail_person_6.png"},
    ])

    sendPhishingWarning: bool = True
    showUrlInEmail: bool = True
    receiveWhitelistedEmailsOnly: bool = False
    sendWhitelistedEmailsOnly: bool = False
    languageSet: LanguageSet = field(default_factory=lambda: LanguageSet())
