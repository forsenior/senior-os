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


def get_default_menu_button_style(highlight_color):
    return f"""
        QPushButton {{
            text-align: center;
            font-family: Inter;
            font-size: 40px;
            background-color: #949494;
            border: 1px solid #797979;
            border-radius: 8px;
            color: #FFFFFF;
            margin: 1px;
            box-sizing: border-box;
            width: 244px;
            height: 107px;
        }}
        QPushButton:hover {{
            background-color: #{highlight_color};
        }}
    """


def get_active_menu_button_style(highlight_color):
    return f"""
        QPushButton {{
            background-color: #48843F;
            border: 1px solid #797979;
            border-radius: 8px;
            color: #FFFFFF;
            margin: 1px;
            text-align: center;
            font-family: Inter;
            font-size: 40px;
            box-sizing: border-box;
            width: 244px;
            height: 107px;
        }}
        QPushButton:hover {{
            background-color: #{highlight_color};
        }}
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


def get_default_rich_text_style():
    return """
        QLabel {
            font-family: Inter;
            font-size: 20px;
            color: #000000;
            background-color: #e6e8e6;
            text-align: center;
            margin: 10px;
            padding: 20px;
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


def get_default_settings_button_style(highlight_color):
    return f"""
        QPushButton {{
            font-family: Inter;
            font-size: 12px;
            text-align: center;
            color: #000000;
            border: 1px solid #000000;
            border-radius: 4px;
            background-color: #D9D9D9;
            max-height: 20px;
            max-width: 500px;
        }}
        QPushButton:hover {{
            background-color: #{highlight_color};
        }}
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


def get_default_config_button_style(highlight_color):
    return f"""
        QPushButton {{
            font-family: Inter;
            font-size: 20px;
            text-align: center;
            color: #000000;
            margin-top: 15px;
            margin-left: 40px;
            margin-right: 40px;
            border: 1px solid #000000;
            border-radius: 4px;
            background-color: #D9D9D9;
            min-width: 240px;
            height: 50px;

        }}
        QPushButton:hover {{
            background-color: #{highlight_color};
        }}
    """


def get_default_table_style():
    return """
        QTableWidget {
            background-color: #FFFFFF;
            border: 1px solid #000000;
            border-radius: 3px;
            font-size: 16px;
            min-width: 500px;
            min-height: 300px;
            max-height: 400px;
        }
        QTableWidget::item {
            font-size: 16px;
            padding: 5px;
            border-bottom: 1px solid #E0E0E0;
        }
        QTableWidget::item:selected {
            background-color: #48843F;
        }
        QHeaderView::section {
            background-color: #E0E0E0;
            padding: 5px;
            font-weight: bold;
            border: 1px solid #C0C0C0;
        }
        QTableWidget QLineEdit {
            font-family: Inter;
            font-size: 16px;
            border: 1px solid #000000;
            border-radius: 3px;
            padding: 5px;
            margin: 2px;
        }
        QPushButton {
            min-height: 30px;
            margin: 2px;
        }
    """


def get_default_dialog_style():
    return """
            QDialog{
                background-color: #f0f0f0;
                border: 2px solid #444;
                border-radius: 10px;
                font-family: 'Inter';
            }
        """