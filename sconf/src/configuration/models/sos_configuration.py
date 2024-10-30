from dataclasses import dataclass, field

from configuration.models.GlobalConfiguration import GlobalConfiguration
from configuration.models.SmailConfiguration import SmailConfiguration
from configuration.models.SwebConfiguration import SwebConfiguration


@dataclass
class SOSConfiguration:
    globalConfiguration: GlobalConfiguration = field(default_factory=lambda: GlobalConfiguration())
    swebConfiguration: SwebConfiguration = field(default_factory=lambda: SwebConfiguration())
    smailConfiguration: SmailConfiguration = field(default_factory=lambda: SmailConfiguration())
