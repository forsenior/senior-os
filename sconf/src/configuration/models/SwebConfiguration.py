from dataclasses import dataclass, field
from typing import List


@dataclass
class SwebConfiguration:
    urlsForWebsites: List[str] = field(default_factory=lambda: ["https://seznam.cz",
                                                                "https://google.com",
                                                                "https://vut.cz"])
    picturePaths: List[str] = field(default_factory=lambda: ["",
                                                             "",
                                                             ""])
    sendPhishingWarning: bool = True
    phishingFormular: bool = True
    seniorWebsitePosting: bool = True
    allowedWebsites: List[str] = field(default_factory=lambda: ["https://seznam.cz",
                                                                "https://google.com",
                                                                "https://vut.cz"])
