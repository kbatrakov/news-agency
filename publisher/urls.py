from django.urls import path
from publisher.views import (
    index, EditorListView, EditorDetailView, NewspaperListView,
    NewspaperDetailView, TopicListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("editors/", EditorListView.as_view(),
         name="editor-list"),
    path("editors/<int:pk>/", EditorDetailView.as_view(),
         name="editor-detail"),
    path("newspapers/", NewspaperListView.as_view(),
         name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(),
         name="newspaper-detail"),
    path("topics/", TopicListView.as_view(),
         name="topic-list")

]

app_name = "publisher"
