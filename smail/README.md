# SMAIL - Email client for elderly users

This email client is adapted for seniors in the age group of 90 years and more. 
The developed email client is easy to use and contains only features that a senior may need. 

## Environment for reading email messages
SMAIL has an environment specifically designed for reading email messages in a user-friendly way, with large, clear buttons and text.
![menu1](https://github.com/forsenior/senior-os/blob/f69c6886a6b1b831bbf55c9c162af55fd61f8e0e/smail/screens/smail_screen1_en.png)

## Environment for writing email messages
The environment for writing emails is as easy as possible, with predefined contacts available for convenience.
![menu2](https://github.com/forsenior/senior-os/blob/f69c6886a6b1b831bbf55c9c162af55fd61f8e0e/smail/screens/smail_screen2_en.png)

## Confirmation of Successful Email Sending
After successfully sending an email, the application displays a confirmation message to inform the user that their email has been sent.
![alert](https://github.com/forsenior/senior-os/blob/f69c6886a6b1b831bbf55c9c162af55fd61f8e0e/smail/screens/smail_email_send_en.png)

## Warning when sending sensitive data
The application warns users when they are about to send sensitive information, adding an additional layer of security.
![alert1](https://github.com/forsenior/senior-os/blob/f69c6886a6b1b831bbf55c9c162af55fd61f8e0e/smail/screens/smail_sensitive_data_alert_en.png)

## Warning when leaving unconfirmed email
The application warns users when they attempt to leave an unfinished email draft. Users are prompted to confirm whether they want to discard the email before proceeding.
![alert2](https://github.com/forsenior/senior-os/blob/f69c6886a6b1b831bbf55c9c162af55fd61f8e0e/smail/screens/smail_unconfirmed_email_en.png)

## 1) For launching the application, use the following procedure.
Download the latest ISO from the [repository](https://github.com/forsenior/senior-os/releases).
Create a new virtual machine in your chosen virtualization environment (such as VirtualBox, VMware, or QEMU), and add the downloaded ISO. 
This ISO is distributed as a Linux-based system.
Start the virtual environment, and if the application does not launch automatically, run the following command in the terminal:
```bash
srun
```

## 2) For easier modifications and an overview of the application, follow this procedure.

## Installation
To get started with SMAIL, follow these steps to clone the repository and install dependencies:

### Step 1: Install Poetry
SMAIL uses Poetry for dependency management and packaging. 
If you don't have Poetry installed, you will need to install it first. 
You can follow this [step-by-step guide on how to install Poetry](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0).

### Step 2: Clone Repository and Install Dependencies
After installing Poetry, you can continue with the following steps:

```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Navigate into the project directory
cd smail

# Build and install dependencies using Poetry
poetry build

poetry install
```
Repeat these steps for the *sconf* and *srun* directories as well (cd .. -> cd sconf -> poetry build -> poetr...): 
```bash
#Run this command in the directory with the same name:
poetry run srun
#Or you can use this command, after you set up configuration file:
poetry run smail
```
Supported Python Versions: This program is tested and optimized for Python 3.12.

## Configuration requirement for SMAIL

To ensure proper functioning of the SMAIL email client, it is recomended to first edit configuration files.
For temporary configuration, you can edit the main configuration file config.json, located in the home directory (For example: C:\Users\user\.sconf\config.json). 
If it is not present, copy or create a config.json file (The configuration file should be automatically created after running *srun*). 
However, for permanent settings that will work continuously, you need to modify the configuration file `smail_configuration.py` located in `sconf/src/sconf/models/`.
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

1. **Open your preferred IDE**  
   Open your preferred development environment, such as PyCharm or any other suitable IDE.

2. **Navigate to the smail directory**  
   Use your IDE's file explorer to navigate to the `smail` directory within the cloned repository.

3. **Open a terminal in this folder**  
   Make sure you have an active terminal session open in the `smail` directory.

4. **Ensure that all necessary dependencies are installed**  
   Make sure that all dependencies are properly installed. You can verify this by following the [Installation](#installation) instructions.

5. **Set up configurations and app password**  
   Before running the application, ensure that all configurations are set and that you have generated an app password as mentioned in the [Password generation](#password-generation-for-smail) section.

6. **Run the application**  
   Once everything is set up, you can start the application by running the command:
```bash
cd smail
poetry run smail
```
