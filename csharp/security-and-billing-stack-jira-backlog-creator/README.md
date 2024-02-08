# Security and Billing Stack: Jira Backlog Ticket Creator
This is intended to populate the Jira backlog with the Security and Billing stack requirements for use in multiple projects. 

## Getting Started 
Set the following environment variables: 

| Name              | Description                                                                                       | Required  |
|:------------------|:--------------------------------------------------------------------------------------------------|:----------|
| JIRA_API_TOKEN    | Used for authenticating to Jira                                                                   | Yes       |
| JIRA_USERNAME     | Used for loging in to Jira                                                                        | Yes       |
| JIRA_SERVER       | Server URL for the Jira instance                                                                  | Yes       |
| JIRA_PROJECT_KEY  | Project key where the newly created tickets will reside                                           | Yes       | 
| TEMPLATES_PATH    | Path to the templates directory where the ticket templates reside. Default value is `templates/`  | No        | 


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
1. Navigate to the `bin/Release/net8.0/` directory:
   ```
   cd bin/Release/net8.0/
   ```
2. Run the compiled executable:
   ```
   dotnet JiraTicketCreator
   ```
