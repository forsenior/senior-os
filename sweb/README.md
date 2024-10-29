# Web browser for the elderly and mentally disabled

## Application Overview

This project is a web browser tailored for seniors, built using PyQt5, with a strong emphasis on accessibility, simplicity, and security. 
Its goal is to create a more user-friendly environment for older adults by offering features such as improved text readability, intuitive navigation, 
audio support, multilingual options, and robust security measures to guard against phishing websites. 
Below is the design concept for the web browser:

## MENU1 Overview
MENU1 provides a user-friendly interface with four large, fixed-size buttons, designed for easy navigation, especially for seniors.

<img src="https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB-screen-1.png" >

Button Actions:

1. MENU1 Button: Switches the menu bar to MENU2.
2. Exit Button: Closes the application.
3. Website Buttons (3): Open links to predefined websites.
   
## MENU2 Overview
<img src="https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB-screen-2.png" width="700" />

## Content of the second menu

### Installation
!!!Ensure you have Python3 or pip installed on your system.
Follow these steps to set up Web Browser in FEDORA operating system:
```bash
# Install required Python packages with dnf if using Fedora
sudo dnf install python3
sudo dnf install python3-qt5
sudo dnf install python3-qt5-webengine
sudo dnf install python3-pygame
pip3 install screeninfo
pip3 install yagmail

```

> [!NOTE]
> My Contribution to the Project:
> Please note that I did not design the application from scratch. My role is to modify and enhance the app, making it more user-friendly while improving its security features.

**Changelog**

1. Removed the audio assistant successfully from the app.
2. Updated the app to read configurations from the configuration provider instead of directly from the JSON file.
3. Enabled background email sending using the secondary app, Smail.
4. Faced challenges in migrating all configurations from JSON to the configuration provider.



---------------------------------------

## Current state of the solution





      

## The demonstration video


# How to Contribute
Feel free to submit pull requests or raise issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the MIT License.
