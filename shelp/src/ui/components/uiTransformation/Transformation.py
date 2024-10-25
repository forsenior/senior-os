from PyQt5.QtWidgets import QLineEdit, QTextEdit


class UiElementTransformation:

    @staticmethod
    def expand_widget(text_edit: QTextEdit, line_edit: QLineEdit):
        """Expands the corresponding QTextEdit and hides the passed QLineEdit."""
        line_edit.setVisible(False)
        text_edit.setVisible(True)
        text_edit.setFocus()

    @staticmethod
    def collapse_widget(text_edit: QTextEdit, line_edit: QLineEdit):
        """Collapses the QTextEdit and shows the corresponding QLineEdit."""
        line_edit.setVisible(True)
        text_edit.setVisible(False)
        line_edit.setText(text_edit.toPlainText())
