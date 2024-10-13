import json
import os


def temporaryGetPath():
    currentDir = os.path.dirname(os.path.dirname(__file__))
    parentCurentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    confPath = os.path.join(parentCurentDir, "sconf")
    return confPath


def configExistCheck():
    pathToJsonConf = temporaryGetPath()
    if os.path.exists(pathToJsonConf):
        if os.path.isfile(os.path.join(pathToJsonConf,'config.json')):
            print("LOG: conf.json is already there, skipping")
            return True
        else:
            _jsonWrite()
            return True
    else:
        print("LOG: there is no path to the configuration file")
        return False


def _jsonWrite():
    # default json config
    dictionary = {
        'pathToConfig': {
            "path": "D:\\aTIT\\sos\\sconf"
        },
        'GlobalConfiguration': {
            "numOfScreen": 0,
            "language": "CZ",
            "alertSoundLanguage": "CZ",
            "colorMode": "Light",
            "alertColor": "#8B0000",
            "hoverColor": "#4b5946",
            "hoverColorLighten": "#7c8e76",
            "soundDelay": 5,
            "fontSize": 36,
            "controlFontSize": 70,
            "fontThickness": "bold",
            "fontFamily": "Helvetica",
        },
        "GUI_template": {
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "num_of_opt_buttons": 18,
            "padx_value": 5,
            "height_divisor": 4.5,
            "width_divisor": 5,
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00",
        },
        "careConf": {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": [
                "Global",
                "Mail",
                "Web",
                "Logs"
            ],
            "LanguageOptions": [
                "Czech",
                "English",
                "German"
            ],
            "GlobalFrameLabels": [
                "Display",
                "Language",
                "Sound language",
                "Colorscheme",
                "Alert color (in hex)",
                "Highlight color (in hex)",
                "Sound delay (in s)",
                "Toolbar font (in px)",
                "Widget font (in px)",
                "Font weight"
            ],
            "SMailFrameLabels": [
                "Senior email",
                "Senior password",
                "Email contacts (six)",
                "Pictures (six)",
                "Caregiver warning",
                "Caregiver email",
                "URL links in email"
            ],
            "SwebFrameLabels": [
                "Sender email",
                "Sender password",
                "Receiver email"
            ],
            "EntryOptions": [
                "alertColor",
                "hoverColor",
                "soundDelay",
                "controlFontSize",
                "fontSize"
            ]
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(f"{temporaryGetPath()}/config.json", "w+") as outfile:
        outfile.write(json_object)


def jsonRed(key, value):
    path = temporaryGetPath()
    if os.path.exists(path):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        print("LOG: there is no path to the configuration file")
        return

def jsonRed_upd(key, value):
    path = temporaryGetPath()
    if os.path.exists(path):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        print("LOG: there is no path to the configuration file")
        return