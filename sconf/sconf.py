import os
import sys

from PyQt5.QtWidgets import QApplication

import configuration.configuration_provider as data_provider
import configuration.configuration_writer as data_writer
from ui.view.main_window_view import MainWindow

CONFIG_FILE_NAME = 'config.json'


def main():
    try:
        _dataProvider: data_provider.ConfigurationProvider
        _dataWriter: data_writer.ConfigurationWriter
        config_folder = os.getcwd()

        _dataWriter = data_writer.ConfigurationWriter(configFileName=CONFIG_FILE_NAME,
                                                      configStoragePath=config_folder)
        _dataProvider = data_provider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME,
                                                            configStoragePath=config_folder)

        app = QApplication(sys.argv)
        window = MainWindow(_dataProvider, _dataWriter, config_folder)
        window.show()
        sys.exit(app.exec_())
    except:
        print(f"Exception occurred")


if __name__ == '__main__':
    # Initialize the main method
    main()