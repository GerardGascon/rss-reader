from abc import abstractmethod

import requests

from lists.models import Feed


class Notifier(object):
    def __init__(self, feed: Feed):
        self.feed = feed


    @abstractmethod
    def notify(self, rss_entry):
        pass


class DiscordNotifier(Notifier):
    def notify(self, rss_entry):
        message = ""
        message += f"**{rss_entry.title}**\n\n" if hasattr(rss_entry, "title") else ""
        message += f"{rss_entry.summary}\n\n" if hasattr(rss_entry, "summary") else ""

        message += f"🔗 {rss_entry.link}"
        self._send_message(message)


    def _send_message(self, content):
        webhook_url = self.feed.category.webhook_url

        message = "@everyone\n" if self.feed.notify else ""
        message += (
            f"# {self.feed.announcement_title}\n\n"
            f"{content}"
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