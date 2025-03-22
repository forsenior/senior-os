import sys

from PyQt5.QtWidgets import QApplication


from srun.ui.view.main_window_view import MainWindowView
import sconf.configuration.configuration_provider as dp
import sconf.configuration.configuration_writer as dw


def main():
    # try:
        data_writer = dw.ConfigurationWriter()
        data_provider = dp.ConfigurationProvider()

        print(data_provider.get_main_configuration())

        app = QApplication(sys.argv)
        window = MainWindowView(data_provider, data_writer)
        window.show()
        sys.exit(app.exec_())

    # except Exception as e:
    #     print(f"Exception occurred {e}")


if __name__ == '__main__':
    main()
