# Project Name

Welcome to Synoptic! This README is designed to help you get started with coding quickly and easily.

## Installation

To install the required dependencies, follow these steps:

1. Make sure you have Python 12 installed on your system.
2. Fork the project and clone the fork to your local machine.
3. Navigate to the project directory.
4. Run the following command to install the dependencies from the `requirements.txt` file:

    ```shell
    pip install -r requirements.txt
    ```

## Usage with VS Code
I chose VS Code for this project since you probably want to learn it before pycharm becomes a paid product
1. you will need to install following extensions:

    - Ruff: [Installation instructions](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
    - Djlint: [Installation instructions](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
    - Docker: [Installation instructions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
    - Python: [Installation instructions](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## Project Structure

In this project, we are using the following technologies:

- [htmx](https://htmx.org/): A JavaScript library for AJAX interactions in the browser.
- [daisyUI](https://daisyui.com/): A CSS framework for rapidly building custom designs.
- [alpine.js](https://alpinejs.dev/): A lightweight JavaScript framework for building interactive web interfaces.

The project follows a standard Django project structure and consists of three apps: `manager`, `public`, and `sensor`. Here's a brief overview of each app:

### Manager App
The `manager` app is responsible for managing the charity manager that are able to login to the app.

### Public App
The `public` app handles the public-facing functionality of the project. It includes features such as public pages, user registration, and public APIs. This app is accessible to all users of the project.

### Sensor App
The `sensor` app deals with sensor-related functionality.

## Project Stack


Feel free to explore each app's directory for more details on their specific functionality and implementation.


## Making Language Specific Pages

`django-admin makemessages -a` to create/update django.po for the languages

`django-admin compilemessages -a` to compile the language for user submission.

> [!TIP]
> Make sure you are in the same directory as manage.py when running the above commands.

> [!NOTE] 
> This README was written with copilot so best not include it in final submission