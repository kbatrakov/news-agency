from django.urls import path
import publisher
import publisher.views

urlpatterns = [
    path("", publisher.views.index, name="index"),
]

app_name = "publisher"
