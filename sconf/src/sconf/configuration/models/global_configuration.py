from dataclasses import dataclass


@dataclass
class GlobalConfiguration:
    language: str = "en"
    colorMode: str = "light"
    alertColor: str = ""
    highlightColor: str = ""
    protectionLevel: int = 1
