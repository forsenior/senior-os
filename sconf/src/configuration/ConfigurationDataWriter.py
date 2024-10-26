import dataclasses
import json
import os.path

from dataclass_wizard import asdict

import sconf.src.configuration.models.GlobalConfiguration as globalConfig
import sconf.src.configuration.models.SmailConfiguration as smailConfig
import sconf.src.configuration.models.SwebConfiguration as swebConfig
from sconf.src.configuration.models import SosConfiguration
from sconf.src.decorators.Decorators import singleton


@singleton
class ConfigurationWriter:
    _configFileName: str = ""
    _configStoragePath: str = ""

    def __init__(self, configFileName: str, configStoragePath: str):
        """
        Class providing ability to save the configuration into the persistent storage
        :param configFileName: Name of the SOS configuration file
        :param configStoragePath: Expected folder path from which the configuration can be loaded into memory
        """
        self._configFileName = configFileName
        self._configStoragePath = configStoragePath

        self.__validate_and_create_default_config()

    def update_configuration(self, configuration: SosConfiguration.SOSConfiguration):
        """
        Method allowing the caller to save GlobalConfiguration into persistent storage as a python
        :param configuration: :py:class: `GlobalConfiguration`
        :return:
        """
        configuration = asdict(configuration)
        configuration_json = json.dumps(configuration)
        self.__save_configuration(configuration_json)

    def __validate_and_create_default_config(self):
        """
        Private method creating default configuration os SOS if the specified file is not present
        :return:
        """
        if not os.path.isfile(os.path.join(self._configStoragePath, self._configFileName)):
            default_config = SosConfiguration.SOSConfiguration(
                globalConfiguration=globalConfig.GlobalConfiguration(),
                smailConfiguration=smailConfig.SmailConfiguration(),
                swebConfiguration=swebConfig.SwebConfiguration()
            )

            self.__save_configuration(json.dumps(default_config, indent=4, cls=EnhancedJSONEncoder, ensure_ascii=True))

        pass

    def __save_configuration(self, config: str):
        with open(os.path.join(self._configStoragePath, self._configFileName), "w+", encoding='utf-8') as outfile:
            outfile.write(config)


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    JSON Encoder allowing json dump to process @dataclass viewModels
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
