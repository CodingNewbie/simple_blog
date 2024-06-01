from django.views.generic import TemplateView
from posts.models import Post, Status


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["post_list"] = Post.objects.filter(status=published_status).order_by("-created_on")
        return context

class AboutPageView(TemplateView):
    template_name = "pages/about.html"
