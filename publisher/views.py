from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from publisher.forms import (EditorCreationForm, EditorYearsOfExperienceUpdateForm,
                             NewspaperForm, EditorUsernameSearchForm,
                             TopicNameSearchForm,
                             NewspaperTitleSearchForm)
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

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(EditorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["search_form"] = EditorUsernameSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset


class EditorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Editor
    queryset = Editor.objects.prefetch_related("newspapers__topic")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 7

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperTitleSearchForm(
            initial={
                "title": title
            }
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title")

        if title:
            return queryset.filter(title__icontains=title)

        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    queryset = Topic.objects.all()
    paginate_by = 7

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TopicNameSearchForm(
            initial={
                "name": name
            }
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("publisher:newspaper-list")
    template_name = "publisher/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
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


class EditorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Editor
    form_class = EditorCreationForm


class EditorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Editor
    success_url = reverse_lazy("publisher:editor-list")


class EditorYearsOfExperienceView(LoginRequiredMixin, generic.UpdateView):
    model = Editor
    form_class = EditorYearsOfExperienceUpdateForm
    template_name = "publisher/years_of_experience_form.html"

    def get_success_url(self):
        return reverse(
            "publisher:editor-detail",
            kwargs={"pk": self.object.pk}
        )


def self_assign_to_newspaper(request, pk):
    newspaper = get_object_or_404(Newspaper, pk=pk)

    if request.user not in newspaper.publishers.all():
        newspaper.publishers.add(request.user)

    return redirect("publisher:newspaper-list")
