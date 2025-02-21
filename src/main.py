import requests

GITHUB_API_URL = "https://api.github.com"

def fetch_issues(repo_owner, repo_name, token):
    url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/issues"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # List of issues
    else:
        return {"error": response.json()}

if __name__ == "__main__":
    # Example usage
    repo_owner = "telex_integrations"
    repo_name = "github-issues-integration"
    token = "your_github_personal_access_token"
    
    issues = fetch_issues(repo_owner, repo_name, token)
    print(issues)

