# Frameworks from PyQt5 libraries
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QToolBar, QWidget
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy
# Library for creating channel for monitoring input keyboard
from PyQt5.QtWebChannel import QWebChannel
# Library for parsing URL value
from urllib.parse import urlparse
# Library for getting information about user's monitor

# Created own class for logging and blocking phishing URL
import math
#import pygame
import sys, os, json, getpass, socket
from datetime import datetime

# details of error
import traceback
from sweb.ui.window import MyBrowser
from sweb.utils.monitor_provider import GetMonitorHeightAndWidth
from sweb.phish.notification_email import NotificationFillTextToPhishing




import sconf.configuration.configuration_provider as dataProvider
CONFIG_FILE_NAME = 'config.json'
SUBFOLDER_NAME = "sconf"

_dataProvider: dataProvider.ConfigurationProvider

# Library for sending mail to authorized people
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def main():
    current_location = os.getcwd()
    path_split = current_location.split("sweb")
    config_folder = os.path.join(path_split[0], SUBFOLDER_NAME)
    _dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)
    try:
        
        qApplication = QApplication(sys.argv)
        # If browser is opened in command terminal
        input_url_from_terminal = sys.argv[1] if len(sys.argv) > 1 else "https://vut.cz"
        # Load config data from JSON file
        main_window = MyBrowser(input_url_from_terminal,_dataProvider.get_sweb_configuration(),_dataProvider.get_global_configuration()) # Set parametr for main browser window
        main_window.resize(1700, 1100)
        main_window.show() 
        main_window.show_app_full_screen() # Call main browser window, this set the full screen.
        sys.exit(qApplication.exec_())
    except Exception as excep:
        print(f"Error: {excep}")
        print("Detailed traceback:")
        traceback.print_exc()
        sys.exit(1)
 
    
# Define main function to call application
if __name__ == "__main__":
    main()    
    
   
