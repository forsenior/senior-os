def get_default_start_button_style():
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
                margin-left: 5px;
                margin-right: 5px;
                min-height:260;
            }
            QPushButton:hover {
                background-color: #48843F;
            }
            QPushButton:open {
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
