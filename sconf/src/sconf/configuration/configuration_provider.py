import json
import os.path
from pathlib import Path

from dataclass_wizard import fromdict

from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.configuration.models.sos_configuration import SOSConfiguration
from sconf.configuration.models.sweb_configuration import SwebConfiguration
from sconf.decorators.decorators import singleton
from sconf.configuration.default_configuration import default_configuration

@singleton
class ConfigurationProvider:
    _configFileName: str = ""
    _configStoragePath: str = ""
    _sosConfiguration: SOSConfiguration

    def __init__(self, configFileName: str = 'config.json', configStoragePath: str = os.path.join(Path.home(), '.sconf')):
        """
        Class providing access to the configuration data of the SOS.
        This class has singleton decorator which should allow existence of only singular instance of this class.
        :param configFileName: Name of the SOS configuration file
        :param configStoragePath: Expected folder path from which the configuration can be loaded into memory
        """
        self._configFileName = 'config.json'
        if os.path.exists(os.path.join(Path.home(), '.sconf')):
            if os.path.isdir(os.path.join(Path.home(), '.sconf')):
                self._configStoragePath = os.path.join(Path.home(), '.sconf')
            else:
                print(f"{os.path.join(Path.home(), '.sconf')} exists and is NOT a directory!")
                exit(1)
        else:
            os.mkdir(os.path.join(Path.home(), '.sconf'))

        self.__load_configuration()

    def __load_configuration(self):
        config_file = os.path.join(self._configStoragePath, self._configFileName)
        if not os.path.exists(config_file):
            with open(config_file, 'w') as newConfig:
                json.dump(default_configuration(), newConfig)
        with open(config_file, 'r') as sourceFile:
            self._sosConfiguration: SOSConfiguration = fromdict(SOSConfiguration, json.load(sourceFile))

    def update_memory_configuration(self, configuration):
        if isinstance(configuration, SOSConfiguration):
            self._sosConfiguration = configuration
        if isinstance(configuration, GlobalConfiguration):
            self._sosConfiguration.globalConfiguration = configuration
        if isinstance(configuration, SwebConfiguration):
            self._sosConfiguration.swebConfiguration = configuration
        if isinstance(configuration, SmailConfiguration):
            self._sosConfiguration.smailConfiguration = configuration

    def get_main_configuration(self) -> SOSConfiguration:
        """
        This method allows any caller to retrieve all configuration information from the memory

        To Use:
            1. Import data viewModels from sconf/src/configuration/viewModels
            2. Call this method
            3. Either map it to the model or use as it is
        :return: `SOSConfiguration`
        """
        return self._sosConfiguration

    def get_global_configuration(self) -> GlobalConfiguration:
        """
        This method allows any caller to retrieve configuration information for the GlobalConfig from the memory
        :return: `GlobalConfiguration`
        """
        return self._sosConfiguration.globalConfiguration

    def get_sweb_configuration(self) -> SwebConfiguration:
        """
        This method allows any caller to retrieve configuration information for the SWEB from the memory
        :return: `SwebConfiguration`
        """
        return self._sosConfiguration.swebConfiguration

    def get_smail_configuration(self) -> SmailConfiguration:
        """
        This method allows any caller to retrieve configuration information for the SMAIL from the memory
        :return: `SmailConfiguration`
        """
        return self._sosConfiguration.smailConfiguration
