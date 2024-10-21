from shelp.src.configuration.models import SwebConfiguration, SmailConfiguration
from dataclasses import dataclass, field


@dataclass
class GlobalConfiguration:
    language: str = "en"
    colorMode: str = "light"
    alertColor: str = ""
    highlightColor: str = ""
    protectionLevel: int = "1"


@dataclass
class SOSConfiguration:
    globalConfiguration: GlobalConfiguration = field(default_factory=lambda: GlobalConfiguration())
    swebConfiguration: SwebConfiguration.SwebConfiguration = field(default_factory=lambda: SwebConfiguration
                                                                   .SwebConfiguration())
    smailConfiguration: SmailConfiguration.SmailConfiguration = field(default_factory=lambda: SmailConfiguration
                                                                      .SmailConfiguration())
