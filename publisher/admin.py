from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from publisher.models import Topic, Newspaper, Editor


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display =[
        "name",
    ]

    list_filter = [
        "name",
    ]

    search_fields = [
        "name",
    ]


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "content",
        "published_date",
        "topic",
    ]

    list_filter = [
        "title",
        "published_date",
        "topic",
    ]

    search_fields = [
        "title",
    ]


@admin.register(Editor)
class EditorAdmin(UserAdmin):
    list_display =UserAdmin.list_display +("years_of_experience", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
