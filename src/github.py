import requests
from config import config  # Import configuration

def create_github_issue(issue_type, title):
    """Creates a GitHub issue using the GitHub API."""
    url = f"https://api.github.com/repos/{config.GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {config.GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"title": f"[{issue_type}] {title}", "body": "Created via Telex integration."}

    print(f"Creating GitHub issue with title: {payload['title']}")  # Debugging log

    response = requests.post(url, json=payload, headers=headers)
    print(f"GitHub response: {response.status_code}, {response.text}")  # Debugging log

    return response.json() if response.status_code == 201 else None

