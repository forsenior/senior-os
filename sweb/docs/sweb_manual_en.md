# <p align="center">Instructions for using the SWEB</p>
## Controlling the application:
The application has a main control panel that contains 5 buttons per menu (10 buttons in total):  
 ![MENU_1](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu1.png)
 ![MENU_2](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu2_en.png)
1.	**Menu** - allows you to switch between two different parts of the application (Menu 1 and Menu 2).
2.	**Red button with white cross** - used to exit the application.
3.	**Buttons with website icons** - quick access to a specific website, one click and the website opens on the screen. 
4.	**Button "Search"** - opens a blank field where the user can enter any web address.

## Opening a Website
- **Protection Level 1: Basic Protection**
1. **Opening via Menu:** Click any button or icon in Menu 1/2 to directly open the website.
2. **Opening via Search:** Click the search button, enter your search text, and the input will be checked against a "blacklist" and phishing detection using a neural network.

- **Protection Level 2: Enhanced Protection**
1. **Opening via Menu:** Click any button or icon in Menu 1/2 to directly open the website.
2. **Opening via Search:** Click the search button, enter your search text, and the input will be verified against a whitelist. The system will only open URLs that match the input in the whitelist.
  
- **Protection Level 3: Maximum Protection**
1. **Opening via Menu:** Click any button or icon in Menu 1/2 to directly open the website.
2. **No Search:** The search button will be disabled, and search functionality is not available at this protection level.

## Phishing Detection Alert
- **Phishing Detection:**
   - Entering URL or Visiting a Site: When the user enters a URL or visits a website, the system checks if the URL is listed in the blacklist or if it is detected through the neural network for phishing.

- **Alert Mechanism:**
   - If a potential phishing threat is detected, the button on the menu bar will change color to red to alert the user about the potential danger.

- **Ignoring the Alert:**
   - If the user ignores the red alert and proceeds to enter any data on the website, the app will automatically send an email notification to the guardian to inform them about the suspicious activity.

 ![MENU_2](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_phishing_en.png)
