import requests
import os
import re
from config import config
from dotenv import load_dotenv
import os

load_dotenv()

print("Lets print for telex again")
print(os.getenv("TELEX_WEBHOOK"))

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

