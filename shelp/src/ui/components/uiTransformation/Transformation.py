from typing import List

from PyQt5.QtWidgets import QLineEdit, QTextEdit, QFileDialog


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

    @staticmethod
    def open_file_dialog(folder_path: str) -> List[str]:
        """Opens file dialog window for multi Image File selection"""
        file_dialog = QFileDialog(None)
        selected_files, _ = file_dialog.getOpenFileNames(None,
                                                         "QFileDialog.getOpenFileName()",
                                                         f"{folder_path}"
                                                         , "All Files (*);;Image File (*.png *.jpg *.gif)")
        return selected_files
