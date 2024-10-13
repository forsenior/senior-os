import os
import configuration.ConfigurationDataWriter as dataWriter
import configuration.ConfigurationDataProvider as dataProvider

CONFIG_FILE_NAME = 'SOS-conf.json'
SUBFOLDER_NAME = "sconf"

_dataProvider: dataProvider.ConfigurationProvider
_dataWriter: dataWriter.ConfigurationWriter

def main():
    current_location = os.getcwd()
    path_split = current_location.split("shelp")
    config_folder = os.path.join(path_split[0], SUBFOLDER_NAME)

    _dataWriter = dataWriter.ConfigurationWriter(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)
    _dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)
    test = _dataProvider.getGlobalConfiguration()
    print(test)


if __name__ == '__main__':
    #Initialize the main method
    main()

