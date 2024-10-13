import json
import os.path

from shelp.src.configuration.Models.GlobalConfiguration import GlobalConfiguration
from shelp.src.decorators.Decorators import singleton


@singleton
class ConfigurationProvider:
    _configFileName: str = ""
    _configStoragePath: str = ""
    _configuration: GlobalConfiguration

    def __init__(self, configFileName: str, configStoragePath: str):
        self._configFileName = configFileName
        self._configStoragePath = configStoragePath

        self.__loadConfiguration()

    def __updateSavedConfiguration(self):
        return True

    def __loadConfiguration(self):
        with open(os.path.join(self._configStoragePath, self._configFileName), 'r') as sourceFile:
            self._configuration = json.load(sourceFile)

    def getGlobalConfiguration(self):
        return self._configuration
