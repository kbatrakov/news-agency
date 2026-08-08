from django.urls import path
from publisher.views import (
    EditorListView, EditorDetailView, NewspaperListView,
    NewspaperDetailView, TopicListView, NewspaperCreateView, NewspaperUpdateView,
    NewspaperDeleteView, TopicCreateView, TopicUpdateView, TopicDeleteView,
    EditorCreateView, EditorDeleteView, EditorYearsOfExperienceView,
    IndexView, SelfAssignToNewspaperView,
)


urlpatterns = [
    path("", IndexView.as_view(),
         name="index"),
    path("editors/", EditorListView.as_view(),
         name="editor-list"),
    path("editors/<int:pk>/", EditorDetailView.as_view(),
         name="editor-detail"),
    path("newspapers/", NewspaperListView.as_view(),
         name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(),
         name="newspaper-detail"),
    path("topics/", TopicListView.as_view(),
         name="topic-list"),
    path("newspapers/create/", NewspaperCreateView.as_view(),
         name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(),
         name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(),
         name="newspaper-delete"),
    path("topics/create/", TopicCreateView.as_view(),
         name="topic-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(),
         name="topic-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(),
         name="topic-delete"),
    path("editors/create/", EditorCreateView.as_view(),
         name="editor-create"),
    path("editors/<int:pk>/delete/", EditorDeleteView.as_view(),
         name="editor-delete"),
    path("editors/<int:pk>/update/", EditorYearsOfExperienceView.as_view(),
         name="editor-update"),
    path("newspapers/<int:pk>/assign/", SelfAssignToNewspaperView.as_view(),
         name="newspaper-assign"),
]

app_name = "publisher"
