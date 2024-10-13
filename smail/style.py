import logging
import json
import os
import sys
from pathlib import Path
from PyQt5.QtGui import QPixmap, QIcon, QImage
script_directory = Path(__file__).parent
parent_directory = script_directory.parent
sys.path.append(str(parent_directory))
from smail.template.guiTemplate import resolutionMath

logger = logging.getLogger(__file__)

def get_path(folder, file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    file_path = os.path.join(root_dir, folder, file)

    return file_path

def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return 0
    except Exception as error:
        logger.error(f"An unexpected error occurred while loading data from {file_path}", exc_info=True)
        return -1

def load_button_colors():
    data = load_json_file(get_path("sconf", "config.json"))
    default_color = data["GUI_template"]["buttons_unselected"]
    select_color = data["GUI_template"]["buttons_selected"]
    return default_color, select_color


def load_credentials(path):
    data = load_json_file(path)
    credentials = data["credentials"]
    login = credentials["username"]
    password = credentials["password"]
    smtp_server = credentials["smtp_server"]
    smtp_port = credentials["smtp_port"]
    imap_server = credentials["imap_server"]
    imap_port = credentials["imap_port"]

    return login, password, smtp_server, smtp_port, imap_server, imap_port

def load_show_url(path):
    data = load_json_file(path)
    show = data["show_url"]
    return show

def load_email_content(path):
    data = load_json_file(path)
    show = data["email_content"]
    return show

def font_config():
    data = load_json_file(get_path("sconf", "config.json"))
    font_family = data["GlobalConfiguration"]["fontFamily"]
    font_size = data["GlobalConfiguration"]["fontSize"]
    font_thickness = data["GlobalConfiguration"]["fontThickness"]

    font_info = font_family + " " + str(font_size) + " "+ font_thickness
    return font_info

def app_color():
    data = load_json_file(get_path("sconf", "config.json"))
    bg = data["GUI_template"]["app_frame"]
    return bg

def images():
    data = load_json_file(get_path("sconf", "SMAIL_config.json"))
    images = data["images"]
    return images


def image_config(name, btn_height):
    data = images()
    path = data[name]
    image = QImage(path)
    original_width = image.width()
    original_height = image.height()
    height_ratio = btn_height / original_height
    new_width = int(original_width * height_ratio)
    new_height = int(original_height * height_ratio)
    resized_image = image.scaled(new_width, new_height)
    pixmap = QPixmap.fromImage(resized_image)
    icon = QIcon(pixmap)
    return icon


def search_mail(id):
    data = load_json_file(get_path("sconf", "SMAIL_config.json"))
    emails = data["emails"]
    email = emails[f"Person{id}"]
    return email


def get_language():
    data = load_json_file(get_path("sconf", "config.json"))
    language = data["GlobalConfiguration"]["language"].lower()
    data = load_json_file(get_path("sconf", "SMAIL_config.json"))
    text = data["text"]
    return language, text

def get_alert_color():
    data = load_json_file(get_path("sconf", "config.json"))
    color = data["GlobalConfiguration"]["alertColor"]
    return color


def height_config(parent):
    font_base = font_config()
    font = font_base.split(" ")
    font_size = int(font[1])

    if font_size >= 36:
        scaling_factor = 0.75
    elif font_size < 16:
        scaling_factor = 0.65
    else:
        scaling_factor = 0.7

    font_size_in_pixels = font_size / scaling_factor

    # Resolution info
    parent_height = parent.height()
    area_of_upper_widget = resolutionMath()[2]
    usable_height = parent_height - area_of_upper_widget

    # Calculating widget height
    number_of_lines_listbox = int((usable_height - font_size_in_pixels * 3) / font_size_in_pixels)
    number_of_lines_textarea = int((usable_height - font_size_in_pixels * 6) / font_size_in_pixels)

    return number_of_lines_listbox, number_of_lines_textarea

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


def get_guardian_email():
    # Reading configuration
    data = load_json_file(get_path("sconf", "SMAIL_config.json"))
    email = data["guardian_email"]
    return email

def resend_active():
    # Reading configuration
    data = load_json_file(get_path("sconf", "SMAIL_config.json"))
    active = data["resend_email"]
    smail = data["credentials"]["username"]
    gmail = data["guardian_email"]
    return active ==1, smail, gmail
