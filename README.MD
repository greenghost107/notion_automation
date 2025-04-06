## Logging

The `notion_automation` script generates logs to track its execution and any issues encountered. The logs are saved to a file named `notion_automation.log`.

### Accessing Logs in GitHub Actions

Since this script runs as part of a scheduled GitHub Actions workflow, the logs are uploaded as an artifact after each run. You can download and inspect the logs by following these steps:

1. Go to the **Actions** tab in the repository.
2. Select the most recent workflow run (or the specific run you want to inspect).
3. Scroll down to the **Artifacts** section.
4. Download the artifact named `notion-automation-log`.
5. Open the `notion_automation.log` file to view the logs.

### Example Log Output

Here is an example of what the log file might look like:
2025-04-06 23:59:00 - INFO - Starting Notion automation script... 2025-04-06 23:59:01 - INFO - Successfully retrieved environment variables. 2025-04-06 23:59:02 - INFO - Fetching accessible databases... 2025-04-06 23:59:03 - INFO - Database ID: 1c3ff09e431480c8b527c81515151515, Title: Example Database 2025-04-06 23:59:04 - INFO - Retrieving database info for DATABASE_ID: 1c3ff09e431480c8b527c81515151515 2025-04-06 23:59:05 - INFO - Columns in the database: 2025-04-06 23:59:05 - INFO - - Name: Title 2025-04-06 23:59:05 - INFO - - Done: checkbox 2025-04-06 23:59:06 - INFO - Querying items marked as 'Done'... 2025-04-06 23:59:07 - INFO - Found 3 items marked as 'Done'. Archiving them... 2025-04-06 23:59:08 - INFO - Archived page with ID: abc123 2025-04-06 23:59:09 - INFO - Archived page with ID: def456 2025-04-06 23:59:10 - INFO - Archived page with ID: ghi789 2025-04-06 23:59:11 - INFO - Notion automation script completed.


### Log Retention

The script automatically deletes logs older than 6 months to prevent excessive file size. This behavior is handled by the `delete_old_logs` function in the script.