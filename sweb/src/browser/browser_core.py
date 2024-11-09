from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot
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
    