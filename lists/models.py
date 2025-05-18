from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    webhook_url = models.URLField()

    def __str__(self):
        return self.name


class Feed(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    announcement_title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    fetch_interval = models.IntegerField(default=60)
    notify = models.BooleanField(default=False)
    last_fetched = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url