"""
Written by: RYUseless
Edited by: Marxs
"""
import smail.template.configActions as JS
from screeninfo import get_monitors

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
         padding-top: 5px;
         padding-left: 5px;
         margin: 0px;
         text-align: left;
         font-family: 'Inter';
         font-size: 16px;
         line-height: 150%;
         vertical-align: middle;
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
        border: 1px solid black;             
        border-radius: 8px;
        padding: 0px;
        font-family: 'Inter';
        font-size: 16px;
        margin: 0px;
        padding: 5px;
        
    
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

def resolutionMath():
    _numOfScreen = JS.jsonRed('GlobalConfiguration', "numOfScreen")
    _screenWidth = get_monitors()[_numOfScreen].width
    _screenHeight = get_monitors()[_numOfScreen].height
    panelWidth = int(_screenWidth / JS.jsonRed('GUI_template', "width_divisor"))
    panelHeight = int(_screenHeight / JS.jsonRed('GUI_template', "height_divisor"))
    app_width = _screenWidth - panelWidth
    app_height = _screenHeight - panelHeight
    return _screenWidth, panelWidth, panelHeight, app_width, app_height



