from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    model = Feed

    list_display = ('name', 'url', 'notify', 'fetch_interval', 'last_fetched')
    fieldsets = (
        (None, {'fields': ('name', 'url',)}),
        ('Details', {'fields': ('notify', 'fetch_interval', 'last_fetched')}),
    )
