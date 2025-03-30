from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QGridLayout, QFileDialog, QDesktopWidget, QAbstractItemView

from sconf.ui.styles.global_style_sheets import get_default_dialog_style, get_default_settings_button_style, \
    get_default_table_style, get_default_input_box_style


class TablePopup(QDialog):
    """
    A dialog that displays a table for editing either email contacts or website URLs
    along with their associated icons.
    """

    def __init__(self, entries, parent=None, entry_type="mail", highlight_color="#48843F"):
        """
        Initialize the TablePopup dialog.

        Args:
            entries: List of dictionaries containing the initial data
            parent: Parent widget
            entry_type: Type of entries to edit ("mail" or "url")
            highlight_color: Color for highlighted elements
        """
        super().__init__(parent)

        # Store parameters
        self.entry_type = entry_type.lower()  # Normalize to lowercase
        self.highlight_color = highlight_color
        self.entries_result = []  # Will store the updated entries when saved

        # Validate entry_type
        if self.entry_type not in ["mail", "web", "url"]:
            # Default to mail if invalid type provided
            print(f"Warning: Invalid entry_type '{entry_type}'. Defaulting to 'mail'.")
            self.entry_type = "mail"

        # Normalize "web" to "url" for internal consistency
        if self.entry_type == "web":
            self.entry_type = "url"

        # Configure dialog
        self.setWindowTitle(f"Add {'Email Contacts' if self.entry_type == 'mail' else 'Websites'}")
        self.setFixedSize(600, 400)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.center()
        self.setStyleSheet(get_default_dialog_style())

        # Create layout
        self._setup_ui()
        self._populate_table(entries)

    def _setup_ui(self):
        """Set up the user interface components."""
        main_layout = QGridLayout()

        # Create table widget
        self.entry_table = QTableWidget(6, 2)

        # Set table headers based on entry type
        if self.entry_type == "mail":
            self.entry_table.setHorizontalHeaderLabels(["Email", "Icon"])
        else:
            self.entry_table.setHorizontalHeaderLabels(["Website", "Icon"])

        # Configure table appearance
        self.entry_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.entry_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.entry_table.setShowGrid(True)
        self.entry_table.horizontalHeader().setVisible(True)
        self.entry_table.verticalHeader().setVisible(False)
        self.entry_table.setEditTriggers(QAbstractItemView.AllEditTriggers)

        # Create action buttons
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(f"""
                           margin: 5px;
                           {get_default_settings_button_style(self.highlight_color)}
                           """)
        self.save_button.setMinimumWidth(150)
        self.save_button.clicked.connect(self._save_entries)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(f"""
                           margin: 5px;
                           {get_default_settings_button_style(self.highlight_color)}
                           """)
        self.cancel_button.setMinimumWidth(150)
        self.cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        main_layout.addWidget(self.entry_table, 0, 0, 1, 2)
        main_layout.addWidget(self.save_button, 1, 0)
        main_layout.addWidget(self.cancel_button, 1, 1)

        self.setLayout(main_layout)

        # Apply overall styling
        self.setStyleSheet(f"""
                   {get_default_settings_button_style(self.highlight_color)}
                   {get_default_input_box_style()}
                   {get_default_table_style()}
                   """)

    def _populate_table(self, entries):
        """
        Initialize the table with data from entries.

        Args:
            entries: List of dictionaries containing the data to populate
        """
        # Initialize all table cells
        for row in range(6):
            # Create text item for first column (email/url)
            text_item = QTableWidgetItem("")
            text_item.setFlags(text_item.flags() | Qt.ItemIsEditable)
            self.entry_table.setItem(row, 0, text_item)

            # Create button for second column (icon)
            icon_button = QPushButton("Select Icon")
            icon_button.setStyleSheet(f"""
                           {get_default_settings_button_style(self.highlight_color)}
                           """)
            icon_button.clicked.connect(lambda checked, r=row: self._select_icon(r))
            self.entry_table.setCellWidget(row, 1, icon_button)

        # Fill with existing data
        for row in range(min(len(entries), 6)):
            entry = entries[row]

            # Get entry index (typically 1-based)
            index = row + 1

            # Determine which keys to look for based on entry type
            if self.entry_type == "mail":
                text_key = f"email{index}"
                icon_key = f"icon{index}"
            else:  # url/web type
                text_key = f"url{index}"
                icon_key = f"icon{index}"

            # Set text if it exists in the entry
            if text_key in entry and entry[text_key]:
                self.entry_table.item(row, 0).setText(entry[text_key])

            # Set icon path on button if it exists
            if icon_key in entry and entry[icon_key]:
                icon_button = self.entry_table.cellWidget(row, 1)
                icon_button.setText(entry[icon_key])

    def _select_icon(self, row):
        """
        Open file dialog to select an icon and update the button text.

        Args:
            row: The row index for which to select an icon
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon")
        if file_path:
            icon_button = self.entry_table.cellWidget(row, 1)
            icon_button.setText(file_path)

    def _save_entries(self):
        """
        Save the current table data and close the dialog.
        """
        # Commit any current edit by changing focus
        self.save_button.setFocus()

        # Collect data from the table
        updated_entries = []

        for row in range(6):
            # Get text from first column
            text_item = self.entry_table.item(row, 0)
            text_value = text_item.text() if text_item else ""

            # Get icon path from button in second column
            icon_button = self.entry_table.cellWidget(row, 1)
            icon_path = icon_button.text() if (icon_button and icon_button.text() != "Select Icon") else ""

            # Only save non-empty entries
            if text_value:
                index = row + 1

                # Create dict with appropriate keys based on entry type
                if self.entry_type == "mail":
                    updated_entries.append({
                        f"email{index}": text_value,
                        f"icon{index}": icon_path
                    })
                else:  # url/web type
                    updated_entries.append({
                        f"url{index}": text_value,
                        f"icon{index}": icon_path
                    })

        # Store result and accept dialog
        self.entries_result = updated_entries
        self.accept()

    def center(self):
        """Center the dialog on the screen."""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def get_updated_entries(self):
        """
        Return the updated entries after dialog is accepted.

        Returns:
            List of dictionaries containing the updated entries
        """
        return self.entries_result

    def is_mail_type(self):
        """
        Check if this popup is for mail entries.

        Returns:
            True if entry_type is mail, False otherwise
        """
        return self.entry_type == "mail"

    def is_web_type(self):
        """
        Check if this popup is for web/url entries.

        Returns:
            True if entry_type is url/web, False otherwise
        """
        return self.entry_type == "url"
