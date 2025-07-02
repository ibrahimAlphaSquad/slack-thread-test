import os
import json
import requests
from slack_utils import search_slack_thread
from dotenv import load_dotenv

load_dotenv()

with open("sample_event.json", "r") as f:
    event = json.load(f)

slack_token = os.getenv("SLACK_USER_OAUTH_TOKEN")
webhook_url = os.getenv("SLACK_INCOMING_WEBHOOK_URL")
channel = os.getenv("SLACK_CHANNEL")

thread_key = event["thread_key"]
thread_ts = search_slack_thread(slack_token, channel, thread_key)

payload = {
    "channel": channel,
    "attachments": [
        {
            "color": "#28a745",
            "pretext": f"*{os.getenv('GITHUB_REPOSITORY')}*",
            "title": f"{event['title']} #{event['number']}",
            "title_link": event["title_link"],
            "text": event["message"],
            "footer": f"GitHub Actions • Thread-Key: {thread_key}",
            "footer_icon": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "mrkdwn_in": ["text", "pretext", "footer"]
        }
    ]
}

if thread_ts:
    print(f"[✅] Found thread_ts: {thread_ts}")
    payload["thread_ts"] = thread_ts
else:
    print("[⚠️ ] No thread found. Sending as top-level message.")

response = requests.post(webhook_url, json=payload)

if response.status_code != 200:
    print("Slack response:", response.text)
    raise Exception("Failed to send Slack message")

print("[🎉] Slack message sent!")
