from dataclasses import dataclass, field

from sconf.src.configuration.models.global_configuration import GlobalConfiguration
from sconf.src.configuration.models.smail_configuration import SmailConfiguration
from sconf.src.configuration.models.sweb_configuration import SwebConfiguration


@dataclass
class SOSConfiguration:
    globalConfiguration: GlobalConfiguration = field(default_factory=lambda: GlobalConfiguration())
    swebConfiguration: SwebConfiguration = field(default_factory=lambda: SwebConfiguration())
    smailConfiguration: SmailConfiguration = field(default_factory=lambda: SmailConfiguration())
