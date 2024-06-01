'''from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Status

class ArchivedPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived_status = Status.objects.get(name="archived")
        context["post_list"] = (
            Post.objects.filter(status=archived_status)
            .order_by("created_on")
            .reverse()
        )
        return context

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["post_list"] = (
            Post.objects.filter(status=published_status)
            .order_by("created_on")
            .reverse()
        )
        return context

class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = (
            Post.objects.filter(status=draft_status)
            .filter(author=self.request.user)
            .order_by("created_on")
            .reverse()
        )
        return context


class PostDetailView(UserPassesTestMixin, DetailView):
    template_name = "posts/detail.html"
    model = Post

    def test_func(self):
        post = self.get_object()
        if post.status.name == "published":
            return True
        else:
            if post.status_name == "draft":
                return post.author == self.request.user
            elif post.status.name == "archived":
                if self.request.user:
                    return True
        return False




class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "status", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status", "image"]

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
'''

# posts/views.py
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Status

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ["title", "subtitle", "body", "status", "image"]

class ArchivedPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived_status = Status.objects.get(name="archived")
        context["post_list"] = (
            Post.objects.filter(status=archived_status)
            .order_by("created_on")
            .reverse()
        )
        return context

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["post_list"] = (
            Post.objects.filter(status=published_status)
            .order_by("created_on")
            .reverse()
        )
        return context

class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = (
            Post.objects.filter(status=draft_status)
            .filter(author=self.request.user)
            .order_by("created_on")
            .reverse()
        )
        return context

class PostDetailView(UserPassesTestMixin, DetailView):
    template_name = "posts/detail.html"
    model = Post

    def test_func(self):
        post = self.get_object()
        if post.status.name == "published":
            return True
        else:
            if post.status_name == "draft":
                return post.author == self.request.user
            elif post.status.name == "archived":
                if self.request.user:
                    return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    form_class = PostForm  # Use the custom form with CKEditor

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    form_class = PostForm  # Use the custom form with CKEditor

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

