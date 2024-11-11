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
                margin-left: 10px;
                margin-top: 10px;
                margin-right: 10px;
                margin-bottom: 12px;
                min-height:145;
            }
            QPushButton:hover {
                background-color: #48843F;
            }
            QPushButton:open {
                background-color: #48843F;
            }
        """