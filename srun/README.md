# SRUN
## Running the Application in ISO

    Download the latest ISO from the repository.

    Create a new virtual machine in your preferred virtualization environment (e.g., VirtualBox, VMware, or QEMU), and attach the downloaded ISO.

    This ISO is a Linux-based system.

Once the virtual machine starts, the application should launch automatically.
If it doesn't, run the following command in the terminal:
```
srun
```

## Extending the SRUN

To get started with SRUN from source, follow these steps to clone the repository and install dependencies.
### Option A: Running with Poetry
1. Install Poetry

SCONF uses Poetry for dependency management and packaging.
If Poetry isn’t installed, follow this installation guide.
2. Clone the Repository and Install Dependencies manually

#### Clone the project repository
```git clone https://github.com/forsenior/senior-os```

#### Navigate into the project directory
```cd srun```

#### Build and install dependencies using Poetry
```
poetry build
poetry install

Repeat these steps for the other applications if need be directory as well:

cd ..
cd {smail, sweb, sconf}
poetry build
poetry install
```

3. Run the Application
```poetry run srun```

### Option B: Running with an IDE (e.g., PyCharm)
Set Up Poetry in Your IDE, which can be found for PyCharm [here](https://www.jetbrains.com/help/pycharm/poetry.html)

#### Clone the project repository
```
git clone https://github.com/forsenior/senior-os
```

#### Navigate into the project directory
```
cd srun
```

#### Install dependencies manually
```
pip install -r requirements.txt
```

To run the app, open the ``srun_run.py`` file in your IDE and execute it.

## Adding new application 
To add the new application into the runner follow these steps:
1. Go into the ``srun`` source directory
2. Open the data folder and locate the ``executables.py`` file
3. Add the new application as an executable

Once the application is added into the executables proceed into the ``ui/view/main_window_view.py`` and add the new UI tile and executable.

Notes

    Make sure you are using Python 3.12 to avoid unexpected compatibility issues.

    If you're unsure about which command to use, prefer running through poetry run to ensure dependency resolution.