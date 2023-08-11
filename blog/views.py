from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import BlogForm
from blog.models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserRequiredMixin:  # миксин блокирует доступ пользователя к чужим объектам
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    paginate_by = 3


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object.owner != self.request.user:
            context_data['owner'] = False
        else:
            context_data['owner'] = True
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

class BlogDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class BlogUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('blog:view_post', args=[self.kwargs.get('pk')])