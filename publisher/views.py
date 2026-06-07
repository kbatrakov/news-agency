from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from publisher.models import Editor, Topic, Newspaper


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
