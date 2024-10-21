from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QGridLayout


class GlobalSettingsView(QWidget):
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
                        border: 1px solid #000000;
                        border-radius: 3px;
                        width: 513px;
                        height: 30px
                    }
                """)
