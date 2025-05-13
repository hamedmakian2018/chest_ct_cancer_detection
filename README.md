# Chest CT Cancer Detection

This repository contains an end-to-end MLOps pipeline for chest cancer detection using chest CT scans. The goal is to develop a robust and automated system for model training, deployment, and monitoring. This README provides detailed steps to set up the environment, follow development practices, and understand the project structure.

# First Commit:
Project Setup

1. Creating the Repository

Repository Name: chest_ct_cancer_detection (any name you want)

Visibility: Public

Additional Settings:

Include a README file.

Add a .gitignore file configured for Python projects.

Select the MIT license for open usage.
--------------------------------------------------------------------------------

# Second commit

2. Cloning the Repository

Copy the HTTPS link from the GitHub repository.

Open a terminal (CMD or PowerShell) in the desired folder location. You can quickly do this in Windows by typing cmd in the folder's address bar.

Clone the repository using the following command:

git clone <repository_https_url>

3. Setting Up the Python Environment

Create a virtual environment:(CMD or PowerShell)

python -m venv .venv (or any name you like instead .venv)



Open the project in VSCode:(CMD or PowerShell)

code .

Activate the environment:(VSCode terminal)

.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/MacOS

Exclude the virtual environment from version control by adding the following line to .gitignore:

.venv/

Pre-Commit Configuration:

To ensure code quality, we use black for code formatting and isort for sorting imports. We leverage pre-commit to automatically apply these checks before every commit.

Installation and Configuration:

Install required libraries:(VSCode terminal)

pip install -r dev-requirements.txt

Configure pre-commit hooks:(VSCode terminal)

pre-commit install

Pre-Commit Setup Files:

dev-requirements.txt: Lists required packages (black, isort, pre-commit).

pyproject.toml: Configures black formatting and isort.

.pre-commit-config.yaml: Configures black and isort hooks.

Project Structure:

src/: Contains all the main source code.

__init__.py: Initializes the folder as a Python package.

iterative_functions.py: Defines utility functions, such as folder creation.

logger.py: Implements structured logging.

Commit Workflow: (VSCode terminal)

git add .

Commit changes:(VSCode terminal)

git commit -m "Added logger functionality"

Push to GitHub:(VSCode terminal)

git push origin main
--------------------------------------------------------------------------------
# Third Commit
