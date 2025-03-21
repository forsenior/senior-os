import os
import sys

from PyQt5.QtWidgets import QApplication

from sconf.ui.view.main_window_view import MainWindow
import sconf.configuration.configuration_writer as data_writer
import sconf.configuration.configuration_provider as data_provider

CONFIG_FILE_NAME = 'config.json'


def main():
    try:
        _dataWriter: data_writer.ConfigurationWriter
        _dataProvider: data_provider.ConfigurationProvider
        config_folder = os.getcwd()

        _dataWriter = data_writer.ConfigurationWriter()
        _dataProvider = data_provider.ConfigurationProvider()

        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        print(f"Screen size: {screen.size()}")

        window = MainWindow(screen, _dataProvider, _dataWriter, config_folder)
        window.show()
        window.showFullScreen()
        print(window.size())
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Exception occurred {e}")


if __name__ == '__main__':
    # Initialize the main method
    main()
