from dataclasses import dataclass, field
from typing import List


@dataclass
class SmailConfiguration:
    seniorEmail: str = ""
    seniorPassword: str = ""
    careGiverEmail: str = ""
    emailContacts: List[str] = field(default_factory=lambda: ["",
                                                              "",
                                                              "",
                                                              "",
                                                              "",
                                                              ""])
    emailPicturesPath: List[str] = field(default_factory=lambda: ["",
                                                                  "",
                                                                  "",
                                                                  "",
                                                                  "",
                                                                  ""])
    sendPhishingWarning: bool = True
    showUrlInEmail: bool = True
