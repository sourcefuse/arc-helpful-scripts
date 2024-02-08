from jira import JIRA
import os

# Jira server URL
JIRA_SERVER = 'https://your-jira-instance.com'

# Jira username and API token
JIRA_USERNAME = 'your_username'
JIRA_API_TOKEN = 'your_api_token'

# Connect to Jira
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

# Function to read template files
def read_template(template_name):
    template_path = os.path.join('templates', template_name)
    with open(template_path, 'r') as file:
        return file.read()

# Function to create a Jira ticket
def create_ticket(summary, description):
    issue_dict = {
        'project': {'key': 'YOUR_PROJECT_KEY'},  # Change this to your project key
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'}  # Change this to the appropriate issue type
    }
    issue = jira.create_issue(fields=issue_dict)
    print(f"Ticket created successfully: {issue.key}")

# Main function
def main():
    template_files = os.listdir('templates')
    for template_file in template_files:
        if template_file.endswith('.txt'):
            template_name = template_file.split('.')[0]
            summary, description = read_template(template_file).split('\n', 1)
            create_ticket(summary, description)

if __name__ == "__main__":
    main()
