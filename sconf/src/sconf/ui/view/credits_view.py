from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from sconf.ui.styles.global_style_sheets import get_default_rich_text_style


class CreditsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignCenter)

        credits_text = QLabel("Credits")
        credits_text.setAlignment(Qt.AlignCenter)
        credits_text.setText(f"""\n\tAuthors \n\n\tDan Komosny, Hung Ngo Quang, Ondrej Kudela, Tarik Alkanan \n\n\tZacek Jan Filip, Nguyen Tuan Ninh, Vala Robin, Brablik Petr \n\n\tVeronika Vojáčková, Štěpán Pijáček, Fiala Marek
            """)

        layout.addWidget(credits_text)

        self.setLayout(layout)

        self.setStyleSheet(f"""
                            {get_default_rich_text_style()}
                        """)
