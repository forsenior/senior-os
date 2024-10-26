from dataclasses import dataclass, field

from sconf.src.configuration.models.GlobalConfiguration import GlobalConfiguration
from sconf.src.configuration.models.SmailConfiguration import SmailConfiguration
from sconf.src.configuration.models.SwebConfiguration import SwebConfiguration


@dataclass
class SOSConfiguration:
    globalConfiguration: GlobalConfiguration = field(default_factory=lambda: GlobalConfiguration())
    swebConfiguration: SwebConfiguration = field(default_factory=lambda: SwebConfiguration())
    smailConfiguration: SmailConfiguration = field(default_factory=lambda: SmailConfiguration())
