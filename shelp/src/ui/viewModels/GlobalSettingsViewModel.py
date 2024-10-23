from PyQt5.QtCore import QObject

from shelp.src.configuration.models.GlobalConfiguration import GlobalConfiguration
from shelp.src.configuration.ConfigurationDataProvider import ConfigurationProvider


class GlobalViewModel():
    _globalConfiguration: GlobalConfiguration

    def __init__(self, global_configuration: GlobalConfiguration):
        super().__init__()
        self._globalConfiguration = global_configuration

#    def __del__(self):
#        super().__del__(QObject)
#        ConfigurationProvider.update_memory_configuration(self._globalConfiguration)

    def update_model(self, attribute_name: str, value):
        if hasattr(self._globalConfiguration, attribute_name):
            setattr(self._globalConfiguration, attribute_name, value)
        else:
            raise AttributeError(f"{attribute_name} is not valid attribute")