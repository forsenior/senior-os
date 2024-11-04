import sys
import os
from PyQt5.QtWidgets import  QApplication, QMainWindow
from src.layout import first_frame

current_dir = os.path.dirname(os.path.abspath(__file__))
sconf_src_path = os.path.join(current_dir, '../sconf/src')
sys.path.append(sconf_src_path)

import configuration.configuration_writer as dataWriter
import configuration.configuration_provider as dataProvider


if __name__ == '__main__':

    CONFIG_FILE_NAME = 'config.json'
    config_folder = os.path.join(current_dir, '../sconf')

    _dataWriter = dataWriter.ConfigurationWriter(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)
    _dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)

    try:

        app = QApplication([])
        window = QMainWindow()
        window.setWindowTitle("SMAIL App")
        # window.showFullScreen()
        window.setGeometry(100, 100, 1280, 720)
        layout = first_frame(window, _dataProvider)
        window.setCentralWidget(layout)
        window.show()
        app.exec()

    except Exception as e:
        print(f"Could not start SMAIL app, error loading configuration. {e}" )