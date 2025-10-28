import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy

from smail.layout import first_frame
from smail.smail_confview import MainWindow


import sconf.configuration.configuration_writer as dataWriter
import sconf.configuration.configuration_provider as dataProvider

CONFIG_FILE_NAME = 'config.json'

def main():
    """
        Starts the email client, initializes the application window, and loads configuration.
    """
    try:
        _dataWriter: dataWriter.ConfigurationWriter
        _dataProvider: dataProvider.ConfigurationProvider
        config_folder = os.getcwd()

        _dataWriter = dataWriter.ConfigurationWriter()
        _dataProvider = dataProvider.ConfigurationProvider()

        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        window = MainWindow(screen, _dataProvider, _dataWriter, config_folder)
        window.showFullScreen()
        #window.setGeometry(100, 100, 1280, 720)
        window.setMinimumSize(1280, 720)
        window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        window.setWindowFlags(Qt.FramelessWindowHint)
        window.show()
        app.exec()

    except Exception as e:
        print(f"Could not start SMAIL app, error loading configuration. {e}" )

if __name__ == '__main__':
    main()
