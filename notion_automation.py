import os
import logging
import time
from notion_client import Client

# Configure logging
LOG_FILE = "notion_automation.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Function to delete logs older than 6 months
def delete_old_logs(log_file, months=6):
    if os.path.exists(log_file):
        # Get the current time and the file's modification time
        current_time = time.time()
        file_mod_time = os.path.getmtime(log_file)
        # Calculate the age of the file in seconds (6 months = ~180 days)
        six_months_in_seconds = months * 30 * 24 * 60 * 60
        if current_time - file_mod_time > six_months_in_seconds:
            os.remove(log_file)
            logging.info(f"Deleted old log file: {log_file}")
        else:
            logging.info(f"Log file is not older than {months} months: {log_file}")
    else:
        logging.info(f"Log file does not exist: {log_file}")

# Read secrets from environment variables
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

if not SECRET_TOKEN or not DATABASE_ID:
    logging.error("SECRET_TOKEN or DATABASE_ID environment variables are not set.")
    raise ValueError("SECRET_TOKEN or DATABASE_ID environment variables are not set.")

logging.info("Successfully retrieved environment variables.")

notion = Client(auth=SECRET_TOKEN)

# This will list pages your integration has access to
logging.info("Fetching accessible databases...")
response = notion.search(filter={"property": "object", "value": "database"})
for r in response["results"]:
    logging.info(f"Database ID: {r['id']}, Title: {r['title']}")

# Fetch database info
logging.info(f"Retrieving database info for DATABASE_ID: {DATABASE_ID}")
db_info = notion.databases.retrieve(database_id=DATABASE_ID)

# Print all column names and types
logging.info("Columns in the database:")
for name, prop in db_info["properties"].items():
    logging.info(f"- {name}: {prop['type']}")

def _remove_done_from_db():
    logging.info("Querying items marked as 'Done'...")
    # Query items where done is True
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Done",
                "checkbox": {
                    "equals": True
                }
            }
        }
    )["results"]

    logging.info(f"Found {len(results)} items marked as 'Done'. Archiving them...")
    # Delete each page
    for page in results:
        notion.pages.update(page["id"], archived=True)
        logging.info(f"Archived page with ID: {page['id']}")

if __name__ == "__main__":
    logging.info("Starting Notion automation script...")
    delete_old_logs(LOG_FILE)  # Delete old logs before running the script
    _remove_done_from_db()
    logging.info("Notion automation script completed.")