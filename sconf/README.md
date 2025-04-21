# SCONF
## Running the Application in ISO

    Download the latest ISO from the repository.

    Create a new virtual machine in your preferred virtualization environment (e.g., VirtualBox, VMware, or QEMU), and attach the downloaded ISO.

    This ISO is a Linux-based system.

Once the virtual machine starts, the application should launch automatically.
If it doesn't, run the following command in the terminal:
```
sconf
```
Alternatively, you can start the SCONF application using SRUN from the OS's main screen.
Running the Application from an IDE

## Extending the SCONF

To get started with SCONF from source, follow these steps to clone the repository and install dependencies.
### Option A: Running with Poetry
1. Install Poetry

SCONF uses Poetry for dependency management and packaging.
If Poetry isn’t installed, follow this installation guide.
2. Clone the Repository and Install Dependencies manually

#### Clone the project repository
```git clone https://github.com/forsenior/senior-os```

#### Navigate into the project directory
```cd sconf```

#### Build and install dependencies using Poetry
```
poetry build
poetry install

Repeat these steps for the srun directory as well:

cd ..
cd srun
poetry build
poetry install
```

3. Run the Application
```poetry run sconf```

### Option B: Running with an IDE (e.g., PyCharm)
Set Up Poetry in Your IDE, which can be found for PyCharm [here](https://www.jetbrains.com/help/pycharm/poetry.html)

#### Clone the project repository
```
git clone https://github.com/forsenior/senior-os
```

#### Navigate into the project directory
```
cd sconf
```

#### Install dependencies manually
```
pip install -r requirements.txt
```

To run the app, open the ``sconf_run.py`` file in your IDE and execute it.

### Generating ``config.json``

To generate the config.json for SCONF and related applications:

1. Follow the installation guide above and run the SCONF application.

2. The config.json file is automatically generated in your HOME directory at startup.

Alternatively, to generate it manually:

1. Create a .sconf folder in your HOME directory.

2. Add a config.json file inside it.

3. Navigate to sconf/src/sconf/configuration/models and copy the default values and attribute names into the JSON file format.

Or use the older ``config.json`` file in the root of the SCONF folder

## Adding new configuration options
To add the new configuration option into the config.json file follow these steps:
1. Locate the desired configuration model for the application in the ``sconf/src/sconf/configuration/models`` 
2. In the model add the new field with its type and default value
```
    newValue: int = 156
```
the new value will look like this in the model
```
@dataclass
class GlobalConfiguration:
    language: str = "en"
    colorMode: str = "light"
    alertColor: str = "F90000"
    highlightColor: str = "48843F"
    protectionLevel: int = 1
    careGiverEmail: str = "ai.pythonbot@gmail.com"x
    newValue: int = 156
```
3. Once the new value is added delete the old ``config.json`` file and re-run the SCONF

Notes

    Make sure you are using Python 3.12 to avoid unexpected compatibility issues.

    If you're unsure about which command to use, prefer running through poetry run to ensure dependency resolution.