import logging
import os
import re
import subprocess
import threading

from PyQt5 import sip
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QDesktopServices, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QTextEdit, \
    QApplication, QListWidget, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem

from connection.mail_connection import (send_email, read_mail)

from style import (search_mail, get_language, images, app_color,
                   get_email_sender, load_credentials,
                   load_show_url, load_button_colors, get_path)
# from template import configActions as act
from template import guiTemplate as temp

logger = logging.getLogger(__file__)

class first_frame(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_configuration()
        self.language, self.text_configuration = get_language()
        self.last_selected_index = None
        self.last_selected_email = None
        self.last_selected_button = None
        self.button_state = None
        self.alert= False
        self.menu1= True
        self.red_state = False
        main_layout = QVBoxLayout()

        # 1. Top strip (button frame)
        self.button_frame_setup()
        main_layout.addWidget(self.button_frame)

        # 1.1 Load icons
        self.image_configuration()

        # 1.2 Buttons
        self.buttons_setup()

        # 2. Bottom section (left and right panel)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(0)

        # 3. Left panel for email list
        self.left_panel_setup()
        self.bottom_layout.addWidget(self.left_panel)

        # 4. Right panel for email content
        self.right_panel_setup()
        self.bottom_layout.addWidget(self.right_panel, stretch=1)

        # 5. Add to main layout
        main_layout.addLayout(self.bottom_layout)
        self.setLayout(main_layout)

        # 6. Load emails
        self.loading_emails = threading.Thread(target=self.periodic_email_loading)
        self.loading_emails.start()
        self.allow_show_email = True

    def toggle_menu1(self):
        self.menu1 = not self.menu1
        print(f"menu1 toggled to: {self.menu1}")
        self.clear_buttons()
        self.buttons_setup()

    def button_frame_setup(self):
        self.button_frame = QFrame(self)
        self.button_frame.setStyleSheet(temp.get_button_frame_style())
        self.button_layout = QHBoxLayout(self.button_frame)

    def clear_buttons(self):
        while self.button_layout.count():
            child = self.button_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def buttons_setup(self):
        button_menu1 = ["MENU 1", "EXIT", "Button 2", "Button 3", "Button 4"]
        button_menu2 = ["MENU 2", "Button 6", "Button 7", "Button 8", "Komu"]
        spacer_left = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        current_menu = button_menu1 if self.menu1 else button_menu2

        self.button_layout.addItem(spacer_left)
        for index, text in enumerate(current_menu):
            button = QPushButton(text, self.button_frame)

            if not self.menu1 and index == 4:
                button.setStyleSheet(temp.get_button_style(green=True))
            else:
                button.setStyleSheet(temp.get_button_style())

            self.button_layout.addWidget(button, alignment=Qt.AlignCenter)

            if self.menu1:
                if index == 0:
                    button.clicked.connect(self.toggle_menu1)

                elif index == 1:
                    button.setText("")
                    button.setIconSize(QSize(72, 72))
                    button.setIcon(self.exit_image)
                    button.clicked.connect(self.exit_app)

                elif index == 2:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person1_image)
                    button.clicked.connect(lambda _, btn=button, nb=1: self.decide_action_for_button(btn, nb))

                elif index == 3:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person2_image)
                    button.clicked.connect(lambda _, btn=button, nb=2: self.decide_action_for_button(btn, nb))

                elif index == 4:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person3_image)
                    button.clicked.connect(lambda _, btn=button, nb=3: self.decide_action_for_button(btn, nb))

            else:
                if index == 0:
                    button.clicked.connect(self.toggle_menu1)

                elif index == 1:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person4_image)
                    button.clicked.connect(lambda _, btn=button, nb=4: self.decide_action_for_button(btn, nb))

                elif index == 2:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person5_image)
                    button.clicked.connect(lambda _, btn=button, nb=5: self.decide_action_for_button(btn, nb))

                elif index == 3:
                    button.setText("")
                    button.setIconSize(QSize(100, 100))
                    button.setIcon(self.person6_image)
                    button.clicked.connect(lambda _, btn=button, nb=6: self.decide_action_for_button(btn, nb))

                elif index == 4:
                    button.clicked.connect(lambda _, btn=button, nb=7: self.decide_action_for_button(btn, nb))

        self.button_layout.setSpacing(10)
        self.button_layout.addItem(spacer_right)
        self.button_layout.setContentsMargins(10, 12, 10, 10)

    def alert_buttons(self, alert=True):
        for i in range(self.button_layout.count()):
            widget = self.button_layout.itemAt(i).widget()

            if isinstance(widget, QPushButton):
                if alert:
                    widget.setStyleSheet(temp.get_button_style(normal=False))
                else:
                    widget.setStyleSheet(temp.get_button_style(normal=True))

    def image_configuration(self):
        try:
            self.img = images()
            self.exit_image = QIcon(self.img["exit"])
            self.person1_image = QIcon(self.img["Person1"])
            self.person2_image = QIcon(self.img["Person2"])
            self.person3_image = QIcon(self.img["Person3"])
            self.person4_image = QIcon(self.img["Person4"])
            self.person5_image = QIcon(self.img["Person5"])
            self.person6_image = QIcon(self.img["Person6"])
        except Exception:
            logger.error("Failed loading language and images")

    def exit_app(self):
        self.close()
        QApplication.quit()
        subprocess.run(["kill", "-9", str(os.getpid())])

    def left_panel_setup(self):

        self.left_panel = QFrame(self)
        self.left_panel.setStyleSheet(temp.get_left_panel_style())
        self.left_panel.setFixedWidth(259)

        # Email list
        self.inbox_list_label = QLabel("Doručená pošta:", self.left_panel)
        self.inbox_list_label.setFixedHeight(22)
        self.inbox_list_label.setStyleSheet(temp.get_text_style())
        self.inbox_list = QListWidget(self.left_panel)
        self.inbox_list.setStyleSheet(temp.get_inbox_style())

        # Layout for the left panel
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.addWidget(self.inbox_list_label)
        self.left_panel_layout.addWidget(self.inbox_list)

    def right_panel_setup(self, recipient_email="", show_sender_info=True):

        subject_label = self.text_configuration[f"smail_{self.language}_subjectLabel"]
        recipient_label = self.text_configuration[f"smail_{self.language}_recipientLabel"]
        message_label = self.text_configuration[f"smail_{self.language}_messageLabel"]
        from_label = self.text_configuration[f"smail_{self.language}_from"]

        # Right panel setup
        self.right_panel = QFrame(self)
        self.right_panel.setStyleSheet(temp.get_right_panel_style())

        if show_sender_info:
            self.sender_info_label_1 = QLabel(f"{from_label}", self.right_panel)
            self.sender_info_label_1.setFixedHeight(22)
            self.sender_info_label_1.setStyleSheet(temp.get_text_style())
            self.sender_info_label_2 = QTextEdit(self.right_panel)
            self.sender_info_label_2.setReadOnly(True)
            self.sender_info_label_2.setFixedHeight(114)
            self.sender_info_label_2.setStyleSheet(temp.get_sender_info_label())

        # Recipient info
        else:
            self.recipient_info_label_1 = QLabel(f"{recipient_label}",
                                                 self.right_panel)
            self.recipient_info_label_1.setFixedHeight(22)
            self.recipient_info_label_2 = QTextEdit(recipient_email or "", self.right_panel)
            self.recipient_info_label_2.setReadOnly(True)
            self.recipient_info_label_2.setFixedHeight(40)
            self.recipient_info_label_3 = QLabel(f"{subject_label}:",
                                                 self.right_panel)
            self.recipient_info_label_3.setFixedHeight(22)
            self.recipient_info_label_4 = QTextEdit("", self.right_panel)
            self.recipient_info_label_4.setReadOnly(True)
            self.recipient_info_label_4.setFixedHeight(40)
            self.recipient_info_label_1.setStyleSheet(temp.get_text_style())
            self.recipient_info_label_2.setStyleSheet(temp.get_label_style())
            self.recipient_info_label_3.setStyleSheet(temp.get_text_style())
            self.recipient_info_label_4.setStyleSheet(temp.get_label_style())

        # Layout for the email content
        self.email_content_label_1 = QLabel(f"{message_label}",
                                            self.right_panel)
        self.email_content_label_1.setFixedHeight(22)
        self.email_content_label_1.setStyleSheet(temp.get_text_style())
        self.email_content_label_2 = QTextEdit(self.right_panel)
        self.email_content_label_2.setReadOnly(True)
        self.email_content_label_2.setStyleSheet(temp.get_email_content_label())

        # Layout for the right panel
        self.right_panel.setLayout(QVBoxLayout())

        if show_sender_info:
            self.right_panel.layout().addWidget(self.sender_info_label_1)
            self.right_panel.layout().addWidget(self.sender_info_label_2)
            self.right_panel.layout().addWidget(self.email_content_label_1)
            self.right_panel.layout().addWidget(self.email_content_label_2)

        else:
            self.right_panel.layout().addWidget(self.recipient_info_label_1)
            self.right_panel.layout().addWidget(self.recipient_info_label_2)
            self.right_panel.layout().addWidget(self.recipient_info_label_3)
            self.right_panel.layout().addWidget(self.recipient_info_label_4)
            self.right_panel.layout().addWidget(self.email_content_label_1)
            self.right_panel.layout().addWidget(self.email_content_label_2)

    def load_emails(self):
        self.insert_emails()

    def periodic_email_loading(self):
            self.load_emails()
            QTimer.singleShot(10000, self.periodic_email_loading)

    def activate_show_email(self, event):
        self.allow_show_email = True

    def insert_emails(self):
        previous_emails = getattr(self, "reversed_list", [])
        (login, password, smtp_server, smtp_port, imap_server, imap_port) = (
            load_credentials(get_path("sconf", "SMAIL_config.json")))
        language, text = get_language()

        self.emails, self.subjects = read_mail(login, password, imap_server, imap_port, language, text)
        self.reversed_list = list(zip(self.emails[::-1], self.subjects[::-1]))

        if previous_emails != self.reversed_list:
            self.inbox_list.clear()
            print("Clearing the listbox")

            self.all_emails = [(email_content, subject, "safe") for email_content, subject in self.reversed_list]

            for email_content, subject, _ in self.all_emails:
                name = get_email_sender(email_content.split("\n")[1])
                sub = email_content.split("\n")[0].split(":", 1)[1]
                self.inbox_list.addItem(f"{name} - {sub}")

            self.inbox_list.itemSelectionChanged.connect(self.show_email)

    def show_email(self):

        if not self.allow_show_email:
            return

        if hasattr(self, 'last_selected_button') and self.last_selected_button is not None:
            if not sip.isdeleted(self.last_selected_button):
                self.last_selected_button.setStyleSheet(temp.get_button_style())
            self.last_selected_button = None

        selected_items = self.inbox_list.selectedItems()
        if not selected_items:
            return

        try:
            selected_index = self.inbox_list.currentRow()
        except IndexError:
            print("Index out of range.")
            return

        selected_email = self.all_emails[selected_index]
        email_content = selected_email[0]
        email_lines = email_content.split("\n")
        email_subject_line = email_lines[0]
        email_sender_line = email_lines[1]
        email_date_line = email_lines[2]
        email_message_content = "\n".join(email_lines[4:])

        self.configure_message_area(email_message_content, email_subject_line, email_sender_line, email_date_line)
        self.last_selected_index = selected_index
        self.last_selected_email = email_content

    def configure_message_area(self, email_content, email_subject, email_sender, email_date):
        self.right_panel.setParent(None)
        self.right_panel_setup(show_sender_info=True)
        self.bottom_layout.addWidget(self.right_panel, stretch=1)

        self.email_content_label_2.setReadOnly(False)
        self.email_content_label_2.clear()
        self.email_content_label_2.append(email_content)
        self.email_content_label_2.setReadOnly(True)

        self.sender_info_label_2.setReadOnly(False)
        self.sender_info_label_2.clear()
        self.sender_info_label_2.append(f"{email_subject}\n{email_sender}\n{email_date}")
        self.sender_info_label_2.setReadOnly(True)

    def update_email_content(self, subject: str, content: str):
        self.email_content_label_1.setText(subject)
        self.email_content_label_2.setText(content)

    def decide_action_for_button(self, button, recipient_index=None):
        try:
            if self.last_selected_button == button:
                self.send_email_status()
            else:
                self.fill_recipient(recipient_index)
                self.last_selected_button = button
        except Exception as e:
            logger.error(f"An error occurred in decide_action_for_button: {e}")
            print(f"An error occurred in decide_action_for_button: {e}")

    def fill_recipient(self, index):
        try:
            if hasattr(self, 'last_selected_button') and self.last_selected_button is not None:
                if not sip.isdeleted(self.last_selected_button):
                    self.last_selected_button.setStyleSheet(temp.get_button_style())
            sender = self.sender()

            if sender is not None and not sip.isdeleted(sender):
                sender.setStyleSheet(temp.get_button_style(green=True))
                self.last_selected_button = sender
            recipient_email = ""
            if 1 <= index <= 6:
                recipient_email = search_mail(index)
            elif index == 7:
                recipient_email = ""

            self.right_panel.setParent(None)
            self.right_panel_setup(recipient_email, False)
            self.bottom_layout.addWidget(self.right_panel, stretch=1)
            self.email_content_label_2.setReadOnly(False)
            self.recipient_info_label_4.setReadOnly(False)
            self.recipient_info_label_2.setReadOnly(False)

        except Exception as e:
            logger.error(f"An error occurred in fill_recipient: {e}")
            print(f"An error occurred in fill_recipient: {e}")

    def send_email_status(self):

        (login, password, smtp_server,
         smtp_port, imap_server, imap_port) = (
            load_credentials(get_path("sconf", "SMAIL_config.json")))

        recipient = self.recipient_info_label_2.toPlainText().strip()
        subject = self.recipient_info_label_4.toPlainText().strip()
        content = self.email_content_label_2.toPlainText().strip()

        if not recipient:
            logger.error("Příjemce nebyl zadan.")
            return

        if not subject or not content:
            logger.error("Předmět nebo obsah emailu chybi.")
            return

        success = send_email(
            recipient, subject, content, login, password, smtp_server, smtp_port
        )

        if success == 1:
            self.send_email_success()
        else:
            logger.error(f"Email nebyl uspěšně odeslán, status: {success}")

    def send_email_success(self):
        default_color, selected_color = load_button_colors()
        bg_default_color = app_color()

        self.recipient_info_label_2.clear()
        self.recipient_info_label_4.clear()
        self.email_content_label_2.clear()

        height = self.email_content_label_2.height()
        line_height = 36
        total_lines = max(1, height // line_height)
        middle_line = total_lines // 2

        padding = "\n" * (middle_line - 2)
        self.email_content_label_2.insertPlainText(padding)
        self.email_content_label_2.insertPlainText(self.text_configuration[f"smail_{self.language}_email_sent"])
        self.email_content_label_2.setAlignment(Qt.AlignCenter)
        current_style = temp.get_email_content_label()
        self.email_content_label_2.setStyleSheet(current_style + f"background-color: {selected_color};")
        self.email_content_label_2.setReadOnly(True)

        QTimer.singleShot(5000, lambda: self.clear_content_entry(bg_default_color))

    def clear_content_entry(self, default_color):
        self.email_content_label_2.setReadOnly(False)
        self.email_content_label_2.clear()
        self.email_content_label_2.setStyleSheet(temp.get_email_content_label() + f"background-color: {default_color};")

    def alert_missing_text(self, entry, default_color, select_color):
        #entry.configure(background=select_color)
        entry.setStyleSheet(f"background-color: {select_color};")
        #entry.after(2000, lambda: entry.configure(background= default_color))
        QTimer.singleShot(2000, lambda: entry.setStyleSheet(f"background-color: {default_color};"))

    def mark_important_data(self):

        default_color, selected_color = (
            load_button_colors())

        #lines = self.message_area.get("1.0", "end-1c").split("\n")
        lines = self.message_area.toPlainText().split("\n")
        words_before_colon = [lines[0][:lines[0].find(":")].strip(),
                              lines[1][:lines[1].find(":")].strip()]

        # try:
             # for i, word in enumerate(words_before_colon, start=1):
            #     start_index = "1.0"
            #     line_number = i
            #     while True:
            #         line_start = self.message_area.search(word, start_index, stopindex=f"{line_number}.end",
            #                                              nocase=True)
            #         if not line_start:
            #            break
            #         colon_index = int(line_start.split('.')[1]) + len(word)
            #         text_after_colon = self.message_area.get(f"{line_number}.{colon_index + 2}",
            #                                                 f"{line_number}.end")
            #         self.message_area.delete(f"{line_number}.{colon_index + 2}",
            #                                 f"{line_number}.end")
            #         self.message_area.insert(f"{line_number}.{colon_index + 2}",
            #                                 text_after_colon, "color")
            #
            #        start_index = f"{line_number + 1}.0"
            # self.message_area.tag_configure("color", background=selected_color)


        # except Exception as e:
        #     print("lag")
        #     logger.error("Error occurred when marking important data: " + str(e))

    def mark_email(self):

        show = load_show_url(get_path("sconf", "SMAIL_config.json"))

        if show == 1:
            # Find all URLs in email and tag them
            #for match in re.finditer(r'https?://\S+|www\.\S+', self.message_area.get("1.0", tk.END)):
            for match in re.finditer(r'https?://\S+|www\.\S+', self.message_area.toPlainText()):
                url = match.group()
                self.mark_and_link_url(url)

    def mark_and_link_url(self, url):
        # Assign name to URL and bind it for click event
        #start_pos = "1.0"
        start_pos = 0
        text = self.message_area.toPlainText()

        while True:
            #start_index = self.message_area.search(url, start_pos, tk.END)
            start_index = text.find(url, start_pos)
            # If there are no other URLs break
            #if not start_index:
            if start_index == -1:
                break

            # Calculating the end of URL
            #end_index = f"{start_index}+{len(url)}c"
            end_index = start_index + len(url)

            # Creating an original name for the URL: replacing . with _ to make the name valid
            #tag_name = f"clickable_{start_index.replace('.', '_')}"
            cursor = self.message_area.textCursor()
            cursor.setPosition(start_index)
            cursor.setPosition(end_index, QTextCursor.KeepAnchor)

            # Name and URL config
            #self.message_area.tag_add(tag_name, start_index, end_index)
            #self.message_area.tag_config(tag_name, foreground="blue", underline=True)
            #self.message_area.tag_bind(tag_name, "<Button-1>", lambda event, u=url: self.open_browser(event, u))
            char_format = QTextCharFormat()
            char_format.setForeground(Qt.blue)
            char_format.setFontUnderline(True)

            cursor.setCharFormat(char_format)

            self.message_area.setTextCursor(cursor)
            self.message_area.cursorPositionChanged.connect(lambda: self.open_browser(url))

            start_pos = end_index

    def open_browser(self, event, url):
        # Open web browser when clicking on a URL.
        try:
            subprocess.run(["python3", get_path("sweb", "sweb.py"), url])
            self.exit_app()
        except Exception as e:
            #webbrowser.open_new(url)
            QDesktopServices.openUrl(QUrl(url))
            #logger.error("Failed to open sweb.")
            logger.error("Failed to open sweb. Defaulting to browser.", exc_info=True)
