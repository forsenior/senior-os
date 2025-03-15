import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy

from smail.layout import first_frame


import sconf.configuration.configuration_writer as dataWriter
import sconf.configuration.configuration_provider as dataProvider

def main():
    """
        Starts the email client, initializes the application window, and loads configuration.
    """
    _dataProvider = dataProvider.ConfigurationProvider()

    try:

        app = QApplication([])
        window = QMainWindow()
        window.showFullScreen()
        #window.setGeometry(100, 100, 1280, 720)
        window.setMinimumSize(1280, 720)
        window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        window.setWindowFlags(Qt.FramelessWindowHint)
        layout = first_frame(window, _dataProvider)
        window.setCentralWidget(layout)
        window.show()
        app.exec()

    except Exception as e:
        print(f"Could not start SMAIL app, error loading configuration. {e}" )

if __name__ == '__main__':
    main()
