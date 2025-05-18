import requests

from lists.models import Feed


def send_message(feed: Feed, content):
    webhook_url = feed.category.webhook_url

    message = "@everyone\n\n" if feed.notify else ""
    message += (
        f"# {feed.announcement_title}\n"
        f"{feed.url}\n\n"
        f"{content}\n\n"
    )

    payload = {
        "content": message,
        "allowed_mentions": {
            "parse": ["users", "everyone"]
        }
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Successfully sent message")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
