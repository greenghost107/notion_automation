## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Install the Dependencies](#install-the-dependencies)
- [Adding a Notion Integration and Connecting it to a Database](#adding-a-notion-integration-and-connecting-it-to-a-database)
- [Setting Up the .env File (For Local Run)](#setting-up-the-env-file-for-local-run)
- [Running the Script Locally](#running-the-script-locally)
- [Running the Script in GitHub Actions](#running-the-script-in-github-actions)
- [Logging](#logging)

### Overview
This project automates task management in a Notion database. It fetches tasks, deletes tasks marked as "Done," and logs the number of deleted tasks to a Notion logs database.

## Project Structure
The project is organized as follows:
```
notion_automation/
├── notion_automation.py       # Main script for automation
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables for local development (ignored by Git)
└── .github/
    └── workflows/
        └── notion_automation.yml  # GitHub Actions workflow automation
```

## Prerequisites
Python 3.10 or higher  
A Notion integration token with access to the required databases  
The following Python libraries:  
`notion-client`    
`python-dotenv` - for local run  

## Install the dependencies using:
```
pip install -r requirements.txt
```

## Adding a Notion Integration and Connecting it to a Database
__1. Create a Notion Integration__
- Go to the Notion Integrations page.
- Click + __New integration__.
- Enter a name for your integration (e.g., `Automation`).
- Select the workspace where the integration will be used.
- Click __Submit__ to create the integration.
- Copy the __Integration Token__ (you will use this as `SECRET_TOKEN` in your .env file or GitHub Secrets).

__2. Connect the Integration to a Database__
- Open the Notion database you want to connect to.
- Click the __three dots__ (`...`) in the top-right corner of the database.
- Select __Connections__.
- Under __Add connections__, search for your integration name (e.g., `Automation`) and click Invite.

## Setting Up the .env File (For Local Run)
The .env file is used to store environment variables for local development. It should be placed in the root directory of the project (notion_automation/) and should contain the following variables:
```
SECRET_TOKEN=your_notion_secret_token  
TASKS_DATABASE_ID=your_tasks_database_id  
LOGS_DATABASE_ID=your_logs_database_id  
```

Explanation of Variables  
- SECRET_TOKEN: The Notion integration token used to authenticate API requests.
- TASKS_DATABASE_ID: The ID of the Notion database containing tasks.
- LOGS_DATABASE_ID: The ID of the Notion database where logs will be stored.

## Running the Script Locally
1. Ensure the .env file is properly configured with the required variables.
2. Run the script:
```
python notion_automation.py
```

## Running the Script in GitHub Actions
The project includes a GitHub Actions workflow `(.github/workflows/notion_automation.yml)` to automate the script on a schedule. The workflow uses GitHub Secrets to securely store environment variables.

Required GitHub Secrets
- SECRET_TOKEN
- TASKS_DATABASE_ID
- LOGS_DATABASE_ID

To add GitHub Secrets, go to your repository's __Settings > Secrets and variables > Actions__. Click __New repository secret__, enter the name (e.g., `SECRET_TOKEN`) and value, then save it. Repeat for `TASKS_DATABASE_ID` and `LOGS_DATABASE_ID`.

## Logging
The script logs the number of tasks deleted to the Notion logs database. If an error occurs, the error message is also logged to the same database.