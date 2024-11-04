from dataclasses import dataclass, field
from typing import List


@dataclass
class LanguageSet:
    smailEnSendToButton: str = "Send To"
    smailEnInboxLabel: str = "Inbox:"
    smailEnLoadingInbox: str= "Loading..."
    smailEnRecipientLabel: str = "To: "
    smailEnSubjectLabel: str = "Subject: "
    smailEnMessageLabel: str = "Message: "
    smailEnFrom: str = "Information: "
    smailEnDate: str = "Date: "
    smailEnEmailSent: str = "Email has been sent."
    smailEnEmailFail: str = "Email has not been sent."

    smailCzSendToButton: str = "Komu"
    smailCzInboxLabel: str = "Doručená pošta: "
    smailCzLoadingInbox: str=  "Načítám..."
    smailCzRecipientLabel: str = "Příjemce: "
    smailCzSubjectLabel: str = "Předmět: "
    smailCzMessageLabel: str = "Zpráva: "
    smailCzFrom: str = "Informace: "
    smailCzDate: str = "Datum: "
    smailCzEmailSent: str = "E-mail byl úspěšně odeslán."
    smailCzEmailFail: str = "E-mail nebyl odeslán."

    smailDeSendToButton: str = "Senden An"
    smailDeInboxLabel: str = "Posteingang: "
    smailDeLoadingInbox: str= "Laden..."
    smailDeRecipientLabel: str = "An: "
    smailDeSubjectLabel: str = "Betreff: "
    smailDeMessageLabel: str = "Nachricht: "
    smailDeFrom: str = "Information: "
    smailDeDate: str = "Datum: "
    smailDeEmailSent: str = "Die E-Mail wurde erfolgreich gesendet."
    smailDeEmailFail: str = "Die E-Mail wurde nicht gesendet."


@dataclass
class SmailConfiguration:
    seniorEmail: str = "xfiala59@gmail.com"
    seniorPassword: str = "pafotbpfrrlwvund"
    smtpServer: str = "smtp.gmail.com"
    smtpPort: int = "587"
    imapServer: str = "imap.gmail.com"
    imapPort: int = "993"
    careGiverEmail: str = ""
    emailContacts: List[str] = field(default_factory=lambda: ["sos.smail.person.1@gmail.com",
                                                              "sos.smail.person.2@gmail.com",
                                                              "sos.smail.person.3@gmail.com",
                                                              "sos.smail.person.4@gmail.com",
                                                              "sos.smail.person.5@gmail.com",
                                                              "sos.smail.person.6@gmail.com"])
    emailPicturesPath: List[str] = field(default_factory=lambda: ["../sconf/icons/exit.png",
                                                                  "../sconf/icons/smail_person_1.png",
                                                                  "../sconf/icons/smail_person_2.png",
                                                                  "../sconf/icons/smail_person_3.png",
                                                                  "../sconf/icons/smail_person_4.png",
                                                                  "../sconf/icons/smail_person_5.png",
                                                                  "../sconf/icons/smail_person_6.png"])
    sendPhishingWarning: bool = True
    showUrlInEmail: bool = True
    languageSet: LanguageSet = field(default_factory=lambda: LanguageSet())
