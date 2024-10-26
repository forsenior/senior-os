from dataclasses import dataclass


@dataclass
class GlobalConfiguration:
    language: str = "English"
    colorMode: str = "light"
    alertColor: str = ""
    highlightColor: str = ""
    protectionLevel: str = "1"
