# Security and Billing Stack: Jira Backlog Ticket Creator
This is intended to populate the Jira backlog with the Security and Billing stack requirements for use in multiple projects.

## Overview
```
JiraTicketCreator/
│
├── templates/
│   ├── Epic1/
│   │   ├── description.txt
│   │   ├── CSVFile1.csv
│   │   └── CSVFile2.csv
│   ├── Epic2/
│   │   ├── description.txt
│   │   ├── SubEpic1/
│   │   │   ├── description.txt
│   │   │   └── CSVFile3.csv
│   │   ├── CSVFile4.csv
│   │   └── CSVFile5.csv
│   ├── Epic3/
│   │   ├── CSVFile6.csv
│   │   └── CSVFile7.csv
│   └── ...
│
├── JiraTicketCreator.csproj
└── Program.cs
```
- The `templates/` folder contains various subfolders, each representing an Epic.
- Each Epic folder contains:
  - A `description.txt` file: This file contains the description of the Epic.
  - CSV files (e.g., `csv-file-1.csv`, `csv-file-2.csv`): These files contain the data for creating individual tickets.
  - Optionally, subfolders representing nested Epics.
- The `csv-file-x.csv` files contain the data for creating individual tickets. Each row in the CSV file represents a ticket, with columns specifying the ticket's summary, description, and other relevant fields.
- The `description.txt` files contain the description of the corresponding Epic. This description will be read dynamically and assigned to the Epic when creating it in Jira.

This hierarchical structure allows for organizing Epics and their associated tickets in a folder-based manner, making it easy to manage and maintain the templates for creating Jira tickets.

## Getting Started

### Install packages
  ```
  dotnet add package Newtonsoft.Json
  dotnet add package CsvHelper
  ```
- Adding Epics / Issues to Backlog:
  - `templates/`: This directory contains your Jira ticket templates organized by Epic. Nested folders under `templates/` are treated as Epics.
  - `templates/name-of-issue-template.csv`: This will be the created issue under the epic (if nested under another folder)

### Compilation:
1. Open a terminal
2. Navigate to `JiraTicketCreator/`
3. Run the following command to compile
   ```
   dotnet build
   ```

### Execution:
After successful compilation, you can run the compiled executable from the terminal.
Be sure the environment variables are set prior to running:

| Name              | Description                                                                                      | Required  |
|:------------------|:-------------------------------------------------------------------------------------------------|:----------|
| JIRA_API_TOKEN    | Used for authenticating to Jira                                                                  | Yes       |
| JIRA_USERNAME     | Used for logging in to Jira                                                                      | Yes       |
| JIRA_SERVER       | Server URL for the Jira instance                                                                 | Yes       |
| JIRA_PROJECT_KEY  | Project key where the newly created tickets will reside                                          | Yes       |
| TEMPLATES_PATH    | Path to the templates directory where the ticket templates reside. Default value is `templates/` | No        |

1. Navigate to the `bin/Release/net8.0/` directory:
   ```
   cd bin/Release/net8.0/
   ```
2. Run the compiled executable:
   ```
   dotnet JiraTicketCreator
   ```
