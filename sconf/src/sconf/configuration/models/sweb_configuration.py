from dataclasses import dataclass, field
from typing import List


@dataclass
class SwebConfiguration:
    swebAllowedUrlListV2: List[dict] = field(default_factory=lambda : [
        {"url1": "https://irozhlas.cz/", "icon1": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_1.png"},
        {"url2": "https://edition.cnn.com/", "icon2": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_2.png"},
        {"url3": "https://www.vut.cz/", "icon3": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_3.png"},
        {"url4": "https://google.com/", "icon4": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_4.jpg"},
        {"url5": "https://www.aktualne.cz/", "icon5": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_5.png"},
        {"url6": "https://www.denik.cz/", "icon6": "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_6.png"},
    ])
    urlsForWebsites: List[str] = field(default_factory=lambda: ["https://irozhlas.cz/",
                                                                "https://edition.cnn.com/",
                                                                "https://www.vut.cz/",
                                                                "https://www.info-zdravi.cz/",
                                                                "https://www.aktualne.cz/",
                                                                "https://www.denik.cz/"])

    picturePaths: List[str] = field(default_factory=lambda: ["/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/exit.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_1.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_2.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_3.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_4.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_5.png",
                                                             "/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/sweb_www_6.png"])
    allowedURL: str = "/run/archiso/airootfs/usr/lib/python3.13/site-packages/phish/sweb_allowed_url.txt"
    phishingDatabase: str = "/run/archiso/airootfs/usr/lib/python3.13/site-packages/phish/sweb_phish.txt"
    command_line_mail_script: str = "/run/archiso/airootfs/usr/lib/python3.13/site-packages/smail/connection/command_line_mail.py"
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
