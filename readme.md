<h1 align="center">The Workulator  

Tracking your work-hours with style</h1>

## Installation

Run the following command to install the project:

```text
    pip install 122-gruppenarbeit
```

## Development

It is recommended that the project is installed in a virtual environment.

- instructions for mac: <https://sourabhbajaj.com/mac-setup/Python/virtualenv.html>
- instructions for pc: <https://python.land/virtual-environments/virtualenv>

Run the following command to install the package in development mode:

```text
    pip install -e /path-to-directory-that-has-the-setup.py-file
```

## Compiling the application

Install the project, then navigate to the root folder of the project in your terminal and install pyinstaller by executing the command:

```text
    pip install pyinstaller==5.13.2
```

Build the executable by running:

```text
    pyinstaller --onefile workulator.py --noconsole
```

The executable file "workulator.exe" can now be found in your dist folder.

## Performing manual backups

Navigate to /src/database in your terminal and execute the following command:

```
    chmod +x backup-bash.sh  
```

then run task_scheduler.py
