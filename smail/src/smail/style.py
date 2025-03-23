
import os
import re
import sys
from pathlib import Path
#from PIL import Image, ImageQt
script_directory = Path(__file__).parent
parent_directory = script_directory.parent
sys.path.append(str(parent_directory))

def get_button_style(data_provider=None, normal=True, highlight=False):
    """
        Returns style for buttons based on their state:
        - Normal (grey)
        - Highlight(confirmation)
        - Red (alert)
    """
    button_width, button_height = 244, 107
    button_position = "center"

    colors = get_color_scheme(data_provider)
    if highlight:
        background_color = colors["highlight_color"]
    elif normal:
        background_color = colors["dark_grey_color"]
    else:
        background_color = colors["alert_color"]

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
              background-color: {colors["highlight_color"]};
          }}
          QPushButton:hover {{
              background-color: {colors["highlight_color"]};  
          }}
          QPushButton::icon {{
              alignment: {button_position};
          }}
      """


def get_color_scheme(data_provider=None):
    """
    Returns the application's color scheme, using values from global_config if available.
    If the values are empty ("") or "000000", it falls back to default colors.
    """
    default_colors = {
        "default_color": "#FFFFFF",
        "highlight_color": "#48843F",
        "alert_color": "#F90000",
        "dark_grey_color": "#949494",
        "grey_color": "#D3D3D3"
    }

    if data_provider is None:
        return default_colors

    try:
        global_config = data_provider.get_global_configuration()
        highlight_raw = global_config.highlightColor.strip() if global_config.highlightColor else ""
        alert_raw = global_config.alertColor.strip() if global_config.alertColor else ""

        def format_color(color_value, default):
            if not color_value or color_value == "000000":
                return default
            if not color_value.startswith("#"):
                color_value = "#" + color_value
            return color_value

        return {
            "default_color": default_colors["default_color"],
            "highlight_color": format_color(highlight_raw, default_colors["highlight_color"]),
            "alert_color": format_color(alert_raw, default_colors["alert_color"]),
            "dark_grey_color": default_colors["dark_grey_color"],
            "grey_color": default_colors["grey_color"]
        }

    except Exception as e:
        print(f"Error loading color scheme: {e}. Using default colors.")
        return default_colors


def get_button_frame_style():
    """
        Returns the style for the button bar frame.
    """
    return """
        background-color: transparent;
        border: none;
        height: 107px;
    """

def get_frame_style():
    """
        Returns the style for the frame.
    """
    return """
        background-color: #E7E7E7;
        border-radius: 5px;
    """

def get_bottom_layout_style():
    """
        Returns the style for the bottom layout frame.
    """
    return """
        background-color: #FFFFFF;        
        border: 3px solid #000000;        
        border-radius: 3px;                           
        min-width: 1260px;                
        min-height: 580px;                
    """

def get_left_panel_style():
    """
            Returns the style for the left layout frame.
    """
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
    """
                Returns the style for the right layout frame.
    """
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
    """
        Returns the style for text labels.
    """
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
    """
        Returns style for the sender info label in an email.
    """
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
    """
        Returns style for the email content field.
    """
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

def get_scrollbar():
    """
        Returns style for vertical scrollbars in the UI.
        - Removes default scrollbar background.
        - Uses a custom grey-colored handle.
    """
    return """
        QScrollBar:vertical {
            border: none;  
            background: transparent;  
            width: 12px;  
            margin: 0px 0px 0px -5px;  
        }
        QScrollBar::handle:vertical {
            background: #949494;  
            min-height: 20px;  
            border-radius: 4px;  
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;  
            background: none;  
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;  
        }
    """

def get_inbox_style():
    """
        Returns style for the email list in the left panel.
    """
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
    """

def get_text_style():
    """
        Returns style for general text elements (labels, headers, etc.).
    """
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
    """
        Constructs the absolute path to a file inside a given folder.
        - Used for loading resources dynamically.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(root_dir, folder, file)
    return file_path

def load_credentials(data_provider):
    """
        Loads email login credentials from the configuration provider.
        - Returns email, password, SMTP/IMAP server info.
    """
    smail_config = data_provider.get_smail_configuration()
    login = smail_config.seniorEmail
    password = smail_config.seniorPassword
    smtp_server = smail_config.smtpServer
    smtp_port = smail_config.smtpPort
    imap_server = smail_config.imapServer
    imap_port = smail_config.imapPort

    return login, password, smtp_server, smtp_port, imap_server, imap_port

def images(data_provider):
    """
        Retrieves the list of image filenames from the configuration provider.
    """
    smail_config = data_provider.get_smail_configuration()
    return smail_config.emailPictures

def search_mail(id, data_provider):
    """
        Retrieves an email contact based on the given ID.
        - Ensures the ID is within the valid range.
    """
    smail_config = data_provider.get_smail_configuration()
    email_contacts = smail_config.emailContacts
    if 1 <= id <= len(email_contacts):
        return email_contacts[id - 1]
    else:
        raise ValueError(f"Invalid id: {id}. Valid range is 1 to {len(email_contacts)}.")

def get_language(data_provider):
    """
        Retrieves the current language setting from the configuration provider.
        - Returns the selected language and its corresponding text configuration.
    """
    global_config = data_provider.get_global_configuration()
    language = global_config.language.lower()
    smail_config = data_provider.get_smail_configuration()
    text = smail_config.languageSet
    return language, text

def get_protection_level(data_provider):
    """
        Retrieves the current protection level setting from the configuration provider.
    """
    global_config = data_provider.get_global_configuration()
    protection_level = global_config.protectionLevel
    return protection_level

def get_email_sender(email_string):
    """
        Extracts the sender's name from an email string.
        - Handles different email formats like:
          - "From: <email@example.com>"
          - "From: Name Surname <email@example.com>"
          - "From: email@example.com"
    """
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

def get_sender_email(email_string):
    """
    Extracts only the sender's email address from an email header.
    Supports formats:
      - "From: <email@example.com>"
      - "From: Name Surname <email@example.com>"
      - "From: email@example.com"

    Returns:
        str: Extracted email address.
    """
    start_index = email_string.find(": ") + 2

    email_match = re.search(r'<([^<>@]+@[^<>@]+)>', email_string)
    if email_match:
        sender_email = email_match.group(1).strip()
        return sender_email

    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email_string)
    if email_match:
        sender_email = email_match.group(0).strip()
        return sender_email

    return "Unknown Email"

def get_guardian_email(data_provider):
    """
       Retrieves the guardian email address from the configuration provider.
       - Used for sending a copy of emails to a caregiver.
    """
    smail_config = data_provider.get_global_configuration()
    email = smail_config.careGiverEmail
    return email

def resend_active(data_provider):
    """
        Checks if the phishing warning resend feature is enabled.
        - Returns:
          - Boolean (True if enabled)
          - Senior email address
          - Guardian email address
    """
    smail_config = data_provider.get_smail_configuration()
    active = smail_config.sendPhishingWarning
    smail = smail_config.seniorEmail
    gmail = smail_config.careGiverEmail

    return active == True, smail, gmail
