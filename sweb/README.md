# Web browser for the elderly and mentally disabled

## Application Overview

This project is a web browser tailored for seniors, built using PyQt5, with a strong emphasis on accessibility, simplicity, and security. 
Its goal is to create a more user-friendly environment for older adults by offering features such as improved text readability, intuitive navigation, 
audio support, multilingual options, and robust security measures to guard against phishing websites. 
Below is the design concept for the web browser:

## MENU1 Overview
MENU1 provides a user-friendly interface with four large, fixed-size buttons, designed for easy navigation, especially for seniors.

<img src="https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB-screen-1.png" width="900" />

Button Actions:

1. MENU1 Button: Switches the menu bar to MENU2.
2. Exit Button: Closes the application.
3. Website Buttons (3): Open links to predefined websites.
   
## MENU2 Overview
MENU2 includes five buttons with the following functions:

<img src="https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB-screen-2.png" width="900" />

Button Actions:

1. MENU2 Button: Switches the menu bar back to MENU1.
2. Website Buttons (3): Open links to predefined websites.
3. Search Button: Opens a search bar for user queries.

## Phishing Website Detection
This feature is the core of our app, alerting users if a website is potentially a phishing site.

<img src="https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB-screen-3.png" width="900" />

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


**Changelog**

1. Removed the audio assistant successfully from the app.
2. Updated the app to read configurations from the configuration provider instead of directly from the JSON file.
3. Enabled background email sending using the secondary app, Smail.
4. Remove the logger 


## Challenges

1. Configuration Management
   
   We are still working on switching the app to retrieve all configuration parameters from the configuration provider instead of directly from JSON. Currently, about 80% of the parameters are successfully sourced from the provider.

2. Dependency Removal
   
   The goal is to remove all connections between **sweb** and **sgive** for improved modularity and independence.



      

## The demonstration video


https://github.com/user-attachments/assets/ab53a1bf-695f-4838-87d4-df7c224030bc



# How to Contribute
Feel free to submit pull requests or raise issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the MIT License.
