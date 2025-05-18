from django.db import models
from django.utils import timezone


class Feed(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    fetch_interval = models.IntegerField(default=60)
    notify = models.BooleanField(default=False)
    last_fetched = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url
