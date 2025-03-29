### 📖 Choose your language / Wählen Sie Ihre Sprache / Zvolte si jazyk

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
MENU1 provides a user-friendly interface with five large, fixed-size buttons, designed for easy navigation, especially for seniors.

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
- Below is a diagram illustrating the process of detecting phishing URLs.
<p align="center">
  <img src="screens/sweb_phishing.gif" width="70%" />
</p>
More details on how the phishing detector works will be provided in the documentation.

## Installation



### Launching the Application  

To launch the application, follow these steps:  

1. Download the latest ISO from the repository [here](https://github.com/forsenior/senior-os/releases).  
2. Create a new virtual machine in your preferred virtualization software (such as VirtualBox, VMware, or QEMU).  
3. Attach the downloaded ISO to the virtual machine or create a bootable USB flash drives. The ISO is based on a Linux distribution (Archie).  
4. Start the virtual machine. If the application does not launch automatically, open the terminal and run:  

   ```sh
   srun
   ```  

---

### Installation and Development Setup  

For easier modifications and a better overview of the application, follow these steps:  

#### Step 1: Install Poetry  

SWEB uses [Poetry](https://python-poetry.org/) for dependency management and packaging. If you don’t have Poetry installed, follow the official [installation guide](https://python-poetry.org/docs/#installation).  

#### Step 2: Clone the Repository and Install Dependencies  

Once Poetry is installed, proceed with the following:  

```sh
# Clone the project repository
git clone https://github.com/forsenior/senior-os  

# Navigate into the project directory
cd sweb  

# Build and install dependencies
poetry build  
poetry install  
```  

Repeat these steps for the `sconf` and `srun` directories as well:  

```sh
cd ..  
cd sconf  
poetry build  
poetry install  

cd ..  
cd srun  
poetry build  
poetry install  
```  

#### Running the Application  

To run SWEB, use:  

```sh
poetry run sweb  
```  

**Supported Python Versions:**  
This program is tested and optimized for **Python 3.12**.  
> [!NOTE]  
> Note: If you try to run the SWEB application independently, you may encounter an error due to the configuration file path. By default, config.json should be located at:
> "$HOME/$USER/.sconf/config.json"


      

## The demonstration video

https://github.com/user-attachments/assets/88fbb138-6467-47d3-ad12-a0fb98515719




# How to Contribute
Feel free to submit pull requests or raise issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the MIT License.
