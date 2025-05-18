import time
from datetime import timedelta
from dateutil import parser
from io import BytesIO

import feedparser
import requests
from django.utils import timezone

from lists.models import Feed
from notifier import discord


def fetch_rss_feed(response) -> feedparser.FeedParserDict:
    content = BytesIO(response.content)
    return feedparser.parse(content)


def send_entries(feed: Feed, content: feedparser.FeedParserDict):
    for entry in reversed(content.entries):
        if hasattr(entry, "published"):
            entry_date = parser.parse(entry.published)
        elif hasattr(entry, "updated"):
            entry_date = parser.parse(entry.updated)
        else:
            continue # Skip entries without a date

        if entry_date <= feed.last_fetched:
            continue

        title = f"**{entry.title}**" if hasattr(entry, "title") else "(No title provided)"
        summary = entry.summary if hasattr(entry, "summary") else "(No summary provided)"

        message = f"{title}\n\n{summary}\n\n🔗 {entry.link}"
        discord.send_message(feed, message)
    pass


def fetch_feed(feed: Feed):
    try:
        print(f"[{timezone.now()}] Fetching: {feed.name} ({feed.url})")
        response = requests.get(feed.url, timeout=10)
        response.raise_for_status()
        content = fetch_rss_feed(response)
        send_entries(feed, content)
        feed.last_fetched = timezone.now()
        feed.save()
        print(f"[✓] Fetched {feed.name}")
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
