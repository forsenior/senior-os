import json
import os.path

from shelp.src.configuration.models.GlobalConfiguration import GlobalConfiguration
from shelp.src.configuration.models.SmailConfiguration import SmailConfiguration
from shelp.src.configuration.models.SosConfiguration import SOSConfiguration
from shelp.src.configuration.models.SwebConfiguration import SwebConfiguration
from shelp.src.decorators.Decorators import singleton


@singleton
class ConfigurationProvider:
    _configFileName: str = ""
    _configStoragePath: str = ""
    _sosConfiguration: SOSConfiguration

    def __init__(self, configFileName: str, configStoragePath: str):
        """
        Class providing access to the configuration data of the SOS.
        This class has singleton decorator which should allow existence of only singular instance of this class.
        :param configFileName: Name of the SOS configuration file
        :param configStoragePath: Expected folder path from which the configuration can be loaded into memory
        """
        self._configFileName = configFileName
        self._configStoragePath = configStoragePath

        self.__load_configuration()

    def __load_configuration(self):
        with open(os.path.join(self._configStoragePath, self._configFileName), 'r') as sourceFile:
            self._sosConfiguration: SOSConfiguration = json.load(sourceFile)

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
            1. Import data viewModels from shelp/src/configuration/viewModels
            2. Call this method
            3. Either map it to the model or use as it is
        :return: :py:class:`SOSConfiguration`
        """
        return self._sosConfiguration

    def get_global_configuration(self):
        """
        This method allows any caller to retrieve configuration information for the GlobalConfig from the memory
        :return: :py:class: `GlobalConfiguration`
        """
        return self._sosConfiguration

    def get_sweb_configuration(self) -> SwebConfiguration:
        """
        This method allows any caller to retrieve configuration information for the SWEB from the memory
        :return: :py:class: `SwebConfiguration`
        """
        return self._sosConfiguration.swebConfiguration

    def get_smail_configuration(self) -> SmailConfiguration:
        """
        This method allows any caller to retrieve configuration information for the SMAIL from the memory
        :return: :py:class: `SmailConfiguration`
        """
        return self._sosConfiguration.smailConfiguration
