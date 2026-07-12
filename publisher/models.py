from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=160, null=False, blank=False)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return f"Topic of the publication: {self.name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=160, null=False, blank=False)
    content = models.TextField(max_length=2500, null=False, blank=False)
    published_date = models.DateField(null=False, blank=False)
    topic = models.ForeignKey(Topic, related_name="newspapers", on_delete=models.CASCADE)
    publishers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers",
                                        blank=False)

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return (f"Title: {self.title}"
                f"Topic: {self.topic}"
                f"Published by: {self.publishers}")


class Editor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"Editor: {self.first_name} {self.last_name} ({self.username})"

    def get_absolute_url(self):
        return reverse("publisher:editor-detail", kwargs={"pk": self.pk})