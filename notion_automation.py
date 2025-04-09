import os
from notion_client import Client
from datetime import datetime

# Initialize the Notion client using the integration token from environment variables
notion = Client(auth=os.getenv("SECRET_TOKEN"))

# Database IDs from environment variables
TASKS_DATABASE_ID = os.getenv("TASKS_DATABASE_ID")
LOGS_DATABASE_ID = os.getenv("LOGS_DATABASE_ID")


def fetch_tasks(database_id):
    """Fetch tasks from the Notion database."""
    response = notion.databases.query(database_id=database_id)
    return response.get("results", [])

def delete_task(task):
    """Delete a task by archiving it if the 'Done' column is checked."""
    # Check if the "Done" property exists and is checked
    if task["properties"].get("Done", {}).get("checkbox", False):
        notion.pages.update(page_id=task["id"], archived=True)

def log_to_notion(database_id, message):
    """Log a message to the Notion logs database."""
    timestamp = datetime.now().isoformat()
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Timestamp": {"date": {"start": timestamp}},
            "Log Message": {"title": [{"text": {"content": message}}]},
        },
    )

def main():
    try:
        # Fetch tasks from the tasks database
        tasks = fetch_tasks(TASKS_DATABASE_ID)
        task_count = len(tasks)

        # Delete tasks
        for task in tasks:
            delete_task(task["id"])

        # Log the number of deleted tasks
        log_to_notion(LOGS_DATABASE_ID, f"{task_count} tasks were deleted successfully.")

    except Exception as e:
        # Log any errors to the logs database
        log_to_notion(LOGS_DATABASE_ID, f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()