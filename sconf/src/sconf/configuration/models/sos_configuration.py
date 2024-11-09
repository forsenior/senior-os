from dataclasses import dataclass, field

from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.configuration.models.sweb_configuration import SwebConfiguration


@dataclass
class SOSConfiguration:
    initialStartUp: bool = True
    configurationPassword: str = ""
    globalConfiguration: GlobalConfiguration = field(default_factory=lambda: GlobalConfiguration())
    swebConfiguration: SwebConfiguration = field(default_factory=lambda: SwebConfiguration())
    smailConfiguration: SmailConfiguration = field(default_factory=lambda: SmailConfiguration())
