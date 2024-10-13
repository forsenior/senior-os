import os.path
import json
import dataclasses
import shelp.src.configuration.Models.GlobalConfiguration as globalConfig
import shelp.src.configuration.Models.SwebConfiguration as swebConfig

from shelp.src.decorators.Decorators import singleton


@singleton
class ConfigurationWriter:
    _configFileName: str = ""
    _configStoragePath: str = ""

    def __init__(self, configFileName: str, configStoragePath: str):
        self._configFileName = configFileName
        self._configStoragePath = configStoragePath

        self.__validateAndCreateDefaultConfig()

    def updateConfiguration(self, configuration: globalConfig.GlobalConfiguration):
        configuration_json = json.dumps(configuration)
        self.__writeConfigToJson(configuration_json)

    def __validateAndCreateDefaultConfig(self):
        if not os.path.isfile(os.path.join(self._configStoragePath, self._configFileName)):
            default_config = globalConfig.GlobalConfiguration(
                language="en",
                colorMode="light",
                protectionLevel=1,
                menuBarConfiguration=globalConfig.MenuBarConfiguration(
                    backGroundFill="",
                    borderFill="",
                    buttonConfiguration=globalConfig.MenuButtonConfiguration(
                        buttonSize=[244, 107],
                        buttonCornerRadius=3,
                        buttonBorderThickness=1,
                        buttonFill="949494",
                        borderColor="797979",
                        alertFill="F90000",
                        alertBorderColor="797979"
                    ),
                    textConfiguration=globalConfig.MenuBarTextConfiguration(
                        fontFamily="Inter",
                        fontSize=40,
                        fontWeight="Regular",
                        fontColor="FFFFFF"
                    )
                ),
                mainWindowConfiguration=globalConfig.MainWindowConfiguration(
                    windowSize=[1260, 580],
                    backgroundColor="FFFFFF",
                    borderCornerRadius=3,
                    borderThickness=3,
                    borderColor="000000"
                ),
                swebConfiguration=swebConfig.SwebConfiguration(
                    urlsForWebsites=["https://seznam.cz",
                                     "https://google.com",
                                     "https://vut.cz"],
                    picturePaths=["",
                                  "",
                                  ""],
                    sendPhishingWarning=True,
                    phishingFormular=True,
                    seniorWebsitePosting=True,
                    allowedWebsites=["https://seznam.cz",
                                     "https://google.com",
                                     "https://vut.cz"]
                )
            )

            self.__writeConfigToJson(json.dumps(default_config, indent=4, cls=EnhancedJSONEncoder))

        pass

    def __writeConfigToJson(self, config: str):
        with open(os.path.join(self._configStoragePath, self._configFileName), "w+", encoding='utf-8') as outfile:
            outfile.write(config)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
