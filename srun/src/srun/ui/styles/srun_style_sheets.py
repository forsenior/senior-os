def get_default_start_button_style(highlight_color):
    return f"""
            QPushButton {{
                text-align:center;
                font-family: Inter;
                font-size: 40px;
                background-color: #949494;
                border: 1px solid #797979;
                border-radius: 3px;
                color: #FFFFFF;
                margin-top: 5px;
                margin-left: 5px;
                margin-right: 5px;
                min-height:250;
                min-width: 520
            }}
            QPushButton:hover {{
                background-color: #{highlight_color};
            }}
            QPushButton:open {{
                background-color: #{highlight_color};
            }}
        """


def get_transparent_label_style():
    return """
        QLabel {
            text-align: center;
            font-family: Inter;
            font-size: 10px;
            color: #FFFFFF;
            border: 0px;
            background-color: transparent;
            margin-top: 150px;
            align: bottom;
            min-width: 520px;
            max-height: 20px;
        }
    """


def get_default_tool_button_style():
    return """
            QToolButton {
                text-align:center;
                font-family: Inter;
                font-size: 10px;
                background-color: #949494;
                border: 1px solid #797979;
                border-radius: 3px;
                color: #FFFFFF;
                margin-top: 5px;
                margin-left: 5px;
                margin-right: 5px;
                min-height:250;
                min-width: 520
            }
            QToolButton:hover {
                background-color: #48843F;
            }
            QToolButton:open {
                background-color: #48843F;
            }
        """


def get_default_center_widget_style():
    return """
            QWidget{
                background-color: #F0F0F0;
                border: 1px solid #000000;
                border-radius: 3px;
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
