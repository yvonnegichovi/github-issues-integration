from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

# Load environment variables
TELEX_WEBHOOK = os.getenv("TELEX_WEBHOOK")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: "username/repository"


def parse_telex_message(message):
    """Extracts issue details from a structured Telex message."""
    match = re.match(r"@bot\s+(Report bug|Feature request|Task):\s+(.+)", message, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)  # (Issue Type, Title)
    return None, None


def create_github_issue(issue_type, title):
    """Creates a GitHub issue using the GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"title": f"[{issue_type}] {title}", "body": "Created via Telex integration."}

    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 201 else None


def send_telex_response(text):
    """Sends a response back to the Telex channel."""
    if TELEX_WEBHOOK:
        requests.post(TELEX_WEBHOOK, json={"text": text})


@app.route("/webhook", methods=["POST"])
def telex_webhook():
    """Handles incoming Telex messages and creates GitHub issues."""
    data = request.json
    message = data.get("text", "")
    issue_type, title = parse_telex_message(message)

    if issue_type and title:
        issue = create_github_issue(issue_type, title)
        if issue:
            send_telex_response(f"✅ Issue created: {issue['html_url']}")
            return jsonify({"status": "success", "issue_url": issue['html_url']}), 201
        return jsonify({"status": "error", "message": "Failed to create issue"}), 500

    return jsonify({"status": "ignored", "message": "No valid issue format detected"}), 400


if __name__ == "__main__":
    app.run(port=5000)

