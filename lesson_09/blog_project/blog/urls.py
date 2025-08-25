from .views import BlogDetailView, BlogListView
from django.urls import path

urlpatterns = [
  path("", BlogListView.as_view(), name="home"),
  path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
]