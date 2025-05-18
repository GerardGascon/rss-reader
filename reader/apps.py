import os
import threading

from django.apps import AppConfig


class ReaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reader'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from reader.fetcher import scheduler_loop
        thread = threading.Thread(target=scheduler_loop, name="FeedFetcher")
        thread.daemon = True
        thread.start()
        print("📡 Feed fetcher started in background.")
