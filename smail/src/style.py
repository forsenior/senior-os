
import os
import sys
from pathlib import Path
#from PIL import Image, ImageQt
script_directory = Path(__file__).parent
parent_directory = script_directory.parent
sys.path.append(str(parent_directory))


def get_button_style(normal=True, green=False):
    button_width, button_height = 244, 107
    button_position = "center"

    if green:
        background_color = "#48843F"
    elif normal:
        background_color = "#949494"
    else:
        background_color = "#F90000"

    return f"""
          QPushButton {{
              background-color: {background_color};
              border: 1px solid #797979;
              border-radius: 3px;
              color: #FFFFFF;
              font-family: Inter;
              font-size: 40px;
              text-align: {button_position};
              width: {button_width}px;
              height: {button_height}px;
          }}
          QPushButton:pressed {{
              background-color: #48843F;
          }}
          QPushButton::icon {{
              alignment: {button_position};
          }}
      """


def get_color_scheme():
    return {
        "default_color": "#FFFFFF",
        "green_color": "#48843F",
        "alert_color": "#F90000",
        "dark_grey_color": "#949494",
        "grey_color": "#D3D3D3"
    }



def get_button_frame_style():
    return """
        background-color: transparent;
        border: none;
        height: 107px;
    """


def get_frame_style():
    return """
        background-color: #E7E7E7;
        border-radius: 5px;
    """


def get_bottom_layout_style():
    return """
        background-color: #FFFFFF;        
        border: 3px solid #000000;        
        border-radius: 3px;                           
        min-width: 1260px;                
        min-height: 580px;                
    """


def get_left_panel_style():
    return """
        background-color: #FFFFFF;  
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border-left: 3px solid #000000;
        border-top: 3px solid #000000;
        border-bottom: 3px solid #000000;
        border-right: none;
        margin-left: 10px;
        margin-top: 0px;
        margin-bottom: 10px;
        padding-bottom: 5px;
        padding-left: 5px;
    """


def get_right_panel_style():
    return """
        QFrame {
            background-color: #FFFFFF;  
            border-bottom-right-radius: 3px;
            border-top-right-radius: 3px;
            border-right: 3px solid #000000;
            border-top: 3px solid #000000;
            border-bottom: 3px solid #000000;
            border-left: none;
            margin-right: 10px;
            margin-top: 0px;
            margin-bottom: 10px;
            padding-right: 10px;
            padding-bottom: 5px;
        }
    """


def get_label_style():
    return """
        border: 1px solid black;             
        border-radius: 8px;
        padding: 0px;
        padding-top: 5px;
        padding-left: 5px;
        margin: 0px;
        text-align: left;
        font-family: 'Inter';
        font-size: 16px;
    """


def get_sender_info_label():
    return """
         border: 1px solid black;             
         border-radius: 8px;
         padding: 0px;
         padding-top: 20px;
         padding-left: 5px;
         margin: 0px;
         text-align: left;
         font-family: 'Inter';
         font-size: 16px;
     """


def get_email_content_label():
    return """
        border: 1px solid black;             
        border-radius: 8px;
        padding: 0px;
        padding-top: 5px;
        padding-left: 5px;
        margin: 0px;
        text-align: left;
        font-family: 'Inter';
        font-size: 16px;
    """


def get_inbox_style():
    return """
        QListWidget {
            border: 1px solid black;             
            border-radius: 8px;
            padding: 5px;
            font-family: 'Inter';
            font-size: 16px;
            margin: 0px;
        }
        QListWidget::item {
            padding: 3px;
            margin-bottom: 2px;
        }
        QListWidget::item:selected {
            background-color: #f0f0f0;
            color: black;
        }

        
        QListWidget QScrollBar:vertical {
            background-color: #F0F0F0;
            width: 16px;
            margin: 0px;
            border: 1px solid #D3D3D3;
        }
        QListWidget QScrollBar::handle:vertical {
            background-color: #C0C0C0;
            min-height: 20px;
            border-radius: 8px;
        }

        
        QListWidget QScrollBar:horizontal {
            background-color: #F0F0F0;
            height: 16px;
            margin: 0px;
            border: 1px solid #D3D3D3;
        }
        QListWidget QScrollBar::handle:horizontal {
            background-color: #C0C0C0;
            min-width: 20px;
            border-radius: 8px;
        }
    """


def get_text_style():
    return """
        QLabel {
            font-family: 'Inter';
            font-size: 16px;
            color: #000000;
            text-align: left;
            border: none;
            margin: 0px;
            padding: 0px;
        }
    """


def get_path(folder, file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(root_dir, folder, file)
    return file_path


def load_credentials(data_provider):
    smail_config = data_provider.get_smail_configuration()
    login = smail_config.seniorEmail
    password = smail_config.seniorPassword
    smtp_server = smail_config.smtpServer
    smtp_port = smail_config.smtpPort
    imap_server = smail_config.imapServer
    imap_port = smail_config.imapPort

    return login, password, smtp_server, smtp_port, imap_server, imap_port


################################
# def load_show_url(path):
#     data = load_json_file(path)
#     show = data["show_url"]
#     return show
################################


def images(data_provider):
    smail_config = data_provider.get_smail_configuration()
    return smail_config.emailPicturesPath


def search_mail(id, data_provider):
    smail_config = data_provider.get_smail_configuration()
    email_contacts = smail_config.emailContacts
    if 1 <= id <= len(email_contacts):
        return email_contacts[id - 1]
    else:
        raise ValueError(f"Invalid id: {id}. Valid range is 1 to {len(email_contacts)}.")

def get_language(data_provider):
    global_config = data_provider.get_global_configuration()
    language = global_config.language.lower()
    smail_config = data_provider.get_smail_configuration()
    text = smail_config.languageSet
    return language, text



def get_email_sender(email_string):

    start_index = email_string.find(": ") + 2

    # Check if the string is in format: "Od: <email@seznam.cz>"
    if start_index < len(email_string) - 1 and email_string[start_index] == "<":
        end_index = email_string.find(">", start_index)
        if end_index != -1:
            email_address = email_string[start_index + 1:end_index].strip()
            sender_name = email_address.split("@")[0]
            return sender_name
    end_index = email_string.find("<")

    # Check if the string is in format: "Od: Name Surname <email@seznam.cz>"
    if start_index != -1 and end_index != -1:
        sender_name = email_string[start_index:end_index].strip()
        if '"' in sender_name:
            start_index = email_string.find('"') + 1
            end_index = email_string.find('"', start_index)
            if start_index != -1 and end_index != -1:
                sender_name = email_string[start_index:end_index].strip()

        return sender_name

    # If the format is "Od: email@seznam.cz" , extract name differently
    else:
        tokens = email_string.split(" ")
        if len(tokens) > 1:
            extracted_name = tokens[1]
            name = extracted_name.split("@")[0]
            return name

def get_guardian_email(data_provider):
     smail_config = data_provider.get_smail_configuration()
     email = smail_config.careGiverEmail
     return email

def resend_active(data_provider):
    smail_config = data_provider.get_smail_configuration()
    active = smail_config.sendPhishingWarning
    smail = smail_config.seniorEmail
    gmail = smail_config.careGiverEmail

    return active == True, smail, gmail
