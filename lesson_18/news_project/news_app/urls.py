from django.urls import path
from .views import NewsListView, NewsDetailView, HomePageView, ContactPageView, custom_404_view, AboutPageView
from django.views.generic import TemplateView

urlpatterns = [
  path('', HomePageView.as_view(), name='home'),
  path('news/', NewsListView.as_view(), name='news_list'),
  path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
  path('about/', TemplateView.as_view(template_name="news/about.html"), name='about'),
  path('contact/', ContactPageView.as_view(), name='contact'),
  path("404/", TemplateView.as_view(template_name="news/404.html"), name="404"),
]