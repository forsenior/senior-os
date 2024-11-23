from dataclasses import dataclass, field
from typing import List


@dataclass
class SwebConfiguration:
    swebAllowedUrlListV2: List[dict] = field(default_factory=lambda : [
        {"url1": "https://irozhlas.cz/", "icon1": "../sconf/icons/sweb_www_1.png"},
        {"url2": "https://edition.cnn.com/", "icon2": "../sconf/icons/sweb_www_2.png"},
        {"url3": "https://www.vut.cz/", "icon3": "../sconf/icons/sweb_www_3.png"},
        {"url4": "https://google.com/", "icon4": "../sconf/icons/sweb_www_4.jpg"},
        {"url5": "https://www.aktualne.cz/", "icon5": "../sconf/icons/sweb_www_5.png"},
        {"url6": "https://www.denik.cz/", "icon6": "../sconf/icons/sweb_www_6.png"},
    ])
    urlsForWebsites: List[str] = field(default_factory=lambda: ["https://irozhlas.cz/",
                                                                "https://edition.cnn.com/",
                                                                "https://www.vut.cz/",
                                                                "https://www.info-zdravi.cz/",
                                                                "https://www.aktualne.cz/",
                                                                "https://www.denik.cz/"])

    picturePaths: List[str] = field(default_factory=lambda: ["../sconf/icons/exit.png",
                                                             "../sconf/icons/sweb_www_1.png",
                                                             "../sconf/icons/sweb_www_2.png",
                                                             "../sconf/icons/sweb_www_3.png",
                                                             "../sconf/icons/sweb_www_4.png",
                                                             "../sconf/icons/sweb_www_5.png",
                                                             "../sconf/icons/sweb_www_6.png"])
    allowedURL: str = "../sconf/phish/sweb_allowed_url.txt"
    phishingDatabase: str = "../sconf/phish/sweb_phish.txt"
    phishingGithubDatabase: str = "https://github.com/mitchellkrogza/Phishing.Database/raw/master/ALL-phishing-domains.tar.gz/"
    sendPhishingWarning: bool = True
    phishingFormular: bool = True
    seniorWebsitePosting: bool = True
    whiteListedWebsitesOnly: bool = False
    allowWebSearch: bool = True
    default_language: str = "cz"
    text: List[str] = field(default_factory=lambda: ["MENU 1",
                                                     "MENU 2",
                                                     "Search",
                                                     "MENU 1",
                                                     "MENU 2",
                                                     "Vyhledávání",
                                                     "MENU 1",
                                                     "MENU 2",
                                                     "Suche", ])
