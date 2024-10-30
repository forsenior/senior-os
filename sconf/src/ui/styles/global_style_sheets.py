def get_main_window_style():
    return """
        QMainWindow {
            background-color: #FFFFFF;
            border: 3px solid #000000;
            border-radius: 3px;
        }
    """


def get_default_menu_button_style():
    return """
        QPushButton {
            text-align:center;
            font-family: Inter;
            font-size: 40px;
            padding: 5px;
            background-color: #949494;
            border: 1px solid #797979;
            border-radius: 3px;
            color: #FFFFFF;
            margin-left: 10px;
            margin-top: 10px;
            margin-right: 10px;
            margin-bottom: 12px;
            max-width: 513px;
        }
        QPushButton:hover {
            background-color: #48843F;
        }
        QPushButton:open {
            background-color: #48843F;
        }
    """


def get_active_menu_button_style():
    # Define styles for normal and phishing states
    base_style = """
            QPushButton {
                background-color: #48843F;
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

    return base_style


def get_default_label_style():
    return """
    QLabel {
        font-family: Inter;
        font-size: 20px;
        color: #000000;
        max-width: 261px;
        max-height: 32px;
    }
    """


def get_error_label_style():
    return """
    QLabel {
        font-family: Inter;
        font-size: 20px;
        color: #FF0000;
        max-height: 32px;
        align: center;
    }
    """


def get_default_dropdown_style():
    return """
    QComboBox {
        font-family: Inter;
        font-size: 16px;
        border: 1px solid #000000;
        border-radius: 3px;
        align: left;
        max-width: 513px;
        max-height: 32px;
    }
    """


def get_default_input_box_style():
    return """
    QLineEdit {
        font-family: Inter;
        font-size: 16px;
        border: 1px solid #000000;
        border-radius: 3px;
        max-width: 513px;
        max-height: 32px;
    }
    """


def get_default_settings_button_style():
    return """
        QPushButton{
            text-align:center;
            font-family: Inter;
            font-size: 16px;
            color: #FFFFFF;
            margin-left: 0px;
            margin-top: 0px;
            margin-right: 0px;
            margin-bottom: 2px;
        }
    """


def get_default_settings_text_edit_style():
    return """
        QTextEdit {
            font-family: Inter;
            font-size: 16px;
            border: 1px solid #000000;
            border-radius: 3px;
            max-width: 513px;
            max-height: 200px;
        }
    """
