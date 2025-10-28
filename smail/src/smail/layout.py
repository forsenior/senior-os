import os
import re
import sys
import subprocess
import threading
from pathlib import Path
from PyQt5 import sip
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QDesktopServices, QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QTextEdit, \
    QApplication, QListWidget, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem, QAbstractItemView, QScrollBar, QShortcut, QStackedWidget
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from smail import style
from smail.connection.mail_connection import send_email, read_mail, send_email_with_guardian_copy

import sconf.configuration.configuration_writer as data_writer
import sconf.configuration.configuration_provider as data_provider

CONFIG_FILE_NAME = 'config.json'


class first_frame(QWidget):
    def __init__(self, parent, data_provider, stacked_widget):
        """
            Initializes the main window of the email client, sets language, colors,
            buttons, panels, and starts loading emails.
        """
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.data_provider = data_provider
        self.image_configuration()
        self.language, self.text_configuration = style.get_language(self.data_provider)
        self.protection_level = style.get_protection_level(self.data_provider)
        self.color_scheme = style.get_color_scheme(self.data_provider)
        self.guardian_email = style.get_guardian_email(self.data_provider)
        self.last_selected_index = None
        self.last_selected_email = None
        self.last_selected_button = None
        self.last_selected_button_index = None
        self.sensitive_content_warning_displayed = False
        self.allow_show_email = False
        self.button_state = None
        self.alert= False
        self.menu1= True
        self.red_state = False
        self.cancel_email = False
        self.first_email_load = True
        self.is_viewing_inbox_email = False
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.smail_conf)

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
        self.insert_emails()
        self.email_timer = QTimer(self)
        self.email_timer.timeout.connect(self.insert_emails)
        self.email_timer.start(10000)
        self.allow_show_email = True

    def toggle_menu1(self):
        """
            Toggles between two main menus (MENU 1 and MENU 2) and updates buttons.
        """
        self.menu1 = not self.menu1
        # print(f"menu1 toggled to: {self.menu1}")
        self.clear_buttons()
        self.buttons_setup()

    def button_frame_setup(self):
        """
        Creates the frame for the top button bar.
        """
        self.button_frame = QFrame(self)
        self.button_frame.setStyleSheet(style.get_button_frame_style())
        self.button_layout = QHBoxLayout(self.button_frame)

    def clear_buttons(self):
        """
            Clears all buttons in the top bar.
        """
        while self.button_layout.count():
            child = self.button_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # noinspection PyUnresolvedReferences
    def buttons_setup(self):
        """
           Sets up the buttons in the top bar, including icons, text, and click actions.
        """
        button_9 = getattr(self.text_configuration, f"smail{self.language.capitalize()}SendToButton")
        button_menu1 = ["MENU 1", "EXIT", "Button 2", "Button 3", "Button 4"]
        button_menu2 = ["MENU 2", "Button 6", "Button 7", "Button 8", button_9]
        spacer_left = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        current_menu = button_menu1 if self.menu1 else button_menu2

        self.button_layout.addItem(spacer_left)
        for index, text in enumerate(current_menu):
            button = QPushButton(text, self.button_frame)

            #This was used to change the color of the "To/Komu" button to make it stand out, but it is now set to the same color.
            if not self.menu1 and index == 4:
                button.setStyleSheet(style.get_button_style(self.data_provider))
            else:
                button.setStyleSheet(style.get_button_style(self.data_provider))

            self.button_layout.addWidget(button, alignment=Qt.AlignCenter)

            if self.menu1:
                if index == 0:
                    button.clicked.connect(lambda _, btn=button, nb=None: self.decide_action_for_button(btn, nb))

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
                    button.clicked.connect(lambda _, btn=button, nb=None: self.decide_action_for_button(btn, nb))

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
                    if self.protection_level >= 2:
                        disabled_text = getattr(self.text_configuration,f"smail{self.language.capitalize()}SendToButtonDisabled")
                        button.setText(disabled_text)
                        button.setEnabled(False)
                    else:
                        button.clicked.connect(lambda _, btn=button, nb=7: self.decide_action_for_button(btn, nb))

        self.button_layout.setSpacing(10)
        self.button_layout.addItem(spacer_right)
        self.button_layout.setContentsMargins(10, 12, 10, 10)

    def alert_buttons(self, alert=True):
        """
        Changes button colors to visually indicate an alert state.
        Restores the original button colors after the alert ends.
        """
        if not hasattr(self, "original_button_styles"):
            self.original_button_styles = {}

        for i in range(self.button_layout.count()):
            widget = self.button_layout.itemAt(i).widget()

            if isinstance(widget, QPushButton):
                if alert:
                    if widget not in self.original_button_styles:
                        self.original_button_styles[widget] = widget.styleSheet()

                    widget.setStyleSheet(style.get_button_style(self.data_provider, normal=False))
                else:
                    if widget in self.original_button_styles:
                        widget.setStyleSheet(self.original_button_styles[widget])

    def image_configuration(self):
        """
        Loads and sets button icons based on the configuration.
        If an icon is missing, it falls back to an empty QIcon().
        """
        try:
            self.img = style.images(self.data_provider)
            exitPath =  "/home/vboxuser/senior-os/sconf/icons/exit.png"

            def load_icon(image_path_str, width=413, height=531):
                """
                Loads an icon from an absolute file path.
                If not found, returns an empty icon to prevent UI issues.
                """
                image_path = Path(image_path_str)

                if image_path.exists():
                    pixmap = QPixmap(str(image_path))
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio,
                                               transformMode=Qt.SmoothTransformation)
                        return QIcon(pixmap)
                return QIcon()

            self.exit_image = load_icon(exitPath)
            self.person1_image = load_icon(self.img[0])
            self.person2_image = load_icon(self.img[1])
            self.person3_image = load_icon(self.img[2])
            self.person4_image = load_icon(self.img[3])
            self.person5_image = load_icon(self.img[4])
            self.person6_image = load_icon(self.img[5])

        except Exception as e:
            print(f"Error: Failed loading images, application will continue without icons.\n{e}")
    
    def smail_conf(self): 
        self.stacked_widget.setCurrentIndex(1)
    def exit_app(self):
        """
            Closes the application.
        """
        self.close()
        QApplication.quit()
        QTimer.singleShot(5000, self.force_quit)

    def force_quit(self):
        """
            Forces the application to close if it doesn't exit properly.
        """
        # print("Force quitting the application after timeout...")
        subprocess.run(["kill", "-9", str(os.getpid())])

    def left_panel_setup(self):
        """
            Sets up the left panel containing the email list.
        """
        self.left_panel = QFrame(self)
        self.left_panel.setStyleSheet(style.get_left_panel_style())
        self.left_panel.setFixedWidth(259)

        # Email list
        self.inbox_list_label = QLabel(getattr(self.text_configuration, f"smail{self.language.capitalize()}InboxLabel"), self.left_panel)
        self.inbox_list_label.setFixedHeight(22)
        self.inbox_list_label.setStyleSheet(style.get_text_style())
        self.inbox_list = QListWidget(self.left_panel)
        self.inbox_list.setStyleSheet(style.get_inbox_style())
        self.inbox_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inbox_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Layout for the left panel
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.addWidget(self.inbox_list_label)
        self.left_panel_layout.addWidget(self.inbox_list)

    def right_panel_setup(self, recipient_email="", show_sender_info=True):
        """
            Sets up the right panel for viewing email details or composing a new email.
        """
        subject_label = getattr(self.text_configuration, f"smail{self.language.capitalize()}SubjectLabel")
        recipient_label = getattr(self.text_configuration, f"smail{self.language.capitalize()}RecipientLabel")
        message_label = getattr(self.text_configuration, f"smail{self.language.capitalize()}MessageLabel")
        from_label = getattr(self.text_configuration, f"smail{self.language.capitalize()}From")

        # Right panel setup
        self.right_panel = QFrame(self)
        self.right_panel.setStyleSheet(style.get_right_panel_style())

        if show_sender_info:
            self.sender_info_label_1 = QLabel(f"{from_label}", self.right_panel)
            self.sender_info_label_1.setFixedHeight(22)
            self.sender_info_label_1.setStyleSheet(style.get_text_style())
            self.sender_info_label_2 = QTextEdit(self.right_panel)
            self.sender_info_label_2.setReadOnly(True)
            self.sender_info_label_2.setFixedHeight(114)
            self.sender_info_label_2.setStyleSheet(style.get_sender_info_label())

        # Recipient info
        else:
            self.recipient_info_label_1 = QLabel(f"{recipient_label}", self.right_panel)
            self.recipient_info_label_1.setFixedHeight(22)
            self.recipient_info_label_2 = QTextEdit(recipient_email or "", self.right_panel)
            self.recipient_info_label_2.setReadOnly(True)
            self.recipient_info_label_2.setFixedHeight(40)
            self.recipient_info_label_3 = QLabel(f"{subject_label}",self.right_panel)
            self.recipient_info_label_3.setFixedHeight(22)
            self.recipient_info_label_4 = QTextEdit("", self.right_panel)
            self.recipient_info_label_4.setReadOnly(True)
            self.recipient_info_label_4.setFixedHeight(40)
            self.recipient_info_label_1.setStyleSheet(style.get_text_style())
            self.recipient_info_label_2.setStyleSheet(style.get_label_style())
            self.recipient_info_label_3.setStyleSheet(style.get_text_style())
            self.recipient_info_label_4.setStyleSheet(style.get_label_style())

        # Layout for the email content
        self.email_content_label_1 = QLabel(f"{message_label}",self.right_panel)
        self.email_content_label_1.setFixedHeight(22)
        self.email_content_label_1.setStyleSheet(style.get_text_style())
        self.email_content_label_2 = QTextEdit(self.right_panel)
        self.email_content_label_2.setReadOnly(True)
        self.email_content_label_2.setStyleSheet(style.get_email_content_label())
        scrollbar = QScrollBar(self.email_content_label_2)
        scrollbar.setStyleSheet(style.get_scrollbar())
        self.email_content_label_2.setVerticalScrollBar(scrollbar)

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

    def activate_show_email(self, event):
        """
            Enables email viewing when an email is clicked.
        """
        self.allow_show_email = True

    def insert_emails(self):
        """
        Starts a background thread to load and insert emails into the inbox list.
        """

        if self.first_email_load:
            language, _ = style.get_language(self.data_provider)
            loading_inbox_text = getattr(self.text_configuration, f"smail{language.capitalize()}LoadingInbox",
                                         "Loading inbox...")
            self.inbox_list.clear()
            self.inbox_list.addItem(loading_inbox_text)

        self.thread = QThread()
        self.worker = EmailLoaderWorker(self.data_provider, self.text_configuration)
        self.worker.moveToThread(self.thread)

        # Připojení signálů
        self.thread.started.connect(self.worker.run)
        self.worker.emails_loaded.connect(self.on_emails_loaded)
        self.worker.error_occurred.connect(self.on_email_error)
        self.worker.emails_loaded.connect(lambda *_: self.thread.quit())
        self.worker.emails_loaded.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_emails_loaded(self, emails, subjects):
        previous_emails = getattr(self, "reversed_list", [])

        self.emails, self.subjects = self.filter_unapproved_emails(emails, subjects)
        self.reversed_list = list(zip(self.emails[::-1], self.subjects[::-1]))

        if previous_emails != self.reversed_list:
            self.inbox_list.clear()
            # print("Clearing the listbox")
            self.all_emails = [(email_content, subject, "safe") for email_content, subject in self.reversed_list]

            for email_content, subject, _ in self.all_emails:
                name = style.get_email_sender(email_content.split("\n")[1])
                self.inbox_list.addItem(f"{name} - {subject}")

            self.inbox_list.itemSelectionChanged.connect(self.show_email)
            self.allow_show_email = True
            self.first_email_load = False

    def on_email_error(self, message):
        print(f"Email load error: {message}")

    def filter_unapproved_emails(self, emails, subjects):
        """
        Filters incoming emails based on the protection level.
        - PL2: Blocks emails from unknown contacts.
        """
        protection_level = self.protection_level
        approved_contacts_raw = self.data_provider.get_smail_configuration().emailContactsV2
        approved_contacts = []

        for entry in approved_contacts_raw:
            for key, value in entry.items():
                if key.startswith("email"):
                    approved_contacts.append(value.lower().strip())

        filtered_emails = []
        filtered_subjects = []

        for email, subject in zip(emails, subjects):
            sender_email = style.get_sender_email(email.split("\n")[1])
            sender_email = sender_email.lower().strip()

            if protection_level >= 2 and sender_email not in approved_contacts:
                continue

            filtered_emails.append(email)
            filtered_subjects.append(subject)

        return filtered_emails, filtered_subjects

    def show_email(self):
        """
            Displays the content of the selected email in the right panel.
        """
        if not self.allow_show_email:
            return

        if hasattr(self,
                   'email_content_label_2') and self.email_content_label_2.toPlainText() and not self.is_viewing_inbox_email:
            if not self.cancel_email:
                self.cancel_email = True
                self.alert_unconfirmed_email()
                return
            else:
                self.cancel_email = False
                # print("Rozpracovaný email byl zrušen.")
                self.clear_email_fields()


        if hasattr(self, 'last_selected_button') and self.last_selected_button is not None:
            if not sip.isdeleted(self.last_selected_button):
                self.last_selected_button.setStyleSheet(style.get_button_style(self.data_provider))
            self.last_selected_button = None

        selected_items = self.inbox_list.selectedItems()
        if not selected_items:
            return

        try:
            selected_index = self.inbox_list.currentRow()
        except IndexError:
            # print("Index out of range.")
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
        self.is_viewing_inbox_email = True

    def configure_message_area(self, email_content, email_subject, email_sender, email_date):
        """
            Configures the right panel to display the selected email.
        """
        self.right_panel.setParent(None)
        self.right_panel_setup(show_sender_info=True)
        self.bottom_layout.addWidget(self.right_panel, stretch=1)


        simplified_content = email_content
        if "Message not delivered" in email_content or "Mail Delivery Subsystem" in email_sender:
            recipient_email_match = re.search(r"to\s+([\w\.-]+@[\w\.-]+)", email_content)
            if recipient_email_match:
                recipient_email = recipient_email_match.group(1)
                simplified_content = getattr(self.text_configuration,
                                             f"smail{self.language.capitalize()}UndeliveredEmail").format(
                    recipient_email=recipient_email)

        self.email_content_label_2.setReadOnly(False)
        self.email_content_label_2.clear()
        self.email_content_label_2.append(simplified_content)
        self.email_content_label_2.setReadOnly(True)

        self.sender_info_label_2.setReadOnly(False)
        self.sender_info_label_2.clear()
        self.sender_info_label_2.append(f"{email_subject}\n{email_sender}\n{email_date}")
        self.sender_info_label_2.setReadOnly(True)

    def update_email_content(self, subject: str, content: str):
        """
            Updates the email subject and content in the right panel.
        """
        self.email_content_label_1.setText(subject)
        self.email_content_label_2.setText(content)

    def decide_action_for_button(self, button, recipient_index=None):
        """
        Handles actions when a button is clicked, such as selecting a recipient.
        """
        try:
            self.inbox_list.clearSelection()

            def is_draft_email():
                """Check if there's an unfinished email that is not an inbox email."""
                return bool(self.email_content_label_2.toPlainText()) and not self.is_viewing_inbox_email

            if recipient_index is None:
                if self.cancel_email:
                    self.cancel_email = False
                    self.clear_email_fields()
                    self.toggle_menu1()
                elif is_draft_email():
                    self.cancel_email = True
                    self.alert_unconfirmed_email()
                else:
                    self.toggle_menu1()
                return

            if self.last_selected_button == button:
                if self.cancel_email:
                    self.cancel_email = False
                self.disable_fields_for_sending()
                QTimer.singleShot(100, self.send_email_status)
                return

            if is_draft_email():
                if not self.cancel_email:
                    self.cancel_email = True
                    self.alert_unconfirmed_email()
                    return
                self.cancel_email = False
                self.clear_email_fields()

            self.fill_recipient(recipient_index)
            self.last_selected_button_index = recipient_index
            self.last_selected_button = button
            self.cancel_email = False
            self.is_viewing_inbox_email = False

        except Exception as e:
            print(f"An error occurred in decide_action_for_button: {e}")

    def fill_recipient(self, index):
        """
            Fills in the recipient email address based on the user's selection.
        """
        try:
            if hasattr(self, 'last_selected_button') and self.last_selected_button is not None:
                if not sip.isdeleted(self.last_selected_button):
                    self.last_selected_button.setStyleSheet(style.get_button_style(self.data_provider))
            sender = self.sender()

            if sender is not None and not sip.isdeleted(sender):
                sender.setStyleSheet(style.get_button_style(self.data_provider, highlight=True))
                self.last_selected_button = sender
            recipient_email = ""
            if 1 <= index <= 6:
                recipient_email = style.search_mail(index, self.data_provider)
            elif index == 7:
                recipient_email = ""

            self.right_panel.setParent(None)
            self.right_panel_setup(recipient_email, False)
            self.bottom_layout.addWidget(self.right_panel, stretch=1)
            self.email_content_label_2.setReadOnly(False)
            self.recipient_info_label_4.setReadOnly(False)
            self.recipient_info_label_2.setReadOnly(False)

        except Exception as e:
            print(f"An error occurred in fill_recipient: {e}")

    def is_valid_email(self, email):
        """
            Checks if an email address is valid.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def send_email_status(self):
        """
            Verifies if all required fields are filled and sends the email.
        """
        missing_info = False
        colors = self.color_scheme
        alert_color = colors["alert_color"]
        default_color = colors["default_color"]

        (login, password, smtp_server, smtp_port, imap_server, imap_port) = style.load_credentials(self.data_provider)

        recipient = self.recipient_info_label_2.toPlainText().strip()
        subject = self.recipient_info_label_4.toPlainText().strip()
        content = self.email_content_label_2.toPlainText().strip()
        approved_contacts = self.data_provider.get_smail_configuration().emailContactsV2
        approved_contacts_raw = self.data_provider.get_smail_configuration().emailContactsV2

        approved_contacts = []
        for entry in approved_contacts_raw:
            for key, value in entry.items():
                if key.startswith("email"):
                    approved_contacts.append(value.lower().strip())

        if self.protection_level >= 2 and recipient.lower() not in approved_contacts:
            self.alert_missing_text(self.recipient_info_label_2, default_color, alert_color)
            return

        if not recipient:
            # print("Recipient was not specified.")
            self.alert_missing_text(self.recipient_info_label_2, default_color, alert_color)
            missing_info = True

        elif not self.is_valid_email(recipient):
            # print("Invalid recipient email address.")
            self.alert_missing_text(self.recipient_info_label_2, default_color, alert_color)
            missing_info = True

        if not subject:
            # print("Email subject is missing.")
            # self.alert_missing_text(self.recipient_info_label_4, default_color, alert_color)
            missing_info = False


        if not content:
            # print("Email content is missing.")
            self.alert_missing_text(self.email_content_label_2, default_color, alert_color)
            missing_info = True

        if missing_info:
            return

        if self.contains_sensitive_data(content):
            if not self.sensitive_content_warning_displayed:
                self.alert_sensitive_data()
                self.sensitive_content_warning_displayed = True
                return
            else:
                # print("Sensitive content warning acknowledged. Proceeding with email send.")
                pass


        if self.sensitive_content_warning_displayed:
            success = send_email_with_guardian_copy(
                recipient, subject, content, login, password, smtp_server, smtp_port, self.guardian_email
            )
            # print(f"Poslano i pro guardiana: {self.guardian_email}")
        else:
            success = send_email(
                recipient, subject, content, login, password, smtp_server, smtp_port
            )

        if success == 1:
            self.send_email_success()
        else:
            self.send_email_fail()

    def send_email_success(self):
        """
            Displays a success message when the email is sent.
        """
        self.sensitive_content_warning_displayed = False
        colors = self.color_scheme
        highlight_color = colors["highlight_color"]
        default_color = colors["default_color"]


        self.recipient_info_label_4.clear()
        self.email_content_label_2.clear()

        height = self.email_content_label_2.height()
        line_height = 32
        total_lines = max(1, height // line_height)
        middle_line = total_lines // 2
        padding = "\n" * (middle_line - 2)

        self.email_content_label_2.insertPlainText(padding)
        self.email_content_label_2.insertPlainText(getattr(self.text_configuration, f"smail{self.language.capitalize()}EmailSent"))
        self.email_content_label_2.setAlignment(Qt.AlignCenter)
        current_style = style.get_email_content_label()
        self.email_content_label_2.setStyleSheet(current_style + f"""
                background-color: {highlight_color};
                font-size: 32px;  
                font-weight: bold;  
            """)
        self.email_content_label_2.setReadOnly(True)

        QTimer.singleShot(5000, lambda: self.clear_content_entry(default_color, 3))

    def send_email_fail(self):
        """
            Displays an error message if the email fails to send.
        """
        self.sensitive_content_warning_displayed = False
        colors = self.color_scheme
        alert_color = colors["alert_color"]
        default_color = colors["default_color"]

        self.alert_buttons(alert=True)

        self.recipient_info_label_2.clear()
        self.recipient_info_label_4.clear()
        self.email_content_label_2.clear()

        height = self.email_content_label_2.height()
        line_height = 32
        total_lines = max(1, height // line_height)
        middle_line = total_lines // 2
        padding = "\n" * (middle_line - 2)

        self.email_content_label_2.insertPlainText(padding)
        self.email_content_label_2.insertPlainText(getattr(self.text_configuration, f"smail{self.language.capitalize()}EmailFail"))
        self.email_content_label_2.setAlignment(Qt.AlignCenter)
        current_style = style.get_email_content_label()
        self.email_content_label_2.setStyleSheet(current_style + f"""
                        background-color: {alert_color};
                        font-size: 32px;  
                        font-weight: bold;  
                    """)
        self.email_content_label_2.setReadOnly(True)

        QTimer.singleShot(5000, lambda: self.clear_content_entry(default_color, 3))
        QTimer.singleShot(4000, lambda: self.alert_buttons(alert=False))

    def update_recipient_content(self):
        """
            Updates the recipient email address in the right panel.
        """
        try:
            if not hasattr(self, 'last_selected_button_index') or self.last_selected_button_index is None:
                # print("No valid last selected button index found.")
                return
            if not (1 <= self.last_selected_button_index <= 6):
                return
            recipient_email = style.search_mail(self.last_selected_button_index, self.data_provider)
            self.recipient_info_label_2.setPlainText(recipient_email)

        except Exception as e:
            print(f"An error occurred in update_recipient_content: {e}")

    def clear_content_entry(self, default_color, idx):
        """
            Clears specific text fields (recipient, subject, email body).
        """
        self.email_content_label_2.setReadOnly(False)
        self.recipient_info_label_2.setReadOnly(False)
        self.recipient_info_label_4.setReadOnly(False)

        if idx == 3:
            self.email_content_label_2.clear()
        elif idx == 2:
            # self.recipient_info_label_2.clear()
            self.update_recipient_content()
        elif idx == 1:
            self.recipient_info_label_4.clear()

        self.email_content_label_2.setStyleSheet(style.get_email_content_label() + f"background-color: {default_color};")
        self.recipient_info_label_2.setStyleSheet(style.get_label_style() + f"background-color: {default_color};")
        self.recipient_info_label_4.setStyleSheet(style.get_label_style() + f"background-color: {default_color};")

    def alert_missing_text(self, entry, default_color, select_color):
        """
            Highlights a field if required information is missing.
        """
        if entry == self.recipient_info_label_4:
            entry.setStyleSheet(style.get_label_style() + f"background-color: {select_color};")
            QTimer.singleShot(2000, lambda: self.clear_content_entry(default_color, 1))

        elif entry == self.recipient_info_label_2:
            entry.setStyleSheet(style.get_label_style() + f"background-color: {select_color};")
            QTimer.singleShot(2000, lambda: self.clear_content_entry(default_color, 2))

        elif entry == self.email_content_label_2:
            entry.setStyleSheet(style.get_email_content_label() + f"background-color: {select_color};")
            QTimer.singleShot(2000, lambda: self.clear_content_entry(default_color, 3))

    def disable_fields_for_sending(self):
        """
        Disables text fields and buttons after sending an email to prevent further edits.
        """
        colors = self.color_scheme
        grey_color = colors["grey_color"]

        self.recipient_info_label_2.setReadOnly(True)
        self.recipient_info_label_4.setReadOnly(True)
        self.email_content_label_2.setReadOnly(True)

        self.recipient_info_label_2.setStyleSheet(style.get_label_style() + f"background-color: {grey_color};")
        self.recipient_info_label_4.setStyleSheet(style.get_label_style() + f"background-color: {grey_color};")
        self.email_content_label_2.setStyleSheet(style.get_email_content_label() + f"background-color: {grey_color};")

        self.set_buttons_enabled(False)
        QTimer.singleShot(4000, lambda: self.set_buttons_enabled(True))

    def set_buttons_enabled(self, enabled: bool):
        for i in range(self.button_layout.count()):
            widget = self.button_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setEnabled(enabled)

    def contains_sensitive_data(self, content):
        """
        Checks if the email contains sensitive data such as passwords, credit card numbers,
        bank details, or other confidential information.

        Returns:
            bool: True if sensitive data is detected, False otherwise.
        """
        sensitive_keywords = [
            # Password-related terms (CZ, EN, DE)
            "heslo", "password", "passwort",
            "uživatelské jméno", "username", "benutzername",
            "přihlašovací jméno", "login", "anmeldung",
            "přihlašovací údaje", "credentials", "anmeldeinformationen",
            "tajné heslo", "secret password", "geheimes passwort",

            # Banking & Payment Terms (CZ, EN, DE)
            "banka", "bank", "bank",
            "bankovní účet", "bank account", "bankkonto",
            "číslo účtu", "account number", "kontonummer",
            "směrovací číslo", "routing number", "bankleitzahl",
            "číslo karty", "card number", "kartennummer",
            "platební karta", "payment card", "zahlungskarte",
            "kreditní karta", "credit card", "kreditkarte",
            "debetní karta", "debit card", "debitkarte",
            "cvc", "cvv", "cvc",  # Common across all languages
            "ověřovací kód", "security code", "sicherheitscode",
            "pin", "pin code", "pin-code", "pin-kode",

            # Identity & Government Documents (CZ, EN, DE)
            "rodné číslo", "birth number", "geburtsnummer",
            "osobní číslo", "personal ID", "personalausweisnummer",
            "identifikační číslo", "identification number", "identifikationsnummer",
            "občanský průkaz", "ID card", "personalausweis",
            "cestovní pas", "passport", "reisepass",
            "řidičský průkaz", "driver's license", "führerschein",
            "sociální pojištění", "social security", "sozialversicherung",
            "daňové identifikační číslo", "tax ID", "steueridentifikationsnummer",

            # Two-Factor Authentication (CZ, EN, DE)
            "ověřovací kód", "verification code", "verifizierungscode",
            "dvoufázové ověření", "two-factor authentication", "zwei-faktor-authentifizierung",
            "jednorázový kód", "one-time password", "einmaliges passwort",
            "bezpečnostní kód", "security code", "sicherheitscode",

            # Crypto & Digital Wallets (CZ, EN, DE)
            "bitcoin", "bitcoin", "bitcoin",
            "ethereum", "ethereum", "ethereum",
            "kryptoměna", "cryptocurrency", "kryptowährung",
            "krypto peněženka", "crypto wallet", "krypto-brieftasche",

            # Business Identification Numbers (CZ, EN, DE)
            "ičo", "business ID", "firmenidentifikationsnummer",
            "dič", "tax ID", "steueridentifikationsnummer",
            "evidenční číslo", "registration number", "registrierungsnummer",
            "firemní účet", "business account", "geschäftskonto",

            # Personal Information (CZ, EN, DE)
            "telefonní číslo", "phone number", "telefonnummer",
            "emailová adresa", "email address", "e-mail-adresse",
            "adresa bydliště", "home address", "wohnadresse",
            "ulice", "street", "straße",
            "město", "city", "stadt",
            "psč", "zip code", "postleitzahl"
            ]

        sensitive_patterns = [
            # Credit card numbers (VISA, Mastercard, Amex, Discover)
            r"\b4[0-9]{3}([ -]?[0-9]{4}){2}[0-9]{1,4}\b",  # VISA
            r"\b5[1-5][0-9]{2}([ -]?[0-9]{4}){3}\b",  # Mastercard
            r"\b3[47][0-9]{2}([ -]?[0-9]{4}){3}\b",  # American Express
            r"\b6(?:011|5[0-9]{2})([ -]?[0-9]{4}){3}\b",  # Discover

            # Social Security Numbers (USA)
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN (Social Security Number USA)

            # Czech and Slovak ID numbers
            r"\b\d{6}/\d{3,4}\b",  # Czech/Slovak personal ID (Rodné číslo)

            # Czech, German, and International tax numbers
            r"\b[A-Z]{2}\d{8,12}\b",  # VAT numbers (CZ12345678, DE123456789)
            r"\b\d{9}\b",  # Basic 9-digit tax ID
            r"\b\d{2}-\d{7}\b",  # US EIN (Employer Identification Number)
            r"\b\d{11}\b",  # German Steuer-ID (11 digits)

            # International Bank Account Number (IBAN)
            r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b",  # IBAN (CZ6508000000192000145399, DE89370400440532013000)

            # Bitcoin and Ethereum wallet addresses
            r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",  # Bitcoin address
            r"\b0x[a-fA-F0-9]{40}\b",  # Ethereum address

            # Phone numbers (general)
            r"\b\+?\d{1,3}?[ -]?\(?\d{2,4}\)?[ -]?\d{3,4}[ -]?\d{3,4}\b",  # International phone numbers
            r"\b\d{3}[ -]?\d{3}[ -]?\d{3}\b",  # Czech phone numbers (e.g., 123 456 789 or 123-456-789)

            # ZIP codes (Czech, German, USA)
            r"\b\d{3} ?\d{2}\b",  # Czech ZIP code (123 45)
            r"\b\d{5}(-\d{4})?\b",  # US ZIP code (12345 or 12345-6789)
            r"\b\d{5}\b",  # German PLZ (postal code)

            # Driver's license numbers (CZ, DE, USA)
            r"\b\d{9}\b",  # Czech driver's license (9 digits)
            r"\b[0-9A-Z]{1,2}-\d{4}-\d{6}-\d{2}\b",  # German Führerschein number
            r"\b[A-Z]{1,2}\d{6,8}\b",  # US driver's license (varies by state)

            # Passport numbers (CZ, DE, International)
            r"\b[A-Z0-9]{8,9}\b",  # Czech passport number (e.g., 123456789 or ABC123456)
            r"\b[A-Z]{1,2}[0-9]{7}\b",  # German passport (e.g., C01234567)
            r"\b[A-Z]{2}[0-9]{7}\b",  # International passport format

            # Health insurance numbers (CZ, DE, US)
            r"\b\d{6} ?\d{4}\b",  # Czech health insurance numbers (123456 7890)
            r"\b\d{10,12}\b",  # German Krankenversicherung ID (10-12 digits)
            r"\b\d{3}-\d{2}-\d{4}\b",  # US Medicare number (similar to SSN)

            # Two-factor authentication codes (OTP, 2FA)
            r"\b\d{6}\b",  # 6-digit one-time password (OTP, 2FA)
        ]

        for keyword in sensitive_keywords:
            if keyword.lower() in content.lower():
                return True

        for pattern in sensitive_patterns:
            if re.search(pattern, content):
                return True

        return False

    def alert_sensitive_data(self):
        """
            Warns the user that the email contains sensitive data.
        """
        colors = self.color_scheme
        alert_color = colors["alert_color"]
        default_color = colors["default_color"]

        original_content = self.email_content_label_2.toPlainText()

        self.alert_buttons(alert=True)

        self.email_content_label_2.setReadOnly(False)
        self.email_content_label_2.clear()
        self.email_content_label_2.setStyleSheet(style.get_email_content_label() + f"background-color: {alert_color};")

        height = self.email_content_label_2.height()
        line_height = 32
        total_lines = max(1, height // line_height)
        middle_line = total_lines // 2
        padding = "\n" * (middle_line - 2)

        self.email_content_label_2.insertPlainText(padding)
        self.email_content_label_2.insertPlainText(getattr(self.text_configuration, f"smail{self.language.capitalize()}SensitiveContentWarning"))
        self.email_content_label_2.setAlignment(Qt.AlignLeft)
        current_style = style.get_email_content_label()
        self.email_content_label_2.setStyleSheet(current_style + f"""
                        background-color: {alert_color};
                        font-size: 32px;  
                        font-weight: bold;
                        padding-left: 30px;  
                    """)
        self.email_content_label_2.setReadOnly(True)

        QTimer.singleShot(4000, lambda: self.restore_original_content(original_content, default_color))
        QTimer.singleShot(4000, lambda: self.alert_buttons(alert=False))
        self.cancel_email = True
        self.set_buttons_enabled(False)
        QTimer.singleShot(4000, lambda: self.set_buttons_enabled(True))

    def restore_original_content(self, original_content, default_color):
        """
            Restores the original email content after a sensitive data warning.
        """
        self.email_content_label_2.clear()
        self.email_content_label_2.setStyleSheet(
            style.get_email_content_label() + f"background-color: {default_color};")
        self.recipient_info_label_2.setStyleSheet(
            style.get_label_style() + f"background-color: {default_color};")
        self.recipient_info_label_4.setStyleSheet(
            style.get_label_style() + f"background-color: {default_color};")
        self.email_content_label_2.insertPlainText(original_content)
        self.email_content_label_2.setReadOnly(False)
        self.recipient_info_label_2.setReadOnly(False)
        self.recipient_info_label_4.setReadOnly(False)

    def alert_unconfirmed_email(self):
        """
            Warns the user when they try to leave without sending an email.
        """
        colors = self.color_scheme
        alert_color = colors["alert_color"]
        default_color = colors["default_color"]

        original_content = self.email_content_label_2.toPlainText()

        self.alert_buttons(alert=True)

        self.email_content_label_2.setReadOnly(False)
        self.email_content_label_2.clear()
        self.email_content_label_2.setStyleSheet(style.get_email_content_label() + f"background-color: {alert_color};")

        height = self.email_content_label_2.height()
        line_height = 32
        total_lines = max(1, height // line_height)
        middle_line = total_lines // 2
        padding = "\n" * (middle_line - 2)

        self.email_content_label_2.insertPlainText(padding)
        self.email_content_label_2.insertPlainText(getattr(self.text_configuration, f"smail{self.language.capitalize()}UnconfirmedEmailWarning"))
        self.email_content_label_2.setAlignment(Qt.AlignLeft)
        current_style = style.get_email_content_label()
        self.email_content_label_2.setStyleSheet(current_style + f"""
                        background-color: {alert_color};
                        font-size: 32px;  
                        font-weight: bold; 
                        padding-left: 30px 
                    """)
        self.email_content_label_2.setReadOnly(True)

        QTimer.singleShot(4000, lambda: self.restore_original_content(original_content, default_color))
        QTimer.singleShot(4000, lambda: self.alert_buttons(alert=False))
        self.sensitive_content_warning_displayed = False
        self.set_buttons_enabled(False)
        QTimer.singleShot(4000, lambda: self.set_buttons_enabled(True))

    def clear_email_fields(self):
        """
            Clears all fields in the email.
        """
        self.recipient_info_label_2.clear()
        self.recipient_info_label_4.clear()
        self.email_content_label_2.clear()

class EmailLoaderWorker(QObject):
    emails_loaded = pyqtSignal(list, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, data_provider, text_configuration):
        super().__init__()
        self.data_provider = data_provider
        self.text_configuration = text_configuration

    def run(self):

        try:
            login, password, smtp_server, smtp_port, imap_server, imap_port = style.load_credentials(self.data_provider)
            language, text = style.get_language(self.data_provider)

            emails, subjects = read_mail(login, password, imap_server, imap_port, language, text, self.data_provider)

            if emails is None or subjects is None:
                self.error_occurred.emit("Failed to load emails.")
                return

            self.emails_loaded.emit(emails, subjects)

        except Exception as e:
            self.error_occurred.emit(str(e))