from dataclasses import dataclass, field
from typing import List


@dataclass
class SwebConfiguration:
    urlsForWebsites: List[str] = field(default_factory=lambda: ["https://irozhlas.cz/",
                                                                "https://edition.cnn.com/",
                                                                "https://www.vut.cz/",
                                                                "https://google.com/",
                                                                "https://www.aktualne.cz/",
                                                                "https://www.denik.cz/"])
    
    picturePaths: List[str] = field(default_factory=lambda: ["../sconf/icons/exit.png",
                                                             "../sconf/icons/sweb_www_1.png",
                                                            "../sconf/icons/sweb_www_2.png",
                                                            "../sconf/icons/sweb_www_3.png",
                                                            "../sconf/icons/sweb_www_4.jpg",
                                                            "../sconf/icons/sweb_www_5.png",
                                                            "../sconf/icons/sweb_www_6.png"])
    allowedURL: str = "../sconf/phish/sweb_allowed_url.txt"
    phishingDatabase: str = "../sconf/phish/sweb_phish_1.txt"
    phishingGithubDatabase: str = "https://github.com/mitchellkrogza/Phishing.Database/raw/master/ALL-phishing-domains.tar.gz/"
    sendPhishingWarning: bool = True
    phishingFormular: bool = True
    seniorWebsitePosting: bool = True
    allowedWebsites: List[str] = field(default_factory=lambda: ["https://seznam.cz",
                                                                "https://google.com",
                                                                "https://vut.cz"])
    default_language: str = "cz"
    text: List[str] = field(default_factory=lambda: ["MENU 1",
                                                     "MENU 2",
                                                     "Search",
                                                     "MENU 1",
                                                     "MENU 2",
                                                     "Vyhledávání",
                                                     "MENU 1",
                                                     "MENU 2",
                                                     "Suche",])
