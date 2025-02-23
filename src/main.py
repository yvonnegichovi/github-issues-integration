from flask import Flask, request, jsonify
import requests
import re
import os
from dotenv import load_dotenv
from src.config import config

# Load environment variables
load_dotenv()


app = Flask(__name__)

def parse_telex_message(message):
    """Extracts issue details from a structured Telex message."""
    match = re.match(r"@bot\s+(Report bug|Feature request|Task):\s+(.+)", message, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)  # (Issue Type, Title)
    return None, None

def send_telex_response(text):
    """Sends a response back to the Telex channel."""
    if config.TELEX_WEBHOOK:
        requests.post(config.TELEX_WEBHOOK, json={"text": text})

def create_github_issue(issue_type, title):
    """Creates a GitHub issue using the GitHub API."""
    url = f"https://api.github.com/repos/{config.GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {config.GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"title": f"[{issue_type}] {title}", "body": "Created via Telex integration."}

    print(f"Creating GitHub issue with title: {payload['title']}")  # Debugging log
    response = requests.post(url, json=payload, headers=headers)
    print(f"GitHub response: {response.status_code}, {response.text}")  # Debugging log

    return response.json() if response.status_code == 201 else None

@app.route("/webhook", methods=["POST"])
def telex_webhook():
    """Handles incoming Telex messages and creates GitHub issues."""
    data = request.json
    message = data.get("text", "")
    print(f"Received message: {message}")  # Debugging log
    issue_type, title = parse_telex_message(message)

    if issue_type and title:
        print(f"Parsed issue: {issue_type} - {title}")  # Debugging log
        issue = create_github_issue(issue_type, title)
        if issue:
            send_telex_response(f"✅ Issue created: {issue['html_url']}")
            return jsonify({"status": "success", "issue_url": issue['html_url']}), 201
        return jsonify({"status": "error", "message": "Failed to create issue"}), 500

    return jsonify({"status": "ignored", "message": "No valid issue format detected"}), 400

@app.route("/integration-settings", methods=["GET"])
def telex_integration_settings():
    """Provides the required integration settings JSON for Telex."""
    settings_response = {
        "settings": [
            {
                "label": "GitHub Repository",
                "type": "text",
                "required": True,
                "default": "user/repository"
            },
            {
                "label": "GitHub Token",
                "type": "text",
                "required": True,
                "default": "github_token"
            },
            {
                "label": "Notify on Issue Creation",
                "type": "checkbox",
                "default": True
            },
            {
                "label": "Allowed Issue Types",
                "type": "multi-select",
                "default": "Bug,Feature,Task",
                "options": ["Bug", "Feature", "Task"]
            }
        ]
    }
    return jsonify(settings_response), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
