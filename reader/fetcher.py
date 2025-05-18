import time
from datetime import timedelta
from io import BytesIO

import feedparser
import requests
from django.utils import timezone

from lists.models import Feed
from notifier import telegram


def fetch_rss_feed(response):
    content = BytesIO(response.content)
    feed = feedparser.parse(content)
    return feed.entries


def fetch_feed(feed):
    try:
        print(f"[{timezone.now()}] Fetching: {feed.name} ({feed.url})")
        response = requests.get(feed.url, timeout=10)
        response.raise_for_status()
        feed.last_fetched = timezone.now()
        feed.save()
        content = fetch_rss_feed(response)
        telegram.send_message(f"[✓] Fetched {feed.name}")
        print(f"[✓] Fetched {feed.name}: {content}")
    except Exception as e:
        print(f"[!] Error fetching {feed.name}: {e}")


def scheduler_loop():
    while True:
        now = timezone.now()
        feeds = Feed.objects.all()
        for feed in feeds:
            due = feed.last_fetched + timedelta(seconds=feed.fetch_interval)
            if now >= due:
                fetch_feed(feed)
        time.sleep(1)
