def get_main_window_style():
    return """
        QMainWindow {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 8px;
            margin: 20px;
            padding: 20px;
            box-sizing: border-box;
        }
    """

def get_default_menu_button_style():
    return """
        QPushButton {
            text-align: center;
            font-family: Inter;
            font-size: 40px;
            padding: 10px;
            background-color: #949494;
            border: 2px solid #000000;
            border-radius: 8px;
            color: #FFFFFF;
            margin: 8px;
            box-sizing: border-box;
        }
        QPushButton:hover {
            background-color: #48843F;
        }
    """

def get_active_menu_button_style():
    return """
        QPushButton {
            background-color: #48843F;
            border: 2px solid #000000;
            border-radius: 8px;
            color: #FFFFFF;
            margin: 8px;
            text-align: center;
            font-family: Inter;
            font-size: 40px;
            padding: 10px;
            box-sizing: border-box;
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
        max-width: 260px;
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
            border-radius: 4px;
            padding: 8px;
            background-color: #D9D9D9;
            min-height: 40px;
            max-width: 500px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: url(../icons/dropdown_arrow.png);
            width: 12px;
            height: 12px;
        }
    """

def get_default_input_box_style():
    return """
        QLineEdit {
            font-family: Inter;
            font-size: 16px;
            border: 1px solid #000000;
            border-radius: 4px;
            padding: 8px;
            background-color: #FFFFFF;
            min-height: 40px;
            max-width: 500px;
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
            min-width: 250px;
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
            max-width: 500px;
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
            min-width: 500px;
            max-height: 500px;
            box-sizing: border-box;
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
            max-width: 500px;
            min-height: 25px;
        }
    """