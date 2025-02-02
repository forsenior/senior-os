import os
import sys

from PyQt5.QtWidgets import QApplication


from sconf.ui.view.main_window_view import MainWindow
import sconf.configuration.configuration_provider as data_provider
import sconf.configuration.configuration_writer as data_writer


CONFIG_FILE_NAME = 'config.json'


def main():
    try:
        _dataProvider: data_provider.ConfigurationProvider
        _dataWriter: data_writer.ConfigurationWriter
        config_folder = os.getcwd()

        _dataProvider = data_provider.ConfigurationProvider()
        _dataWriter = data_writer.ConfigurationWriter()

        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        print(f"Screen size: {screen.size()}")

        window = MainWindow(_dataProvider, _dataWriter, config_folder)
        window.setBaseSize(1270, 800)
        window.resize(1270, 800)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Exception occurred {e}")


if __name__ == '__main__':
    # Initialize the main method
    main()
