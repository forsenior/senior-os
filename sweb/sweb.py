# Frameworks from PyQt5 libraries
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout
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
from screeninfo import get_monitors
# Created own class for logging and blocking phishing URL
from antiPhishing.URLBlocker import URLBlocker
from antiPhishing.URLLogger import URLLogger
from antiPhishing.UpdatePhishingTXT import PhishingDatabaseModificationChecker
from loadConfig import *
# Own class for translating
from languge_Translator import Translator
import math
#import pygame
import sys, os, json, getpass, socket
from datetime import datetime

# Library for sending mail to authorized people
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

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
        # Send received data to authorized people
         ##Tarik
        ''' 
        my_config_data = load_sweb_config_json()
        send_phishing_option = my_config_data["advanced_against_phishing"]["send_phishing_warning"]
        if "enable" in send_phishing_option:
            self.send_email(send_data)
        else:
            return
        ''' 
    ##Tarik, This function no need to be used, because there are another way to send email.
    '''   
    def send_email(self, message_to_receiver):
        # Load needed configuration from sweb_config in sconf for sending notification to authorized people
        sender_mail = sweb_config["credentials"]["sender_mail"]
        sender_password = sweb_config["credentials"]["sender_password"]
        receiver_mail = sweb_config["credentials"]["receiver_mail"]
        subject = sweb_config["credentials"]["subject"]
        smtp_server = sweb_config["credentials"]["smpt_server"]
        smtp_port = sweb_config["credentials"]["smtp_port"]
        
        # Convert information to block with multi parts
        message_block = MIMEMultipart()
        message_block['From'] = sender_mail
        message_block['To'] = receiver_mail
        message_block['Subject'] = subject
        message_block.attach(MIMEText(message_to_receiver, 'plain'))

        ssl_context = ssl.create_default_context()
        try:
            # Definition smtp server
            smtp_server = smtplib.SMTP(smtp_server, smtp_port)
            smtp_server.ehlo()
            # Starting connection to smtp server using name and port
            smtp_server.starttls(context=ssl_context) 
            smtp_server.ehlo()
            # Log in to mail server using username and password (Password is not login password, it is created from 2-Oauth gmail for third party)
            smtp_server.login(sender_mail, sender_password)
            text = message_block.as_string()
            # Send message to the smtp server
            smtp_server.sendmail(sender_mail, receiver_mail, text)
            # Close smtp connection
            smtp_server.quit()
            print("Email sent successfully!!!")
        except Exception as excep:
            url_logger = URLLogger()
            # Log with level 2 - CRITICAL
            url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Not success to sending user filling text from phishing webpage to Authorized people')
    ''' 

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
    
# This class is used for detecting and calculating user monitor
##Tarik, this class is used for getting the height and width of the monitor
class GetMonitorHeightAndWidth:
    def __init__(self):
        template_config = load_sweb_config_json()
        num_of_monitor = template_config["template"]["numOfScreen"]
        padding = template_config["template"]["padx_value"]
        height_divisor = template_config["template"]["height_divisor"]
        width_divisor = template_config["template"]["width_divisor"]
        num_option_on_frame = template_config["template"]["num_of_opt_on_frame"]
        # Get monitor size
        # 0 = Get the first monitor
        monitor = get_monitors()[num_of_monitor]
        screen_width, screen_height = monitor.width, monitor.height
        self.button_height = screen_height / height_divisor
        # Number of button on menu = numberOfOptions + 1
        total_padding = (num_option_on_frame)*padding
        # Calculate width for button
        self.button_width = math.floor((screen_width-total_padding)/width_divisor) - padding
    
    def get_height_button(self):
        return self.button_height
    
    def get_width_button(self):
        return self.button_width
    
# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self,my_config_data, input_url):
        super(MyBrowser,self).__init__()
        # Set window flags to customize window behavior
        # Remove standard window controls
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.main_browser = QWebEngineView()
        # Set cutstom page to open new page in the same browser
        self.my_custom_page = MyWebEnginePage(self.main_browser)
        self.my_custom_page.urlChangedSignal.connect(self.on_url_changed_my_custom_page)
        # Configuration for open in Mobile
        # Value for mobile user agent
        mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        #self.my_custom_page.setUserAgent(mobile_user_agent)
        # Add my custom page to browser
        self.main_browser.setPage(self.my_custom_page)
        self.setCentralWidget(self.main_browser)
        # Default page is configured as vut.cz
        # Check if input URL is contained HTTP or HTTPS
        if input_url.startswith("https") or input_url.startswith("http"):
            self.main_browser.setUrl(QUrl(input_url))
        else:
            self.main_browser.setUrl(QUrl("http://" + input_url))
        # Parameter for changging language on application
        self.language_translator = Translator()
        # Parameter for getting monitor heigght ad width
        self.get_monitor_height_and_width = GetMonitorHeightAndWidth()
        # Create notification when connection and input text to phishing page
        self.notification_fill_text = NotificationFillTextToPhishing()
        self.my_custom_page.channel.registerObject("notification_fill_text",self.notification_fill_text)
        # Load URL blocker and logger
        self.data_in_my_config_data = my_config_data
        path_to_phishing_database = my_config_data["phishing_database"]["path"]
        self.url_blocker = URLBlocker(path_to_phishing_database)
        self.url_logger = URLLogger()
        
        # Check if phishing database is up to date
        phishing_database_check_update = PhishingDatabaseModificationChecker(my_config_data,self.url_logger)
        phishing_database_check_update.check_and_update_if_needed()
        
        # Initialization pygame mixer  for play sounds
        ##pygame.mixer.init()
        # Sound control attribute
        self.sound_mixer_control_for_button = None
        
        ##Tarik, remove the sound
        #self.path_to_alert_phishing_music = my_config_data["audio"]["sweb_cz_alert_phishing"]
        #self.path_to_url_music = my_config_data["audio"]["sweb_cz_url"]
        
        # Get parameter from file sconf/TEMPLATE.json
        self.font_family_info = my_config_data["template"]["fontFamily"]
        self.font_size_info = my_config_data["template"]["fontSize"]
        self.font_weight_info = my_config_data["template"]["fontThickness"]
        self.button_value_padd_info = my_config_data["template"]["padx_value"]
        self.time_hover_button = my_config_data["template"]["soundDelay"] * 1000
        
        # Get height and width from class GetHeightAndWidthInfo
        self.buttons_width_info = self.get_monitor_height_and_width.get_width_button()
        self.buttons_height_info = self.get_monitor_height_and_width.get_height_button()
        
        # Get my parametr from file
        self.color_info_menu = my_config_data["colors_info"]["menu_frame"]
        self.color_info_app = my_config_data["colors_info"]["app_frame"]
        self.color_info_button_unselected = my_config_data["colors_info"]["buttons_unselected"]
        self.color_info_button_selected = my_config_data["colors_info"]["buttons_selected"]
        
        # Get path for images
        self.path_to_image_exit = my_config_data["image"]["sweb_image_exit"]
        self.path_to_image_www1 = my_config_data["image"]["sweb_image_www1"]
        self.path_to_image_www2 = my_config_data["image"]["sweb_image_www2"]
        self.path_to_image_www3 = my_config_data["image"]["sweb_image_www3"]
        self.path_to_image_www4 = my_config_data["image"]["sweb_image_www4"]
        self.path_to_image_www5 = my_config_data["image"]["sweb_image_www5"]
        
        # Create a toolbar for saving menu and buttons

        self.menu_1_toolbar = QToolBar("Menu 1")
        self.addToolBar(self.menu_1_toolbar)
        self.menu_1_toolbar.setMovable(False)
        self.menu_1_toolbar.setFixedSize(1850, 220)
        
        ##Tarik, set the bar in the middle.
        '''
        # Add a spacer to the left of the toolbar
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.menu_1_toolbar.addWidget(left_spacer)

        # Add the buttons to the toolbar
        self.setup_initial_menu_1()

        # Add a spacer to the right of the toolbar
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.menu_1_toolbar.addWidget(right_spacer)
        '''
        #Tarik, set the bar in thh middle.
        # Add a spacer to the left of the toolbar
        #left_spacer = QWidget()
        #left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.menu_1_toolbar.addWidget(left_spacer)
        self.permitted_website_list = load_permitted_website_from_sgive(self.data_in_my_config_data)
        

        # Create a toolbar for saving menu and buttons
        self.menu_2_toolbar = QToolBar("Menu 2")
        self.addToolBar(self.menu_2_toolbar)
        self.menu_2_toolbar.setMovable(False)
        self.menu_2_toolbar.setFixedSize(1850, 220)
        
        self.addToolBarBreak()
        
        self.toolbar_space = QToolBar("Spacer")
        # Set the spacer height
        self.toolbar_space.setFixedHeight(int(self.buttons_height_info))
        self.toolbar_space.setStyleSheet(f"""
        QToolBar {{
                background-color: #fff;
        }}
        """)
        self.addToolBar(self.toolbar_space)
        self.toolbar_space.setMovable(False)
        self.toolbar_space.setVisible(False)
        self.addToolBarBreak()
        
        # Set a style for Menu 1 toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for Menu 1 toolbar
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Get number of menu and number of options in the menu from sconf/config.json
        num_menu_buttons = my_config_data['template']['num_of_menu_buttons']
        num_of_opt_on_menu = my_config_data['template']['num_of_opt_on_frame']

        if num_menu_buttons == 2 and num_of_opt_on_menu == 4:
            self.setup_initial_menu_1()
            self.setup_initial_menu_2()
        else:
            self.close()
            
        # Set disvisible for menu 2
        self.menu_2_toolbar.setVisible(False)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.url_toolbar.setMovable(False)
        
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QToolBar {{
                background-color: {self.color_info_menu};
        }}
        QLineEdit {{
            border: 2px solid black;
            height: {self.buttons_height_info}px;
            font-family: {self.font_family_info};
            font-size: {int(self.buttons_height_info/3)}px;
            font-weight: {self.font_weight_info};
            background-color: {self.color_info_app};         
        }}        
        """)
        
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_toolbar.addWidget(self.url_bar)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)
        # Parameter for toggle phishing
        self.toggle_phishing_webpage = False
        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.update_ui_text()
        ##Tarik
        #self.update_ui_audio()
        self.main_browser.urlChanged.connect(self.security_against_phishing)
        # Apply changing text after finishing load
        #self.main_browser.loadFinished.connect(self.finished_load_web_page)
    
    def on_url_changed_my_custom_page(self, url):
        # Load the new URL in the existing browser window
        self.main_browser.setUrl(url)
        
    def setup_initial_menu_1(self):
        # Create first Menu
        self.menu1_button = QPushButton(self)
        self.menu1_button.setFixedSize(360, 210) # Set size to 360x210
        # Create Menu QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        self.menu1_new_text_label = QLabel("Menu 1", self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_new_text_label)
        # Align text in the center
        menu1_news_layout.setAlignment(self.menu1_new_text_label, Qt.AlignCenter)

        # Set font color for menu1
        font_color = self.data_in_my_config_data["template"]["fontcolor"]
        self.menu1_new_text_label.setStyleSheet(f"color: {font_color};")


        menu1_news_layout.setAlignment(self.menu1_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_1_toolbar.addWidget(self.menu1_button)
        
        # Add a bliak space between two button
        spacer1 = QWidget()
        spacer1.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer1)

        # Add Exit button
        self.menu1Exit = QPushButton(self)
        self.menu1Exit.setFixedSize(360, 210)  # Set size to 360x210
        # Create Home QvBoxLayout
        menu1Exit_layout = QVBoxLayout(self.menu1Exit)
        # Set Icon for Exit
        menu1Exit_icon = QIcon(self.path_to_image_exit)
        menu1Exit_label = QLabel(self.menu1Exit)
        menu1Exit_label.setPixmap(menu1Exit_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu1Exit_layout.addWidget(menu1Exit_label)
        # Align text and icon in the center
        menu1Exit_layout.setAlignment(menu1Exit_label,Qt.AlignCenter)
        self.menu1Exit.clicked.connect(self.close)
        self.menu1Exit.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1Exit)
        
        # Add a bliak space between two button
        spacer2 = QWidget()
        spacer2.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer2)
        
        # Add back button
        self.back_btn = QPushButton(self)
        self.back_btn.setFixedSize(360, 210)  # Set size to 360x210
        back_layout = QVBoxLayout(self.back_btn)
        # Set icon for Language
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        back_label = QLabel(self.back_btn)
        back_label.setPixmap(back_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        back_layout.addWidget(back_label)
        # Change to hand when click cursor
        self.back_btn.setCursor(Qt.PointingHandCursor)
        # Align text and icon in the center
        back_layout.setAlignment(back_label,Qt.AlignCenter)
        self.back_btn.clicked.connect(self.main_browser.back)
        self.menu_1_toolbar.addWidget(self.back_btn)
        
         # Add a blank space between two button
        spacer3 = QWidget()
        spacer3.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer3)
        
        # Add Menu1_WWW1 button
        self.menu1WWW1 = QPushButton(self)
        self.menu1WWW1.setFixedSize(360, 210)  # Set size to 360x210
        menu1WWW1_layout = QVBoxLayout(self.menu1WWW1)
        # Icon for Ceska televize
        menu1WWW1_icon = QIcon(self.path_to_image_www1)
        menu1WWW1_label = QLabel(self.menu1WWW1)
        menu1WWW1_label.setPixmap(menu1WWW1_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu1WWW1_layout.addWidget(menu1WWW1_label)
        # Align icon in the center
        menu1WWW1_layout.setAlignment(menu1WWW1_label,Qt.AlignCenter)
        self.menu1WWW1.clicked.connect(self.navigate_www1)
        self.menu1WWW1.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW1)
        
        # Add a blank space between two button
        spacer4 = QWidget()
        spacer4.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer4)
        
        # Add Menu1_WWW2 button
        self.menu1WWW2 = QPushButton(self)
        self.menu1WWW2.setFixedSize(360, 210)  # Set size to 360x210
        menu1WWW2_layout = QVBoxLayout(self.menu1WWW2)
        # Icon for Irozhlas
        menu1WWW2_icon = QIcon(self.path_to_image_www2)
        menu1WWW2_label = QLabel(self.menu1WWW2)
        menu1WWW2_label.setPixmap(menu1WWW2_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu1WWW2_layout.addWidget(menu1WWW2_label)
        # Align icon in the center
        menu1WWW2_layout.setAlignment(menu1WWW2_label,Qt.AlignCenter)
        self.menu1WWW2.clicked.connect(self.navigate_www2)
        self.menu1WWW2.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW2)
        

    def setup_initial_menu_2(self):
        # Create second Menu2
        self.menu2_button = QPushButton(self)
        self.menu2_button.setFixedSize(360, 210) # Set size to 360x210
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        self.menu2_new_text_label = QLabel("Menu 2", self.menu2_button)
        menu2_news_layout.addWidget(self.menu2_new_text_label)
        # Align text and icon in the center
        menu2_news_layout.setAlignment(self.menu2_new_text_label,Qt.AlignCenter)
        # Set font color for menu2
        font_color = self.data_in_my_config_data["template"]["fontcolor"]
        self.menu2_new_text_label.setStyleSheet(f"color: {font_color};")
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        # Show menu 2 when clicked
        self.menu2_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_2_toolbar.addWidget(self.menu2_button)

        
        # Add a bliak space between two button
        spacer5 = QWidget()
        spacer5.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer5)
        
        # Add Menu2_WWW3 button
        self.menu2WWW3 = QPushButton(self)
        self.menu2WWW3.setFixedSize(360, 210) # Set size to 360x210
        menu2WWW3_layout = QVBoxLayout(self.menu2WWW3)
        # Icon for idnes
        menu2WWW3_icon = QIcon(self.path_to_image_www3)
        menu2WWW3_label = QLabel(self.menu2WWW3)
        menu2WWW3_label.setPixmap(menu2WWW3_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu2WWW3_layout.addWidget(menu2WWW3_label)
        # Align text and icon in the center
        menu2WWW3_layout.setAlignment(menu2WWW3_label,Qt.AlignCenter)
        self.menu2WWW3.clicked.connect(self.navigate_www3)
        self.menu2WWW3.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW3)
        
        # Add a bliak space between two button
        spacer6 = QWidget()
        spacer6.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer6)
        
        # Add Menu2_WWW4 button
        self.menu2WWW4 = QPushButton(self)
        self.menu2WWW4.setFixedSize(360, 210) # Set size to 360x210
        menu2WWW4_layout = QVBoxLayout(self.menu2WWW4)
        # Icon for aktualne.cz
        menu2WWW4_icon = QIcon(self.path_to_image_www4)
        menu2WWW4_label = QLabel(self.menu2WWW4)
        menu2WWW4_label.setPixmap(menu2WWW4_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu2WWW4_layout.addWidget(menu2WWW4_label)
        # Align text and icon in the center
        menu2WWW4_layout.setAlignment(menu2WWW4_label,Qt.AlignCenter)
        self.menu2WWW4.clicked.connect(self.navigate_www4)
        self.menu2WWW4.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW4)
        
        # Add a bliak space between two button
        spacer7 = QWidget()
        spacer7.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer7)
        
        # Add Menu2_WWW5 button
        self.menu2WWW5 = QPushButton(self)
        self.menu2WWW5.setFixedSize(360, 210) # Set size to 360x210
        menu2WWW5_layout = QVBoxLayout(self.menu2WWW5)
        # Icon for denik.cz
        menu2WWW5_icon = QIcon(self.path_to_image_www5)
        menu2WWW5_label = QLabel(self.menu2WWW5)
        menu2WWW5_label.setPixmap(menu2WWW5_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        menu2WWW5_layout.addWidget(menu2WWW5_label)
        # Align text and icon in the center
        menu2WWW5_layout.setAlignment(menu2WWW5_label,Qt.AlignCenter)
        self.menu2WWW5.clicked.connect(self.navigate_www5)
        self.menu2WWW5.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW5)
        
        # Add a bliak space between two button
        spacer8 = QWidget()
        spacer8.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer8)
        
        # Add Menu2_Address button
        self.menu2Address = QPushButton(self)
        self.menu2Address.setFixedSize(360, 210) # Set size to 360x210
        # Create Home QvBoxLayout
        menu2Address_layout = QVBoxLayout(self.menu2Address)
        self.menu2_addres_new_text_label = QLabel("My page", self.menu2_button)
        self.menu2Address.setStyleSheet(f"color: {font_color};")
        #self.menu2_addres_new_text_label.setWordWrap(True)
        self.menu2_addres_new_text_label.setAlignment(Qt.AlignCenter)
        menu2Address_layout.addWidget(self.menu2_addres_new_text_label)
        # Align text and icon in the center
        menu2Address_layout.setAlignment(self.menu2_addres_new_text_label,Qt.AlignCenter)
        self.menu2Address.clicked.connect(self.toggle_url_toolbar)
        self.menu2Address.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2Address)
        
    
    # Set default style for Toolbar
    def default_style_toolbar(self):
        style_string = f"""
            QToolBar {{
                background-color: {self.color_info_menu};
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border: 1px solid black;
                background-color: {self.color_info_button_unselected};                   
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
                width: {self.buttons_width_info}px;
                height: {self.buttons_height_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {self.color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
            }}
        """
        
        return style_string
    
    # Set default style for Toolbar
    def phishing_style_toolbar(self):
        alert_style_string = f"""
             QToolBar {{
                background-color: {self.color_info_menu};
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border: 1px solid black;
                background-color: red;                   
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
                width: {self.buttons_width_info}px;
                height: {self.buttons_height_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {self.color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
            }}
        """
        
        return alert_style_string
    
    # This method control HTML injection to web page
    # Function: Zoom in, block input text and zoom text
    def finished_load_web_page(self):
        # Get url value from browser
        url_in_browser_value = self.main_browser.url().toString()
        senior_website_posting_option = self.data_in_my_config_data["advanced_against_phishing"]["senior_website_posting"]
        
        # Get permitted websites list from sgive
        permitted_website_list = self.permitted_website_list
        # Check if it is permitted website
        check_result = any(permitted_website in url_in_browser_value for permitted_website in permitted_website_list)
        if check_result:
            if "homepage.html" not in url_in_browser_value:
                self.main_browser.setZoomFactor(1.1)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content())
        elif self.toggle_phishing_webpage:
            self.main_browser.setZoomFactor(1.1)
            # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
            QTimer.singleShot(250, lambda: self.html_injection_to_phishing_web_content())
        else:
            if "enable" in senior_website_posting_option:
                self.main_browser.setZoomFactor(1.1)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content_strict())
            else:
                return
            
    # This method is applied for connection to phishing web page
    def html_injection_to_phishing_web_content(self):
        injection_javasript = """
        var script = document.createElement('script');
        <!-- Define and call script qtwebchannel-->
        script.src = 'qrc:///qtwebchannel/qwebchannel.js';
        script.onload = function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.notification_fill_text = channel.objects.notification_fill_text;
                <!-- Elements for capturing text are defined HERE!!!-->
                document.querySelectorAll('input[type="text"], input[type="email"], input[type="search"], input[type="password"], input[type="tel"], input[type="url"],input[enterkeyhint="search"], textarea').forEach(function(element) {
                    element.addEventListener('change', function() {
                        <!-- Define data with two parameter: one for saved text, one for url-->
                        var data = {value: element.value, url: window.location.href};
                        <!-- Parse text to channel in type of JSON text-->
                        window.notification_fill_text.receiveData(JSON.stringify(data));
                    });
                });
            });
        };
        document.head.appendChild(script);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # This method is used for changing font in HTML content
    def html_injection_to_web_content(self):
        injection_javasript = """
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var all_changed_content_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            <!-- Method includes will return value in UPPERCASE>
            if (['H3', 'H4', 'H5', 'A'].includes(element.tagName)) {
                <!-- Header with bigger size-->
                element.style.fontSize = '20px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '17px';
                element.style.lineHeight = '1.1';
            }
            Array.from(element.children).forEach(change_content_style);
        }
        change_content_style(document.body);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # This method is used for changing font and block input in HTML content
    # !!!Apply for not permiited website
    def html_injection_to_web_content_strict(self):
        injection_javasript = """
        <!-- Declare tags for prohibiting input text to textfill-->
        var prohibited_tag_input = document.querySelectorAll('input, textarea, div.input');
        <!-- Disable input field in webpage-->
        prohibited_tag_input.forEach(function(input) {
            <!-- True == input value is disabled-->
            input.disabled = true;
        });
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var all_changed_content_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            <!-- Method includes will return value in UPPERCASE>
            if (['H3', 'H4', 'H5', 'A'].includes(element.tagName)) {
                <!-- Header with bigger size-->
                element.style.fontSize = '20px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '17px';
                element.style.lineHeight = '1.1';
            }
            Array.from(element.children).forEach(change_content_style);
        }
        change_content_style(document.body);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # Show full screen without Minimizing or Moving
    def show_app_full_screen(self):
        self.showFullScreen()
        
    # Method use for disable menu when click to another menu
    def toggle_between_toolbar(self):
        # Toggle visibility of toolbars
        if self.menu_1_toolbar.isVisible():
            self.menu_1_toolbar.setVisible(False)
            self.menu_2_toolbar.setVisible(True)
        else:
            self.menu_2_toolbar.setVisible(False)
            self.menu_1_toolbar.setVisible(True)
        
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    def toggle_supported_language(self):
        self.language_translator.toggle_supported_language()
        self.update_ui_text()
        ##Tarik
        #self.update_ui_audio()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_text(self):
            self.menu1_new_text_label.setText(self.language_translator.get_translated_text("menu1"))
            self.menu2_new_text_label.setText(self.language_translator.get_translated_text("menu2"))
            self.menu2_addres_new_text_label.setText(self.language_translator.get_translated_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    '''Tarik
    def update_ui_audio(self):
            self.setup_hover_sound_value(self.menu1_button,self.time_hover_button,self.language_translator.get_translated_audio("menu1"))
            self.setup_hover_sound_value(self.menu1Exit,self.time_hover_button,self.language_translator.get_translated_audio("menu1Exit"))
            self.setup_hover_sound_value(self.back_btn,self.time_hover_button,self.language_translator.get_translated_audio("menu1Back"))
            self.setup_hover_sound_value(self.menu1WWW1,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW1"))
            self.setup_hover_sound_value(self.menu1WWW2,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW2"))
            self.setup_hover_sound_value(self.menu2_button,self.time_hover_button,self.language_translator.get_translated_audio("menu2"))
            self.setup_hover_sound_value(self.menu2WWW3,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW3"))
            self.setup_hover_sound_value(self.menu2WWW4,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW4"))
            self.setup_hover_sound_value(self.menu2WWW5,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW5"))
            self.setup_hover_sound_value(self.menu2Address,self.time_hover_button,self.language_translator.get_translated_audio("menu2Address"))
            self.path_to_alert_phishing_music = self.language_translator.get_translated_audio("alert_phishing")
            self.path_to_url_music = self.language_translator.get_translated_audio("url")
    '''
    # QpushButton can be set HoverLeave and HoverEnter event with "widget"
    # Play sound when usesr hovers on button longer than 5 seconds
    '''Tarik
    def setup_hover_sound_value(self, input_widget, hover_time,path_to_sound):
        # Using Qtimer to set clock
        input_widget.hover_timer = QTimer()
        input_widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        input_widget.hover_timer.setSingleShot(True)
        input_widget.hover_timer.timeout.connect(lambda: self.play_sound_for_button(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        input_widget.installEventFilter(self)
    '''
    # Set event for leave and enter button -> Using only with QpushButton
    def eventFilter(self, watched, event):
        if event.type() == QEvent.HoverEnter:
            watched.hover_timer.start()
        elif event.type() == QEvent.HoverLeave:
            watched.hover_timer.stop()
            # Stop sound immediately
            self.stop_sound_for_button()
        return super().eventFilter(watched, event)
    
    # Play a sound, which is stored on SWEB_config.json
    #My comment
    '''

    def play_sound_for_button(self, path_to_sound):
        # Ensure the file exists before playing it
        if not os.path.exists(path_to_sound):
            print(f"Sound file not found: {path_to_sound}")
            return
        try:
            # Load and play the sound file
            self.sound_mixer_control_for_button = pygame.mixer.Sound(path_to_sound)
            self.sound_mixer_control_for_button.play()
        except Exception as exc:
            print(f"Failed to play sound: {str(exc)}")
    '''   
    # Stop sound immediately when button is leaved hover
    def stop_sound_for_button(self):
        if self.sound_mixer_control_for_button:
            self.sound_mixer_control_for_button.stop()
            self.sound_mixer_control_for_button = None
        
    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        # Toggle visibility of the URL toolbar
        ##Tarik comment
        # self.play_sound_for_button(self.path_to_url_music)
        self.main_browser.setUrl(QUrl("about:blank"))
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())
        self.toolbar_space.setVisible(not self.toolbar_space.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        # Get url from URL toobal
        url_in_bar_value = self.url_bar.text().strip()
        #If "." is not contained in URL
        if "." not in url_in_bar_value:
            url_in_bar_value = "https://www.google.com/search?q=" + url_in_bar_value
        # If in URl not http or https, connect with HTTPS
        if "://" not in url_in_bar_value:
            url_in_bar_value = "https://" + url_in_bar_value
        
        # Set default style for toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
          
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        # Set url bar as clean
        self.url_bar.clear()
        # Connect to URL after entering
        self.main_browser.setUrl(QUrl(url_in_bar_value))
    
    # Method for security against phishing    
    def security_against_phishing(self,qurl):
        # Get url from QURL
        url_in_browser_value = qurl.toString()
        if url_in_browser_value.endswith('/'):
            if self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                ##Tarik comment
                ##self.play_sound_for_button(self.path_to_alert_phishing_music)
                 # Log with level 5 when connected to phishing
                self.url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser_value}')
                    
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                self.toggle_phishing_webpage = False
                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with LEVEL 6 INFORMATIONAL
                self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
        elif not url_in_browser_value.endswith('/'):
            if "about:blank" in url_in_browser_value:
                self.toggle_phishing_webpage = False
                return
            #elif "google.com" in url_in_browser_value:
                #self.toggle_phishing_webpage = False
                #self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                #self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with level 6 INFORMATIONAL
                #self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
                # Connect to URL after entering
                #self.main_browser.setUrl(QUrl(url_in_browser_value))
            elif self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                ## My comment
                ##self.play_sound_for_button(self.path_to_alert_phishing_music)
                # Log with level 5 when connected to phishing
                self.url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser_value}')
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                self.toggle_phishing_webpage = False
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with LEVEL 6 INFORMATIONAL
                self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
        self.main_browser.loadFinished.connect(self.finished_load_web_page)
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www1(self):
        self.main_browser.setUrl(QUrl("https://edition.cnn.com"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        
    # Method for connect to the irozhlas.cz
    def navigate_www2(self):
        self.main_browser.setUrl(QUrl("https://irozhlas.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the idnes.cz
    def navigate_www3(self):
        # Define the Home Page for the Web Browser
        # !!! using .html but still don't have good Home Page
        #html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        #self.main_browser.load(QUrl.fromLocalFile(html_path))
        # Connect to google.com
        self.main_browser.setUrl(QUrl("https://google.com"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())

    # Method for connect to the aktualne.cz
    def navigate_www4(self):
        self.main_browser.setUrl(QUrl("https://www.aktualne.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the denik.cz
    def navigate_www5(self):
        self.main_browser.setUrl(QUrl("https://www.denik.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
    
# Define main function to call application
if __name__ == "__main__":
    try:
        qApplication = QApplication(sys.argv)
        # If browser is opened in command terminal
        input_url_from_terminal = sys.argv[1] if len(sys.argv) > 1 else "https://vut.cz"
        # Load config data from JSON file
        sweb_config = load_sweb_config_json()
        main_window = MyBrowser(sweb_config, input_url_from_terminal) # Set parametr for main browser window
        ##Tarik
        main_window.resize(1700, 1100)
        main_window.show() 
        #main_window.show_app_full_screen() # Call main browser window, this set the full screen.
        sys.exit(qApplication.exec_())
    except Exception as excep:
        url_logger = URLLogger()
        # Log with level 2 - CRITICAL
        url_logger.log_blocked_url('WEBBROWSER', 2, 'main <security>', f'Application did not work')
        # Exit with an error code
        sys.exit(1)
