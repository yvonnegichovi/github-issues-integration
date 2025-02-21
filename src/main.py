from flask import Flask, request, jsonify
from telex import parse_telex_message, send_telex_response
from github import create_github_issue
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def telex_webhook():
    """Handles incoming Telex messages and creates GitHub issues."""
    data = request.json
    message = data.get("text", "")
    print(f"Received message: {message}") # Debugging log
    issue_type, title = parse_telex_message(message)

    if issue_type and title:
        print(f"Parsed issue: {issue_type} - {title}") # Debugging log
        issue = create_github_issue(issue_type, title)
        if issue:
            send_telex_response(f"✅ Issue created: {issue['html_url']}")
            return jsonify({"status": "success", "issue_url": issue['html_url']}), 201
        return jsonify({"status": "error", "message": "Failed to create issue"}), 500

    return jsonify({"status": "ignored", "message": "No valid issue format detected"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
