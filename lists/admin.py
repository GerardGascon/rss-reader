from django.contrib import admin

from .models import Feed, Category


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    model = Feed

    list_display = ('name', 'url', 'notify', 'fetch_interval', 'last_fetched')
    fieldsets = (
        (None, {'fields': ('name', 'url', 'category')}),
        ("Discord", {'fields': ('announcement_title',)}),
        ('Details', {'fields': ('notify', 'fetch_interval', 'last_fetched')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ('name', 'webhook_url')
    fieldsets = (
        (None, {'fields': ('name', 'webhook_url',)}),
    )
