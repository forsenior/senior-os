# SMAIL - Email client for elderly users

This email client is adapted for seniors in the age group of 90 years and more. 
The developed email client is easy to use and contains only features that a senior may need. 

## Environment for reading email messages
SMAIL has an environment specifically designed for reading email messages in a user-friendly way, with large, clear buttons and text.
![menu1](https://github.com/forsenior/senior-os/blob/main/sconf/style/style_images/smail_gui_style_menu_message_1.png)

## Environment for writing email messages
The environment for writing emails is as easy as possible, with predefined contacts available for convenience.
![menu2](https://github.com/forsenior/senior-os/blob/main/sconf/style/style_images/smail_gui_style_global.png)

## Warning when writing sensitive data
The application warns users when they are about to send sensitive information, adding an additional layer of security.
![alert](https://github.com/forsenior/senior-os/blob/main/sconf/style/style_images/smail_gui_style_menu_alert_1.png)

## Installation
To get started with SMAIL, follow these steps to clone the repository and install dependencies:
```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

cd smail

# Install requirements from the requirements.txt file
py -m pip install -r requirements.txt
```
Supported Python Versions: This program is tested and optimized for Python 3.12.

## Configuration requirement for SMAIL
To ensure proper functioning of the SMAIL email client, it is recomended to first edit configuration files (SOS-conf.json). 
During this process, enter your own email address and password to personalize the application. 
Default settings are available, but for enhanced security and personalization, using your own credentials is highly encouraged.

### Password generation for SMAIL
To connect to your Gmail account from a non-web environment, such as SMAIL app, you'll need to generate an app password. 
Follow these steps to obtain the app password:

1. Go to the Google account settings by visiting *Google Account*.

2. Navigate to the "Security" tab.

3. Under the "Signing in to Google" section, locate and select "Two-step verification".

4. After authenticating your identity, scroll down to the "App passwords" section.

5. Choose the option to generate a new app password.

6. Select the app or device for which you're generating the password.

7. Follow the prompts to generate the app password.

8. Copy the generated app password and use it in the SGIVE app to connect your email client to your Gmail account securely.

If you cant find the correct section use this link: [App passwords](https://myaccount.google.com/apppasswords)

## Starting the SMAIL

To launch the application, follow these steps:

1. Open your preferred IDE such as PyCharm or any other suitable development environment.

2. Navigate to the smail directory

3. Open the smail.py file of the application.

4. Ensure that all necessary dependencies are installed ([Installation](#installation)).

5. Before executing the application, ensure that you have set up the necessary configurations and generated the required app password for connection, as outlined in the previous section.

6. Once everything is set up, run the application by clicking on the "Run" button within your IDE or execute the following commands:
```bash
cd smail
python smail.py
```
