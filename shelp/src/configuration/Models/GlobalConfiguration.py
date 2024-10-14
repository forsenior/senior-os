from shelp.src.configuration.Models import SwebConfiguration, SmailConfiguration
from dataclasses import dataclass, field


@dataclass
class MenuBarTextConfiguration:
    fontFamily: str = "Inter"
    fontSize: int = 40
    fontWeight: str = "Regular"
    fontColor: str = "FFFFFF"


@dataclass
class MenuButtonConfiguration:
    buttonSize: [int, int] = field(default_factory=lambda: [244, 107])
    buttonCornerRadius: int = 3
    buttonBorderThickness: int = 1
    buttonFill: str = "949494"
    borderColor: str = "797979"
    alertFill: str = "F90000"
    alertBorderColor: str = "797979"


@dataclass
class MainWindowConfiguration:
    windowSize: [int, int] = field(default_factory=lambda: [1260, 580])
    backgroundColor: str = "FFFFFF"
    borderCornerRadius: int = 3
    borderThickness: int = 3
    borderColor: str = "000000"


@dataclass
class MenuBarConfiguration:
    backGroundFill: str = ""
    borderFill: str = ""
    textConfiguration: MenuBarTextConfiguration = field(default_factory=lambda: MenuBarTextConfiguration())
    buttonConfiguration: MenuButtonConfiguration = field(default_factory=lambda: MenuButtonConfiguration())


@dataclass
class GlobalConfiguration:
    language: str = "en"
    colorMode: str = "light"
    protectionLevel: int = "1"
    menuBarConfiguration: MenuBarConfiguration = field(default_factory=lambda: MenuBarConfiguration())
    mainWindowConfiguration: MainWindowConfiguration = field(default_factory=lambda: MainWindowConfiguration())
    swebConfiguration: SwebConfiguration.SwebConfiguration = field(default_factory=lambda: SwebConfiguration
                                                                   .SwebConfiguration())
    smailConfiguration: SmailConfiguration.SmailConfiguration = field(default_factory=lambda: SmailConfiguration
                                                                      .SmailConfiguration())
