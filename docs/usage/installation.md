# Installation and Setup

This document provides step-by-step instructions for installing and setting up the application. It aims to guide users through the process of interacting with the product, from cloning the repository to running the application. The outline is as seen below:

## Outline
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Installation

Follow the steps below to get started using the free lunch application:
1. ### Clone the Repository
In your terminal, paste and run the command `git clone https://github.com/hngx-org/Metal-food-backend.git`.

2. ### Navigate to the Project Directory
Run the command `cd Metal-food-backend`.

3. ### Set up a Virtual Envirionment
You can (optionally) set up and activate a virtual environment. To achieve this, run the following command: `python3 -m venv venv`. This command uses Python 3 to create a virtual environment named venv, which will be created inside your project directory.

4. ### Activate the Virtual Environment
To activate the virtual environment, run the appropriate command based on your operating system.
- **On Windows**, run: `venv\Scripts\activate`.
- **On Linux or macOS**, run: `source venv/bin/activate`.
    At any point, you can deactivate the virtual environment by simply running the command: `deactivate`.

4. **Install dependencies**
To ensure you have the required packages needed to start using the application, run the command `pip install -r requirements.txt` to install the required dependencies.

## Running the Application

Once you have completed the steps above, you can start the application by running the command: `python manage.py runserver`
This will set up the development server.
To access the application, visit the url `http://localhost:8000`.

*For detailed instructions on using the application and performing various tasks, see the full documentation for this project at [metal food docs](documentation.md).*

## Troubleshooting

If you encounter issues at any stage:
1. Properly review the instructions hitherto outlined to ensure you accurately executed each step.
2. Ensure you are running an up-to-date version of your operating system.
3. Identify error codes or messages and search for any provided solutions online.
4. If issues persist, do not hesitate to send us a [mail](#).
