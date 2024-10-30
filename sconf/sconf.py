import os
import sys

from PyQt5.QtWidgets import QApplication

import configuration.ConfigurationDataProvider as dataProvider
import configuration.ConfigurationDataWriter as dataWriter
from ui.view.MainWindowView import MainWindow

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

    app = QApplication(sys.argv)
    window = MainWindow(_dataProvider, _dataWriter, config_folder)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Initialize the main method
    main()