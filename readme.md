<h1 align="center">The Workulator  

Tracking your work-hours with style</h1>

# The Workulator

Welcome to The Workulator, your stylish companion for effortless work hour tracking.

## Purpose

The Workulator simplifies the process of monitoring and managing your work hours, providing a user-friendly interface for timekeeping. Whether you're a freelancer, remote worker, or simply looking to keep precise records of your professional activities, The Workulator is designed to enhance your experience with style and functionality.

## Key Features

- **Intuitive Timekeeping:** Easily track and manage your work hours with a straightforward interface.
- **Convenient Hotkeys:** Streamline your workflow with customizable hotkeys for quick actions.
- **Secure and Reliable:** Prioritizing your data's security, The Workulator employs robust measures to ensure the safety of your information.

Get started effortlessly and make your work hours count with The Workulator!


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

Navigate to the root folder of the project in your terminal and install pyinstaller by executing the command:

```text
    pip install pyinstaller
```

Build the executable by running:

```text
    pyinstaller --onefile workulator.py --noconsole
```

The executable file can now be found in your dist folder.

## Performing manual backups

Navigate to /src/database in your terminal and execute the following command:

```
    chmod +x backup-bash.sh  
```

then run task_scheduler.py


## Security

The Workulator application prioritizes security to ensure the protection of your data. Here are key aspects of our security measures:

### 1. Code Security

The application code undergoes regular reviews to identify and address any potential security concerns. Our team is dedicated to maintaining a secure codebase.

### 2. User Authentication

User authentication is implemented to safeguard access to sensitive features and data within the application.

### 3. Hotkey Security

The application incorporates hotkeys for convenience, such as adding time edit rows. These are designed to enhance user experience without compromising security.

### 4. Regular Updates

Keep your application up-to-date to benefit from the latest security enhancements and patches.

We are committed to providing a secure environment for your work hours tracking. If you have any security-related questions or concerns, please don't hesitate to contact us.
