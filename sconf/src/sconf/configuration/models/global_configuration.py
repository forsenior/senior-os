from dataclasses import dataclass


@dataclass
class GlobalConfiguration:
    language: str = "en"
    colorMode: str = "light"
    alertColor: str = "F90000"
    highlightColor: str = "48843F"
    protectionLevel: int = 1
    careGiverEmail: str = "tarikalkanan@gmail.com"
