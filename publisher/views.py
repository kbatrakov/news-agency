from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from publisher.models import Editor, Topic, Newspaper
from django.views import generic


def index(request: HttpRequest) -> HttpResponse:
    num_editors = Editor.objects.count()
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()

    context = {
        "num_editors": num_editors,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers
    }

    return render(request, template_name="publisher/index.html", context=context)


class EditorListView(generic.ListView):
    model = Editor
    paginate_by = 7


class EditorDetailView(generic.DetailView):
    model = Editor
    queryset = Editor.objects.prefetch_related("newspapers__topic")


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 7


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class TopicListView(generic.ListView):
    model = Topic
    queryset = Topic.objects.all()
    paginate_by = 7
