import os
from notion_client import Client

# Read secrets from environment variables
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

if not SECRET_TOKEN or not DATABASE_ID:
    raise ValueError("SECRET_TOKEN or DATABASE_ID environment variables are not set.")

notion = Client(auth=SECRET_TOKEN)

# This will list pages your integration has access to
response = notion.search(filter={"property": "object", "value": "database"})
for r in response["results"]:
    print(r["id"], r["title"])

# Fetch database info
db_info = notion.databases.retrieve(database_id=DATABASE_ID)

# Print all column names and types
print("Columns in the database:")
for name, prop in db_info["properties"].items():
    print(f"- {name}: {prop['type']}")

def _remove_done_from_db():
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

    # Delete each page
    for page in results:
        notion.pages.update(page["id"], archived=True)

if __name__ == "__main__":
    _remove_done_from_db()