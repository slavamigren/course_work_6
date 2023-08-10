from django.urls import path
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
from blog.apps import BlogConfig
app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('view/<int:pk>', BlogDetailView.as_view(), name='view_post'),
    path('create', BlogCreateView.as_view(), name='create_post'),
    path('update/<int:pk>', BlogUpdateView.as_view(), name='update_post'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete_post'),

]