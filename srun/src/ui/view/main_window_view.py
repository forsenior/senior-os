import sys
from typing import List

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton


class MainWindowView():
    
    def __init__(self, start_objects: List[str]):
        super().__init__()
        grid_layout = QGridLayout()
        self.start_objects = start_objects

        # Create buttons
        button_exit = QPushButton("X")
        button_smail = QPushButton("MAIL")
        button_sweb = QPushButton("WEB")
        button_scong = QPushButton("CONF")

