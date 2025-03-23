
# Frameworks from PyQt5 libraries
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QToolBar, QWidget

from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy
# Library for creating channel for monitoring input keyboard
from PyQt5.QtWebChannel import QWebChannel

from sweb.utils.url_blocker import URLBlocker
from sweb.phish.update_phishing import PhishingDatabaseModificationChecker
from sweb.language.language_translator import Translator
from sweb.utils.monitor_provider import GetMonitorHeightAndWidth
from sweb.phish.notification_email import NotificationFillTextToPhishing
from sweb.browser.browser_core import MyWebEnginePage
import os
# Set QT Environment Variables
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
Debug = False
## static size of the button
BUTTON_WIDTH = 238
BUTTON_HEIGHT = 107
BUTTON_SPACE = 10
BUTTON_NUMBER = 5


# static size of the toolbar
TOOLBAR_WIDTH = BUTTON_WIDTH * BUTTON_NUMBER + BUTTON_SPACE * (BUTTON_NUMBER + 1) + 80


class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self, input_url, sweb_dataProvider, global_dataProvider):
        super(MyBrowser,self).__init__()

        self.sweb_dataProvider = sweb_dataProvider
        self.global_dataProvider = global_dataProvider

        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.main_browser = QWebEngineView()
        # Set cutstom page to open new page in the same browser
        self.my_custom_page = MyWebEnginePage(self.main_browser)
        
        self.my_custom_page.urlChangedSignal.connect(self.on_url_changed_my_custom_page)
        # Configuration for open in Mobile
        # Value for mobile user agent
        mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        self.my_custom_page.setUserAgent(mobile_user_agent)
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
        self.language_translator = Translator(sweb_dataProvider, global_dataProvider)
        # Parameter for getting monitor heigght ad width
        self.get_monitor_height_and_width = GetMonitorHeightAndWidth()
        # Create notification when connection and input text to phishing page
        self.notification_fill_text = NotificationFillTextToPhishing(self.sweb_dataProvider.command_line_mail_script, self.global_dataProvider.careGiverEmail)
        self.my_custom_page.channel.registerObject("notification_fill_text",self.notification_fill_text)
        self.url_blocker = URLBlocker(sweb_dataProvider.phishingDatabase,sweb_dataProvider.allowedURL)
        # Check if phishing database is up to date
        phishing_database_check_update = PhishingDatabaseModificationChecker(sweb_dataProvider)
        phishing_database_check_update.check_and_update_if_needed()
        

        self.buttons_width_info = BUTTON_WIDTH

        self.buttons_height_info = BUTTON_HEIGHT      
        # Get my parametr from file
        self.color_info_menu = "#e5e5e5"
        self.color_info_app = "#FFFFFF"
        
        
        # Get path for images
        for entry in self.sweb_dataProvider.swebAllowedUrlListV2:
            for key, value in entry.items():
                if key.startswith("url"):
                    setattr(self, f"url_www{key[-1]}", value)
                elif key.startswith("icon"):
                    setattr(self, f"path_to_image_www{key[-1]}", value)

        self.path_to_image_exit = sweb_dataProvider.picturePaths[0]

        if Debug:
            print("Debugging MyBrowser")
            
            print("The websites URLs are: ")
            for i in range(1, 7):  # Loop from 1 to 6 (matching attribute numbering)
                print(f"URL {i} : {getattr(self, f'url_www{i}', 'N/A')}")

            print("The website icons are: ")
            print("Exit icon: ", self.path_to_image_exit)
            for i in range(1, 7):  # Loop from 1 to 6 to match the URLs
                print(f"Path {i} : {getattr(self, f'path_to_image_www{i}', 'N/A')}")
        


        # Load permitted websites from URLBlocker class
        self.permitted_website_list = self.url_blocker.load_permitted_website_from_sconf(sweb_dataProvider.allowedURL)

        # Create a toolbar for saving menu and buttons
        self.menu_1_toolbar = QToolBar("MENU 1")
        self.addToolBar(self.menu_1_toolbar)
        self.menu_1_toolbar.setMovable(False)
        # Calculate the left and right spacers to center the toolbar
        total_screen_width = self.get_monitor_height_and_width.get_width_screen()
        left_spacer_width = (total_screen_width - TOOLBAR_WIDTH) // 2

        left_spacer = QWidget()
        left_spacer.setFixedWidth(left_spacer_width)
        self.menu_1_toolbar.addWidget(left_spacer)

        
        # Create a toolbar for saving menu and buttons
        self.menu_2_toolbar = QToolBar("MENU 2")
        self.addToolBar(self.menu_2_toolbar)
        self.menu_2_toolbar.setMovable(False)
        total_screen_width = self.get_monitor_height_and_width.get_width_screen()
        left_spacer_width = (total_screen_width - TOOLBAR_WIDTH) // 2

        left_spacer = QWidget()
        left_spacer.setFixedWidth(left_spacer_width)
        self.menu_2_toolbar.addWidget(left_spacer)
        
       
        self.toolbar_space = QToolBar("Spacer")
        # Set the spacer height

        self.addToolBar(self.toolbar_space)
        self.toolbar_space.setMovable(False)
        self.toolbar_space.setVisible(False)
        self.addToolBarBreak()
        
        # Set a style for Menu 1 toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for Menu 2 toolbar
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for URL toolbar
        self.setup_initial_menu_1()
        self.setup_initial_menu_2()

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
            font-family: 'Inter';
            font-size: {int(self.buttons_height_info/3)}px;
            font-weight: 'Regular';
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

        
        spacer = QWidget()
        spacer.setFixedWidth(0)  # Set space before the first button
        self.menu_1_toolbar.addWidget(spacer)  # Add spacer to the toolbar
       
        # Create first Menu
        self.menu1_button = QPushButton(self)
        # Create Menu QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        self.menu1_new_text_label = QLabel("MENU 1", self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_new_text_label)
        # Align text in the center
        menu1_news_layout.setAlignment(self.menu1_new_text_label, Qt.AlignCenter)

        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_1_toolbar.addWidget(self.menu1_button)

        # Add Exit button
        self.menu1Exit = QPushButton(self)
        # Create Home QvBoxLayout
        menu1Exit_layout = QVBoxLayout(self.menu1Exit)
        # Set Icon for Exit
        menu1Exit_icon = QIcon(self.path_to_image_exit)
        menu1Exit_label = QLabel(self.menu1Exit)
        menu1Exit_label.setPixmap(menu1Exit_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1Exit_layout.addWidget(menu1Exit_label)
        # Align text and icon in the center
        menu1Exit_layout.setAlignment(menu1Exit_label,Qt.AlignCenter)
        self.menu1Exit.clicked.connect(self.close)
        self.menu1Exit.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1Exit)

        # Add Menu1_WWW1 button
        self.menu1WWW1 = QPushButton(self)
        menu1WWW1_layout = QVBoxLayout(self.menu1WWW1)
        # Icon for Ceska televize
        #menu1WWW1_icon = QIcon(_dataProvider.get_sweb_configuration().picturePaths[1])
        menu1WWW1_icon = QIcon(self.path_to_image_www1)
        menu1WWW1_label = QLabel(self.menu1WWW1)
        menu1WWW1_label.setPixmap(menu1WWW1_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW1_layout.addWidget(menu1WWW1_label)
        # Align icon in the center
        menu1WWW1_layout.setAlignment(menu1WWW1_label,Qt.AlignCenter)
        self.menu1WWW1.clicked.connect(self.navigate_www1)
        self.menu1WWW1.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW1)
        
       
        # Add Menu1_WWW2 button
        self.menu1WWW2 = QPushButton(self)
        menu1WWW2_layout = QVBoxLayout(self.menu1WWW2)
        # Icon for Irozhlas
        menu1WWW2_icon = QIcon(self.path_to_image_www2)
        menu1WWW2_label = QLabel(self.menu1WWW2)
        menu1WWW2_label.setPixmap(menu1WWW2_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW2_layout.addWidget(menu1WWW2_label)
        # Align icon in the center
        menu1WWW2_layout.setAlignment(menu1WWW2_label,Qt.AlignCenter)
        self.menu1WWW2.clicked.connect(self.navigate_www2)
        self.menu1WWW2.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW2)


        # Add Menu1_WWW3 button
        self.menu1_WWW3 = QPushButton(self)
        menu1WWW3_layout = QVBoxLayout(self.menu1_WWW3)
        # Icon for Ceska televize
        menu1WWW3_icon = QIcon(self.path_to_image_www3)
        menu1WWW3_label = QLabel(self.menu1_WWW3)
        menu1WWW3_label.setPixmap(menu1WWW3_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW3_layout.addWidget(menu1WWW3_label)
        # Align icon in the center
        menu1WWW3_layout.setAlignment(menu1WWW3_label,Qt.AlignCenter)
        self.menu1_WWW3.clicked.connect(self.navigate_www3)
        self.menu1_WWW3.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1_WWW3)
        
    

    def setup_initial_menu_2(self):
        """
        Sets up the initial configuration for the second menu, including buttons 
        for various web navigation and a search feature. Configures button 
        properties, layouts, icons, and click events.
        """
        # Calculate the left and right spacers to center the toolbar
        spacer = QWidget()
        spacer.setFixedWidth(0)  # Set space before the first button
        self.menu_2_toolbar.addWidget(spacer)  # Add spacer to the toolbar
       
     
        # Create second Menu2
        self.menu2_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        self.menu2_new_text_label = QLabel("MENU 2", self.menu2_button)
        
        menu2_news_layout.addWidget(self.menu2_new_text_label)
        # Set the font color for menu2
 
        # Align text and icon in the center
        menu2_news_layout.setAlignment(self.menu2_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        # Show menu 2 when clicked
        self.menu2_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_2_toolbar.addWidget(self.menu2_button)

        # Add Menu2_WWW4 button
        self.menu2WWW4 = QPushButton(self)
        menu2WWW4_layout = QVBoxLayout(self.menu2WWW4)
        # Icon for idnes
        menu2WWW4_icon = QIcon(self.path_to_image_www4)
        menu2WWW4_label = QLabel(self.menu2WWW4)
        menu2WWW4_label.setPixmap(menu2WWW4_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW4_layout.addWidget(menu2WWW4_label)
        # Align text and icon in the center
        menu2WWW4_layout.setAlignment(menu2WWW4_label,Qt.AlignCenter)
        self.menu2WWW4.clicked.connect(self.navigate_www4)
        self.menu2WWW4.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW4)

        # Add Menu2_WWW5 button
        self.menu2WWW5 = QPushButton(self)
        menu2WWW5_layout = QVBoxLayout(self.menu2WWW5)
        # Icon for aktualne.cz
        menu2WWW5_icon = QIcon(self.path_to_image_www5)
        menu2WWW5_label = QLabel(self.menu2WWW5)
        menu2WWW5_label.setPixmap(menu2WWW5_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW5_layout.addWidget(menu2WWW5_label)
        # Align text and icon in the center
        menu2WWW5_layout.setAlignment(menu2WWW5_label,Qt.AlignCenter)
        self.menu2WWW5.clicked.connect(self.navigate_www5)
        self.menu2WWW5.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW5)
        
        # Add Menu2_WWW6 button
        self.menu2WWW6 = QPushButton(self)
        menu2WWW6_layout = QVBoxLayout(self.menu2WWW6)
        # Icon for denik.cz
        menu2WWW6_icon = QIcon(self.path_to_image_www6)
        menu2WWW6_label = QLabel(self.menu2WWW6)
        menu2WWW6_label.setPixmap(menu2WWW6_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW6_layout.addWidget(menu2WWW6_label)
        # Align text and icon in the center
        menu2WWW6_layout.setAlignment(menu2WWW6_label,Qt.AlignCenter)
        self.menu2WWW6.clicked.connect(self.navigate_www6)
        self.menu2WWW6.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW6)
        
        # Add Menu2_Address button
        self.menu2Address = QPushButton(self)
        # Create Home QvBoxLayout
        menu2Address_layout = QVBoxLayout(self.menu2Address)
        self.menu2_addres_new_text_label = QLabel("Search", self.menu2_button)
        self.menu2_addres_new_text_label.setAlignment(Qt.AlignCenter)
        menu2Address_layout.addWidget(self.menu2_addres_new_text_label)
        # Align text and icon in the center
        menu2Address_layout.setAlignment(self.menu2_addres_new_text_label,Qt.AlignCenter)
        
        self.menu2Address.clicked.connect(self.toggle_url_toolbar)
        self.menu2Address.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2Address)
    
    def is_hex_color(self, value):
        """
        Checks if the given value is a valid hex color code.
        Args:
            value (str): The value to check.
        Returns:
            bool: True if the value is a valid hex color code, False otherwise.
        """
        if isinstance(value, str) and len(value) in (4, 7) and value.startswith('#'):
            hex_digits = '0123456789ABCDEFabcdef'
            return all(c in hex_digits for c in value[1:])
        return False
    


    # Set default style for Toolbar
    def default_style_toolbar(self):
        if self.is_hex_color(self.global_dataProvider.highlightColor):
            HIGHLIGHTCOLOR = self.global_dataProvider.highlightColor
        else:
            HIGHLIGHTCOLOR = "#48843F"

       ## toolbar_text_config = MenuBarTextConfiguration()

        style_string = f"""
            QToolBar {{    
            border: 0px solid transparent;
            background-color: transparent;
            spacing: 10px;
            }}
            QPushButton QLabel {{
                color: #FFFFFF;
            }}
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border-radius: 3px;
                border: 1px solid #797979;
                background-color: #949494 ; 
                margin: 20px 0px 20px 0px;                 
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Inter';
                width: {BUTTON_WIDTH}px;
                height: {BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHTCOLOR}; 
            }} 
            QPushButton QLabel {{
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Inter';
            }}
        """
        if Debug:
            print("The Default Style : ", style_string)

        return style_string
    
    # Set default style for Toolbar
    def phishing_style_toolbar(self):
        if self.is_hex_color(self.global_dataProvider.alertColor):
            ALERCOLOR = self.global_dataProvider.alertColor 
        else:
            ALERCOLOR = "#F90000" 
        if self.is_hex_color(self.global_dataProvider.highlightColor):
            HIGHLIGHTCOLOR = self.global_dataProvider.highlightColor
        else:
            HIGHLIGHTCOLOR = "#48843F"

        alert_style_string = f"""
            QToolBar {{
            border: 0px solid transparent;
            background-color: transparent;
            spacing: 10px;
            }}
            QPushButton QLabel {{
                color: #FFFFFF;
            }}
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border-radius: 3px;
                border: 1px solid #797979;
                background-color: {ALERCOLOR};   
                margin: 20px 0px 20px 0px;                 
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Inter';
                width: {BUTTON_WIDTH}px;
                height: {BUTTON_HEIGHT}px;      
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHTCOLOR}; 
            }}
            QPushButton QLabel {{
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Inter';
            }}
        """
        if Debug:
            print("The Alert Style: ", alert_style_string)
        
        return alert_style_string
    
    # This method control HTML injection to web page
    # Function: Zoom in, block input text and zoom text
    def finished_load_web_page(self):
        """
        Handles the completion of a web page load in the browser.
        This method performs the following actions:
        - Retrieves the current URL from the browser.
        - Checks if the URL is in the list of permitted websites.
        - Adjusts the zoom factor of the browser.
        - Injects HTML content based on the URL and configuration settings.
        """

        # Get url value from browser
        url_in_browser_value = self.main_browser.url().toString()
        #senior_website_posting_option = self.data_in_my_config_data["advanced_against_phishing"]["senior_website_posting"]

        senior_website_posting_option = self.sweb_dataProvider.seniorWebsitePosting
        
        # Get permitted websites list from sgive
        permitted_website_list = self.permitted_website_list
        # Check if it is permitted website
        check_result = any(permitted_website in url_in_browser_value for permitted_website in permitted_website_list)
        if check_result:
            if "homepage.html" not in url_in_browser_value:
                self.main_browser.setZoomFactor(0.9)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content())

        elif self.toggle_phishing_webpage:
            self.main_browser.setZoomFactor(0.9)
            # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
            QTimer.singleShot(250, lambda: self.html_injection_to_phishing_web_content())
        else:
            
            if senior_website_posting_option:
                self.main_browser.setZoomFactor(0.9)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content_strict())
            else:
                return
            
    # This method is applied for connection to phishing web page
    def html_injection_to_phishing_web_content(self):
        """
        Injects JavaScript into the web page to capture and send input field data to a Qt WebChannel.
        """

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
        def receiveData(self, data):
            print("Captured data:", data)
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # This method is used for changing font in HTML content
    def html_injection_to_web_content(self):
        """
        Injects JavaScript into the web content to modify the styles of specific HTML elements.
        The injected script targets paragraph, div, article, span, and header elements (h3, h4, h5)
        and adjusts their font size and line height based on their tag name.
        """
        injection_javasript = """
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var all_changed_content_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            <!-- Method includes will return value in UPPERCASE>
            if (['H3', 'H4', 'H5', 'A'].includes(element.tagName)) {
                <!-- Header with bigger size-->
                element.style.fontSize = '16px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '12px';
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
        """
        Injects JavaScript into the web page to disable input fields and 
        modify the style of specific HTML elements.
        """

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
                element.style.fontSize = '16px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '12px';
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
        """
        Toggles the visibility between two toolbars, menu_1_toolbar and menu_2_toolbar.
        """

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
        """
        Toggles the supported language in the language translator and updates the UI text.
        """

        self.language_translator.toggle_supported_language()
        self.update_ui_text()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_text(self):
            """
            Updates the UI text labels with translated text for menu items.
            """
            
            self.menu1_new_text_label.setText(self.language_translator.get_translated_text("menu1"))
            self.menu2_new_text_label.setText(self.language_translator.get_translated_text("menu2"))
            self.menu2_addres_new_text_label.setText(self.language_translator.get_translated_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    # Set event for leave and enter button -> Using only with QpushButton
    def eventFilter(self, watched, event):
        """
        Filters events for the watched object and handles hover events.
        Args:
            watched: The object being watched.
            event: The event being filtered.
        Returns:
            bool: True if the event should be filtered out, False otherwise.
        """

        if event.type() == QEvent.HoverEnter:
            watched.hover_timer.start()
        elif event.type() == QEvent.HoverLeave:
            watched.hover_timer.stop()
            # Stop sound immediately
            self.stop_sound_for_button()
        return super().eventFilter(watched, event)
    
    
    # Stop sound immediately when button is leaved hover
    ## TODO delete
    def stop_sound_for_button(self):
        if self.sound_mixer_control_for_button:
            self.sound_mixer_control_for_button.stop()
            self.sound_mixer_control_for_button = None
        
    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        """
        Toggles the visibility of the URL toolbar and the toolbar space in the main browser.
        """
        if self.global_dataProvider.protectionLevel != 3:
            self.main_browser.setUrl(QUrl("about:blank"))
            self.url_toolbar.setVisible(not self.url_toolbar.isVisible())
            self.toolbar_space.setVisible(not self.toolbar_space.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        """
        Navigates the browser to the URL entered in the URL bar. If the URL does not contain a dot,
        it performs a Google search. If the URL does not start with a scheme, it defaults to HTTPS.
        """

        # Get url from URL toobal
        url_in_bar_value = self.url_bar.text().strip()

        if self.global_dataProvider.protectionLevel == 2:
            web_url = self.url_blocker.find_url_with_value(url_in_bar_value)
            
            if web_url != "None":

                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                
                # Set visible after navitigation
                self.url_toolbar.setVisible(False)
                self.toolbar_space.setVisible(False)
                # Set url bar as clean
                self.url_bar.clear()
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(web_url)) 
            else:
                print("URL is not permitted")
                    
        else:
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
        """
        Checks the given URL for phishing threats and updates the browser's UI and logs accordingly.
        Parameters:
        qurl (QUrl): The URL to be checked for phishing threats.
        """
        # Get url from QURL
        url_in_browser_value = qurl.toString()
        if url_in_browser_value.endswith('/'):
            if self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True                   
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.notification_fill_text.send_email(url_in_browser_value)
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                self.toggle_phishing_webpage = False
                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
        elif not url_in_browser_value.endswith('/'):
            if "about:blank" in url_in_browser_value:
                self.toggle_phishing_webpage = False
                return
            elif "google.com" in url_in_browser_value:
                self.toggle_phishing_webpage = False
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))

            elif self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.notification_fill_text.send_email(url_in_browser_value)
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))

            else:
                self.toggle_phishing_webpage = False
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())

        self.main_browser.loadFinished.connect(self.finished_load_web_page)
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www1(self):
        self.main_browser.setUrl(QUrl(self.url_www1))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        
    # Method for connect to the irozhlas.cz
    def navigate_www2(self):
        self.main_browser.setUrl(QUrl(self.url_www2))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the vut.cz
    def navigate_www3(self):
        self.main_browser.setUrl(QUrl(self.url_www3))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
    # Method for connect to the idnes.cz
    def navigate_www4(self):
        self.main_browser.setUrl(QUrl(self.url_www4))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)



    # Method for connect to the aktualne.cz
    def navigate_www5(self):
        self.main_browser.setUrl(QUrl(self.url_www5))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the denik.cz
    def navigate_www6(self):
        self.main_browser.setUrl(QUrl(self.url_www6))
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)


