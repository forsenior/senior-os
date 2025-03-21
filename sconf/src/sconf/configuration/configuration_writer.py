import dataclasses
import json
import os.path
from pathlib import Path

from dataclass_wizard import asdict

import sconf.configuration.models.global_configuration as global_config
import sconf.configuration.models.smail_configuration as smail_config
import sconf.configuration.models.sweb_configuration as sweb_config
from sconf.configuration.models import sos_configuration
from sconf.decorators.decorators import singleton


@singleton
class ConfigurationWriter:
    _configFileName: str = ""
    _configStoragePath: str = ""

    def __init__(self, configFileName: str = 'config.json', configStoragePath: str = os.path.join(Path.home(), '.sconf')):
        """
        Class providing ability to save the configuration into the persistent storage.
        Also, solely responsible for creating the config.json file in an instance that the file is not present!
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

        self.__validate_and_create_default_config()

    def update_configuration(self, configuration: sos_configuration.SOSConfiguration):
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
            default_config = sos_configuration.SOSConfiguration(
                globalConfiguration=global_config.GlobalConfiguration(),
                smailConfiguration=smail_config.SmailConfiguration(),
                swebConfiguration=sweb_config.SwebConfiguration()
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
