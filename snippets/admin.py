from django.contrib import admin
from .models import Snippet, Tag


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_tags", "created_by", "created_at", "updated_at")
    list_filter = ("created_by", "created_at", "updated_at", "tags")
    search_fields = ("title", "note")

    def get_tags(self, obj):
        return ", ".join(tag.title for tag in obj.tags.all())
    get_tags.short_description = "Tags"  # column name in admin list


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)
