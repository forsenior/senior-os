def get_main_window_style():
    return """
        QMainWindow {
            background-color: #FFFFFF;
            border: 1px solid #000000;
            border-radius: 3px;
        }
    """


def get_default_menu_button_style():
    return """
        QPushButton {
            text-align: center;
            font-family: Inter;
            font-size: 40px;
            padding: 5px;
            background-color: #949494;
            border: 1px solid #797979;
            border-radius: 3px;
            color: #FFFFFF;
            margin: 10px 10px 20px 10px;
            max-width: 40%;  /* Ensures buttons adjust within available space */
            min-height: 70px;
        }
        QPushButton:hover, QPushButton:open {
            background-color: #48843F;
        }
    """


def get_active_menu_button_style():
    return """
        QPushButton {
            background-color: #48843F;
            border: 1px solid #797979;
            border-radius: 3px;
            color: #FFFFFF;
            margin: 10px 10px 12px 10px;
            max-width: 40%;
        }
        QPushButton:hover {
            background-color: #48843F;
        }
    """


def get_default_label_style():
    return """
    QLabel {
        font-family: Inter;
        font-size: 20px;
        color: #000000;
        min-height: 32px;
    }
    """


def get_error_label_style():
    return """
    QLabel {
        font-family: Inter;
        font-size: 20px;
        color: #FF0000;
        max-height: 32px;
        text-align: center;
    }
    """


def get_default_dropdown_style():
    return """
    QComboBox {
        font-family: Inter;
        font-size: 16px;
        border: 1px solid #000000;
        border-radius: 3px;
        padding: 4px;
        min-width: 40%;
        min-height: 32px;
    }
    """


def get_default_input_box_style():
    return """
    QLineEdit {
        font-family: Inter;
        font-size: 16px;
        border: 1px solid #000000;
        border-radius: 3px;
        padding: 4px;
        min-width: 40%;
        min-height: 32px;
    }
    """


def get_default_settings_button_style():
    return """
        QPushButton {
            text-align: center;
            font-family: Inter;
            font-size: 16px;
            color: #FFFFFF;
            margin-bottom: 2px;
            min-width: 30%;
            max-height: 25px;
        }
    """


def get_default_settings_text_edit_style():
    return """
        QTextEdit {
            font-family: Inter;
            font-size: 16px;
            border: 1px solid #000000;
            border-radius: 3px;
            padding: 4px;
            min-width: 40%;
            max-height: 200px;
        }
    """


def get_default_table_style():
    return """
        QTableWidget {
            background-color: #FFFFFF;
            border: 1px solid #000000;
            border-radius: 3px;
            font-size: 16px;
            min-width: 90%;
            min-height: 300px;
        }
        QTableWidget::item {
            font-size: 16px;
        }
        QTableWidget::item:selected {
            background-color: #48843F;
        }
        QTableWidget QLineEdit {
            font-family: Inter;
            font-size: 16px;
            border: 1px solid #000000;
            border-radius: 3px;
            padding: 4px;
            min-width: 90%;
        }
    """
