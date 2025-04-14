import os
import logging
from notion_client import Client
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Conditionally load .env file only on Windows and locally
if os.name == "nt" and os.getenv("GITHUB_ACTIONS") is None:  # Windows and not in GitHub Actions
    from dotenv import load_dotenv
    load_dotenv()

# Initialize the Notion client using the integration token from environment variables
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
if not SECRET_TOKEN:
    raise EnvironmentError("SECRET_TOKEN is not set in the environment variables.")
notion = Client(auth=SECRET_TOKEN)

# Database IDs from environment variables
TASKS_DATABASE_ID = os.getenv("TASKS_DATABASE_ID")
LOGS_DATABASE_ID = os.getenv("LOGS_DATABASE_ID")
if not TASKS_DATABASE_ID or not LOGS_DATABASE_ID:
    raise EnvironmentError("TASKS_DATABASE_ID or LOGS_DATABASE_ID is not set in the environment variables.")


def fetch_tasks(database_id):
    """Fetch tasks from the Notion database."""
    try:
        response = notion.databases.query(database_id=database_id)
        return response.get("results", [])
    except Exception as e:
        logging.error(f"Error fetching tasks from database {database_id}: {e}")
        return []

def delete_task(task):
    """Delete a task by archiving it if the 'Done' column is checked."""
    try:
        logging.info(f"Processing task: {task}")

        # Check if the "Done" property exists and is checked
        if task["properties"].get("Done", {}).get("checkbox", False):
            notion.pages.update(page_id=task["id"], archived=True)
            logging.info(f"Task {task['id']} archived successfully.")
            return True  # Task was deleted
        else:
            logging.info(f"Task {task['id']} not marked as done. Skipping.")
            return False  # Task was not deleted
    except Exception as e:
        logging.error(f"Error processing task {task['id']}: {e}")
        return False  # Task was not deleted due to an error

def log_to_notion(database_id, message):
    """Log a message to the Notion logs database."""
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Timestamp": {"date": {"start": timestamp}},
                "Log Message": {"title": [{"text": {"content": message}}]},
            },
        )
        logging.info(f"Logged message to Notion: {message}")
    except Exception as e:
        logging.error(f"Error logging message to Notion: {e}")

def main():
    try:
        # Fetch tasks from the tasks database
        tasks = fetch_tasks(TASKS_DATABASE_ID)
        deleted_task_count = 0

        # Delete tasks
        for task in tasks:
            print(f"Fetched task: {task}")
            if delete_task(task): # Increment count only if the task was deleted
                deleted_task_count += 1

        # Log the number of deleted tasks
        log_to_notion(LOGS_DATABASE_ID, f"{deleted_task_count} tasks were deleted successfully.")
    except Exception as e:
        # Log any errors to the logs database
        log_to_notion(LOGS_DATABASE_ID, f"Error occurred: {str(e)}")
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()