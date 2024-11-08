from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class MenuButton(QPushButton):
    def __init__(self, text, color, active=False):
        super().__init__()

        # Set button text
        self.setText(text)

        # Apply common button styles
        self.setFixedSize(244, 107)
        self.setFont(QFont('Inter', 20))
        self.setStyleSheet(self.get_style(active))

    def get_style(self, active):
        # Define styles for normal and phishing states
        base_style = """
                QPushButton {
                    background-color: #949494;
                    border: 1px solid #797979;
                    border-radius: 3px;
                    color: #FFFFFF;
                    margin-left: 10px;
                    margin-top: 10px;
                    margin-right: 10px;
                    margin-bottom: 12px;
                }
                QPushButton:hover {
                    background-color: #48843F;
                }
            """

        if active:
            return base_style + """
                QPushButton {
                    background-color: #48843F
                }
            """

        return base_style


class MenuBar(QWidget):
    def __init__(self, normal_state=True):
        super().__init__()

        # Create a horizontal layout for menu buttons
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Create buttons
        self.buttons = []
        button_titles = ["Menu", "Place", "Global", "Web", "Mail"]
        for title in button_titles:
            button = MenuButton(title, normal_state)
            self.buttons.append(button)
            self.layout.addWidget(button)

        # Set margin and background for MenuBar
        self.setStyleSheet(self.get_style(normal_state))

    def get_style(self, normal_state):
        # Styles for MenuBar in normal and phishing states
        if normal_state:
            return """
                QWidget {
                    background-color: transparent;
                    border: none;
                    margin: 0px;
                }
            """
        else:
            return """
                QWidget {
                    background-color: #FF0000;
                    border: 1px solid #F90000;
                    margin: 0px;
                }
            """
