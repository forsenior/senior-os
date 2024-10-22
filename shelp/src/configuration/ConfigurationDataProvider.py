import json
import os.path

from shelp.src.configuration.models.SosConfiguration import SOSConfiguration
from shelp.src.decorators.Decorators import singleton


@singleton
class ConfigurationProvider:
    _configFileName: str = ""
    _configStoragePath: str = ""
    _configuration: SOSConfiguration

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

    def __update_saved_configuration(self):
        return True

    def __load_configuration(self):
        with open(os.path.join(self._configStoragePath, self._configFileName), 'r') as sourceFile:
            self._configuration: SOSConfiguration = json.load(sourceFile)

    def get_configuration(self):
        """
        This method allows any caller to retrieve configuration information for the SWEB and SMAIL from the memory

        To Use:
            1. Import data viewModels from shelp/src/configuration/viewModels
            2. Call this method
            3. Either map it to the model or use as it is
        :return: :py:class:`GlobalConfiguration`
        """
        return self._configuration
