# Web browser for seniors

## Application Overview

This project is a web browser tailored for seniors, built using PyQt5, with a strong emphasis on accessibility, simplicity, and security. 
Its goal is to create a more user-friendly environment for older adults by offering features such as improved text readability, intuitive navigation, 
audio support, multilingual options, and robust security measures to guard against phishing websites. 
Below is the design concept for the web browser:

> [!NOTE]
> My Contribution to the Project:
> Please note that I did not design the application from scratch. My role is to modify and enhance the app, making it more user-friendly while improving its security features.

## Content
1. [Current state of the solution](#current-state)
2. [The demonstration video](#demo-video)


## Remove the audio from the application

Remove pygame package to disable  playing the sounds

```python
import math
import pygame   <----
import sys, os, json, getpass, socket
from datetime import datetime
----
----
# Initialization pygame mixer  for play sounds
pygame.mixer.init()  <----
# Sound control attribute

----
----

def play_sound_for_button(self, path_to_sound):    <----
# Ensure the file exists before playing it
       if not os.path.exists(path_to_sound):
            print(f"Sound file not found: {path_to_sound}")
            return
        try:
            # Load and play the sound file
            self.sound_mixer_control_for_button = pygame.mixer.Sound(path_to_sound)
            self.sound_mixer_control_for_button.play()
        except Exception as exc:
            print(f"Failed to play sound: {str(exc)}")

----
----

def toggle_url_toolbar(self):
        # Toggle visibility of the URL toolbar
        self.play_sound_for_button(self.path_to_url_music)   <----
        self.main_browser.setUrl(QUrl("about:blank"))
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())
        self.toolbar_space.setVisible(not self.toolbar_space.isVisible())
----
----
  
 if self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                self.play_sound_for_button(self.path_to_alert_phishing_music)   <----

----
----
  
elif self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                self.play_sound_for_button(self.path_to_alert_phishing_music)  <----

----
----

def setup_hover_sound_value(self, input_widget, hover_time,path_to_sound):  <----
        # Using Qtimer to set clock
        input_widget.hover_timer = QTimer()
        input_widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        input_widget.hover_timer.setSingleShot(True)
        input_widget.hover_timer.timeout.connect(lambda: self.play_sound_for_button(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        input_widget.installEventFilter(self)

----
----

def update_ui_audio(self):  <----
            self.setup_hover_sound_value(self.menu1_button,self.time_hover_button,self.language_translator.get_translated_audio("menu1"))
            self.setup_hover_sound_value(self.menu1Exit,self.time_hover_button,self.language_translator.get_translated_audio("menu1Exit"))
            self.setup_hover_sound_value(self.back_btn,self.time_hover_button,self.language_translator.get_translated_audio("menu1Back"))
            self.setup_hover_sound_value(self.menu1WWW1,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW1"))
            self.setup_hover_sound_value(self.menu1WWW2,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW2"))
            self.setup_hover_sound_value(self.menu2_button,self.time_hover_button,self.language_translator.get_translated_audio("menu2"))
            self.setup_hover_sound_value(self.menu2WWW3,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW3"))
            self.setup_hover_sound_value(self.menu2WWW4,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW4"))
            self.setup_hover_sound_value(self.menu2WWW5,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW5"))
            self.setup_hover_sound_value(self.menu2Address,self.time_hover_button,self.language_translator.get_translated_audio("menu2Address"))
            self.path_to_alert_phishing_music = self.language_translator.get_translated_audio("alert_phishing")
            self.path_to_url_music = self.language_translator.get_translated_audio("url")       
```


## Config the app to read the configuration from the sconf file.

It depends on the configuration file created, now the website will load the configuration from the json file.

---------------------------------------

## Current state of the solution
<a name="current-state"></a>

The following functionalities are already implemented:

 - [x] Remove the audio from the application
     - [x]  Remove pygame package to disable  playing the sounds
 - [ ] Config the app to read the configuration from the sconf file.

 - [ ] Menu text settings
    - [x] Font family: Inter (google font)
    - [x] Font size: 40px
    - [x] Font: Regular
    - [x] Font color: FFFFFF (hex) ??????
    - [x] Position: Center, Center
- [ ] Bar background (Normal State)
    - [ ] Bar fill: Transparent
    - [ ] Border fill Transparent
    - [ ] Border thickness 0px
    - [ ] Buttons (Normal State)
    - [ ] Button size (Minimal): 244x107 (WxH)
    - [ ] Button corner radius: 3px
    - [ ] Button border thickness: 1px
    - [ ] Button fill: 949494 (hex)
    - [ ] Border color: 797979 (hex)
    - [ ] Icon/Text position: Center/Center
    - [ ] Button margin: 10px, 10px, 10px, 12px (Left, Top, Right, Bottom)
    
- [ ] Bar bacground (Phishing State)
    - [ ] Bar fill: FF0000 (hex)
    - [ ] Border fill: F90000 (hex)
    - [ ] Border thickness: 1px
    - [ ] Buttons (Phishing State)
    - [ ] Button size (Minimal): 244x107 (WxH)
    - [ ] Button corner radius: 3px
    - [ ] Button border thickness: 1px
    - [ ] Button fill: F90000 (hex)
    - [ ] Border color: 797979 (hex)
    - [ ] Icon/Text position: Center, Center
    - [ ] Button margin: 10px, 10px, 10px, 12px (Left, Top, Right, Bottom)
    
- [ ] Enable sending mail through the terminal
> [!NOTE]
> Do not have enough info from the smail side


      

## The demonstration video
<a name="demo-video"></a>

# How to Contribute
Feel free to submit pull requests or raise issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the MIT License.
