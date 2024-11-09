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

# Get the current directory of the script and go one level up
#current_directory = os.path.dirname(os.path.abspath(__file__))
#parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
#sys.path.append(parent_directory)

<<<<<<< HEAD:sweb/src/sweb/__main__.py
from sweb.url_blocker import URLBlocker
from sweb.update_phishing_txt import PhishingDatabaseModificationChecker
from sweb.language_translator import Translator
=======
from src.ui.window import MyBrowser
from src.utils.monitor_provider import GetMonitorHeightAndWidth
from src.phish.notification_email import NotificationFillTextToPhishing



>>>>>>> main:sweb/sweb.py

import sconf.configuration.configuration_provider as dataProvider
CONFIG_FILE_NAME = 'config.json'
SUBFOLDER_NAME = "sconf"

_dataProvider: dataProvider.ConfigurationProvider

# Library for sending mail to authorized people
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl


"""
# This class is used for notification to authorized people
# Whenever user ignore warning from connection to phishing web page
# And fill their information in
class NotificationFillTextToPhishing(QObject):
    @pyqtSlot(str)
    def receiveData(self, received_data):
        # Parse received JSON data to invidial data
        parsing_data = json.loads(received_data)
        input_text = parsing_data.get('value')
        connected_phishing_url = parsing_data.get('url')
        computer_username = getpass.getuser()
        computer_devicename = socket.gethostname()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Customize result 
        send_data = f'''*****Data received from sWEB when user filled text in phishing website*****
        - Device name: {computer_devicename}
        - User name: {computer_username}
        - Website: {connected_phishing_url}
        - Time: {current_time}
        - Filled text: {input_text}
        '''
        '''
        # Send received data to authorized people
        send_phishing_option = _dataProvider.get_sweb_configuration().sendPhishingWarning
        if send_phishing_option:
            self.send_email(send_data)
        else:
            return
        '''

     
    def send_email(self, message_to_receiver):
        # Load needed configuration from sweb_config in sconf for sending notification to authorized people
        ##receiver_mail = _dataProvider.get_smail_configuration().emailContacts[0]
        receiver_mail = "test@gmail.com"

        try:
            # Load the command line mail script
            command_line_mail_script = os.path.join(os.path.dirname(__file__), 'command_line_mail.py')
            with open(command_line_mail_script) as f:
                exec(f.read())
            print("Email sent successfully!!!")
        except Exception as excep:
            print(f"Error sending email: {excep}")
            # Log with level 2 - CRITICAL
            
 

# This class is used for customizing page on main browser
class MyWebEnginePage(QWebEnginePage):
    # Define a signal that will carry a URL as its argument
    urlChangedSignal = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create a channel for recording filling text when user fill text in phishing page
        self.channel = QWebChannel(self)
        self.setWebChannel(self.channel)
        
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        # Ensure only modifying behavior for clicked links
        if _type == QWebEnginePage.NavigationTypeLinkClicked and isMainFrame:
            # Navigate to the url
            self.urlChangedSignal.emit(url)
            # Tell the view that handled this navigation request
            return False
        # Return True for all other navigation requests
        return True

    def createWindow(self, _type):
        # Create a new instance of MyWebEnginePage for the new window request
        new_page = MyWebEnginePage(self)
        new_page.urlChangedSignal.connect(self.urlChangedSignal.emit)
        return new_page
    
    # Method for configuration in Mobile user agent
    def setUserAgent(self, user_agent):
        self.profile().setHttpUserAgent(user_agent)


"""  
        
    

    
# Define main function to call application
def main():
    current_location = os.getcwd()
    path_split = current_location.split("sweb")
    config_folder = os.path.join(path_split[0], SUBFOLDER_NAME)
    global _dataProvider
    _dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)
    try:
        
        qApplication = QApplication(sys.argv)
        # If browser is opened in command terminal
        input_url_from_terminal = sys.argv[1] if len(sys.argv) > 1 else "https://vut.cz"
        # Load config data from JSON file
        main_window = MyBrowser(input_url_from_terminal,_dataProvider.get_sweb_configuration()) # Set parametr for main browser window
        main_window.resize(1700, 1100)
        main_window.show() 
        main_window.show_app_full_screen() # Call main browser window, this set the full screen.
        sys.exit(qApplication.exec_())
    except Exception as excep:
        print(f"Error: {excep}")
        print("Detailed traceback:")
        traceback.print_exc()
        sys.exit(1)
    

if __name__ == "__main__":
   main() 
    
   
