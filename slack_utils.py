import requests
import time

def search_slack_thread(slack_token, channel, thread_key, retries=3):
    query = f'in:{channel} "{thread_key}"'

    for attempt in range(retries):
        response = requests.post(
            "https://slack.com/api/search.messages",
            headers={"Authorization": f"Bearer {slack_token}"},
            data={
                "query": query,
                "sort": "timestamp",
                "sort_dir": "asc",
                "count": "5"
            }
        )

        if response.status_code != 200:
            raise Exception(f"Slack API error: {response.text}")

        data = response.json()
        matches = data.get("messages", {}).get("matches", [])

        for msg in matches:
            if thread_key in msg.get("text", ""):
                return msg["ts"]

        time.sleep(1)

    return None
