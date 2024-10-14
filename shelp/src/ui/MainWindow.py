from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, QHBoxLayout, QGridLayout, QLabel, QComboBox, \
    QLineEdit
from shelp.src.ui.uiComponents.Menu import MenuBar, MenuButton


class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout for labels and input fields
        grid_layout = QGridLayout()

        # Labels
        label_language = QLabel("Language")
        label_alert_color = QLabel("Alert color (in hex)")
        label_highlight_color = QLabel("Highlight color (in hex)")
        label_protection_level = QLabel("Protection Level")

        # Dropdowns and Inputs
        combo_language = QComboBox()
        combo_language.addItems(["English", "Spanish", "French"])

        input_alert_color = QLineEdit("Select value of the alert in hex values (default is #FF0000)")
        input_highlight_color = QLineEdit("Select value of the alert in hex values (default is #48843F)")

        combo_protection_level = QComboBox()
        combo_protection_level.addItems(["PL1", "PL2", "PL3"])

        # Add widgets to the grid
        grid_layout.addWidget(label_language, 0, 0)
        grid_layout.addWidget(combo_language, 0, 1)

        grid_layout.addWidget(label_alert_color, 1, 0)
        grid_layout.addWidget(input_alert_color, 1, 1)

        grid_layout.addWidget(label_highlight_color, 2, 0)
        grid_layout.addWidget(input_highlight_color, 2, 1)

        grid_layout.addWidget(label_protection_level, 3, 0)
        grid_layout.addWidget(combo_protection_level, 3, 1)

        # Set widget layout
        self.setLayout(grid_layout)

        # Apply styling
        self.setStyleSheet("""
            QLabel {
                font-family: Inter;
                font-size: 18px;
                color: #000000;
                padding: 5px;
            }
            QComboBox, QLineEdit {
                font-family: Inter;
                font-size: 16px;
                padding: 5px;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set main window properties
        self.setWindowTitle("Main Window")
        self.setFixedSize(1260, 580)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                border: 3px solid #000000;
                border-radius: 3px;
            }
        """)

        # Create layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create the menu bar area
        menu_layout = QHBoxLayout()

        # Add Menu Buttons
        buttons = [
            MenuButton("Menu", color=""),
            MenuButton("Global", color="", active=True),
            MenuButton("Web", color=""),
            MenuButton("Mail", color="")
        ]
        for button in buttons:
            menu_layout.addWidget(button)

        # Add an empty button (for the red button)
        red_button = MenuButton("X", color="#FF0000")
        menu_layout.insertWidget(1, red_button)

        # Create the content area
        content_widget = ContentWidget()

        # Add to layout
        layout.addLayout(menu_layout)
        layout.addWidget(content_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
