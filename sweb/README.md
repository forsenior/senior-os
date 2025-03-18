# 📖 Choose your language / Wählen Sie Ihre Sprache / Zvolte si jazyk

- [English](README.md)
- [Deutsch](README.de.md)
- [Čeština](README.cz.md)

# Web browser for the elderly and mentally disabled

## Application Overview

This project is a web browser tailored for seniors, built using PyQt5, with a strong emphasis on accessibility, simplicity, and security. 
Its goal is to create a more user-friendly environment for older adults by offering features such as improved text readability, intuitive navigation, 
audio support, multilingual options, and robust security measures to guard against phishing websites. 
Below is the design concept for the web browser:

## MENU1 Overview
MENU1 provides a user-friendly interface with four large, fixed-size buttons, designed for easy navigation, especially for seniors.

<img src="screens/sweb_screen_1.png" width="900" />

Button Actions:

1. MENU1 Button: Switches the menu bar to MENU2.
2. Exit Button: Closes the application.
3. Website Buttons (3): Open links to predefined websites.
   
## MENU2 Overview
MENU2 includes five buttons with the following functions:

<img src="screens/sweb_screen_2.png" width="900" />

Button Actions:

1. MENU2 Button: Switches the menu bar back to MENU1.
2. Website Buttons (3): Open links to predefined websites.
3. Search Button: Opens a search bar for user queries.

## Phishing Website Detection
This feature is the core of our app, alerting users if a website is potentially a phishing site.

<img src="screens/sweb_screen_3.png" width="900" />

- Phishing Warning: If the user enters a known phishing URL, the toolbar background changes to red to ensure easy visibility, especially for seniors.

More details on how the phishing detector works will be provided in the documentation.

## Installation

!!!Ensure you have Python3 or pip installed on your system.
Follow these steps to set up Web Browser in FEDORA operating system:

```bash
# Install required Python packages with dnf if using Fedora
sudo dnf install python3

# Clone project repository
git clone https://github.com/forsenior/senior-os

# Install requirements from the requirements.txt in sweb dir
py -m pip install -r requirements.txt

```
      

## The demonstration video

https://github.com/user-attachments/assets/88fbb138-6467-47d3-ad12-a0fb98515719




# How to Contribute
Feel free to submit pull requests or raise issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the MIT License.
