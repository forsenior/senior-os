import sys
from typing import List

from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout

from srun.ui.styles.srun_style_sheets import get_default_start_button_style


class MainWindowView(QWidget):
    
    def __init__(self, start_objects: List[str], data_provider, data_writer):
        super().__init__()

        self.setWindowTitle("SRUN")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Set main background style
        self.setStyleSheet(f"""
                    background-color: #FFFFFF;
                """)

        # Main container layout to center the widget
        main_layout = QVBoxLayout(self)

        # Central container for buttons with fixed size
        central_widget = QWidget()
        central_widget.setFixedSize(1260, 580)
        central_widget.setStyleSheet("""
                    background-color: #F0F0F0;
                    border: 1px solid #000000;
                    border-radius: 3px;
                    /* Optional: light background for central widget */
                """)

        # Grid layout for buttons within the central widget
        grid_layout = QGridLayout(central_widget)

        # Create buttons
        button_exit = QPushButton("")
        button_smail = QPushButton("MAIL")
        button_sweb = QPushButton("WEB")
        button_sconf = QPushButton("CONF")

        button_exit.setStyleSheet(get_default_start_button_style())
        button_smail.setStyleSheet(get_default_start_button_style())
        button_sweb.setStyleSheet(get_default_start_button_style())
        button_sconf.setStyleSheet(get_default_start_button_style())

        pixmap_icon = QPixmap(r"../sconf/icons/exit.png").scaled(100, 100)
        button_exit.setIconSize(QSize(100, 100))
        button_exit.setIcon(QIcon(pixmap_icon))

        grid_layout.addWidget(button_smail, 0, 0)
        grid_layout.addWidget(button_sweb, 0, 1)
        grid_layout.addWidget(button_sconf, 1, 0)
        grid_layout.addWidget(button_exit, 1, 1)

        # Center the central widget in the full-screen layout
        main_layout.addStretch(1)  # Add space above the central widget
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)  # Add space to the left
        h_layout.addWidget(central_widget)
        h_layout.addStretch(1)  # Add space to the right
        main_layout.addLayout(h_layout)
        main_layout.addStretch(1)  # Add space below the central widget

