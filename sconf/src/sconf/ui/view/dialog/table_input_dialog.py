from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QGridLayout, QFileDialog, QDesktopWidget

from sconf.ui.styles.global_style_sheets import get_default_dialog_style, get_default_settings_button_style, \
    get_default_table_style, get_default_input_box_style


class TablePopup(QDialog):
    __updated_entries: list[dict[str, str]]

    def __init__(self, key_value_pairs, parent=None, type: str = "mail", highlight_color: str = "#48843F"):
        super().__init__(parent)

        self.setWindowTitle("Add content")
        self.setFixedSize(600, 400)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.center()
        self.setStyleSheet(get_default_dialog_style())

        layout = QGridLayout()

        # Table widget for URLs and icons (initially hidden)
        self.url_table = QTableWidget(6, 2)
        if type == "mail":
            self.url_table.setHorizontalHeaderLabels(["Email", "Icon"])
        else:
            self.url_table.setHorizontalHeaderLabels(["Website", "Icon"])
        self.url_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.url_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.url_table.setShowGrid(True)
        self.url_table.horizontalHeader().setVisible(True)
        self.url_table.verticalHeader().setVisible(False)

        # Fill table with data from config model
        index = 1

        if type == "mail":
            for row, entry in enumerate(key_value_pairs):
                url_item = QTableWidgetItem(entry[f"email{index}"])
                self.url_table.setItem(row, 0, url_item)

                icon_button = QPushButton("Select Icon")
                icon_button.setText(entry[f"icon{index}"])
                icon_button.setStyleSheet(f"""
                                {get_default_settings_button_style(highlight_color)}
                                """)
                icon_button.clicked.connect(lambda _, r=row: self.__select_icon(r))
                self.url_table.setCellWidget(row, 1, icon_button)
                index += 1
        else:
            for row, entry in enumerate(key_value_pairs):
                url_item = QTableWidgetItem(entry[f"url{index}"])
                self.url_table.setItem(row, 0, url_item)

                icon_button = QPushButton("Select Icon")
                icon_button.setText(entry[f"icon{index}"])
                icon_button.setStyleSheet(f"""
                                {get_default_settings_button_style(highlight_color)}
                                """)
                icon_button.clicked.connect(lambda _, r=row: self.__select_icon(r))
                self.url_table.setCellWidget(row, 1, icon_button)
                index += 1

        # Set up save/cancel buttons
        button_container = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(f"""
                            margin: 5px;
                            {get_default_settings_button_style(highlight_color)}
                            """)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(f"""
                            margin: 5px;
                            {get_default_settings_button_style(highlight_color)}
                            """)

        self.save_button.setMinimumWidth(150)
        self.cancel_button.setMinimumWidth(150)

        self.save_button.clicked.connect(self.__save_entries)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.url_table, 0, 0, 0, 2)
        layout.addWidget(self.save_button, 1, 0)
        layout.addWidget(self.cancel_button, 1, 1)

        self.setLayout(layout)

        self.setStyleSheet(f"""
                    {get_default_settings_button_style(highlight_color)}
                    {get_default_input_box_style()}
                    {get_default_table_style()}""")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __select_icon(self, row):
        # Open file dialog to select icon and update button label to path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon")
        if file_path:
            icon_button = self.url_table.cellWidget(row, 1)
            icon_button.setText(file_path)  # Show path on button for preview

    def __save_entries(self) -> list[dict[str, str]]:
        # Save changes to model
        index = 1
        new_entries = []

        if type == "mail":
            for row in range(6):
                url = self.url_table.item(row, 0).text() if self.url_table.item(row, 0) else ""
                icon_path = self.url_table.cellWidget(row, 1).text() if self.url_table.cellWidget(row, 1) else ""
                if url:  # Only save if URL is not empty
                    new_entries.append({f"email{index}": url, f"icon{index}": icon_path})
                index += 1
        else:
            for row in range(6):
                url = self.url_table.item(row, 0).text() if self.url_table.item(row, 0) else ""
                icon_path = self.url_table.cellWidget(row, 1).text() if self.url_table.cellWidget(row, 1) else ""
                if url:  # Only save if URL is not empty
                    new_entries.append({f"url{index}": url, f"icon{index}": icon_path})
                index += 1

        self.__updated_entries = new_entries
        self.accept()

    def get_updated_entries(self):
        return self.__updated_entries
