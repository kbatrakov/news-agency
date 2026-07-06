from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from publisher.models import Editor, Topic, Newspaper
from django.views import generic


@login_required
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


class EditorListView(LoginRequiredMixin, generic.ListView):
    model = Editor
    paginate_by = 7


class EditorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Editor
    queryset = Editor.objects.prefetch_related("newspapers__topic")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 7


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    queryset = Topic.objects.all()
    paginate_by = 7


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("publisher:newspaper-list")
    template_name = "publisher/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("publisher:newspaper-list")
    template_name = "publisher/newspaper_form.html"


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("publisher:newspaper-list")
    template_name = "publisher/newspaper_confirm_delete.html"


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("publisher:topic-list")
    template_name = "publisher/topic_form.html"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("publisher:topic-list")
    template_name = "publisher/topic_form.html"


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("publisher:topic-list")
    template_name = "publisher/topic_confirm_delete.html"
