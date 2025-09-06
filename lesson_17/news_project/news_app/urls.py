from django.urls import path
from .views import NewsListView, NewsDetailView, HomePageView, ContactPageView, custom_404_view

urlpatterns = [
  path('', HomePageView.as_view(), name='home'),
  path('news/', NewsListView.as_view(), name='news_list'),
  path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
  path('contact/', ContactPageView.as_view(), name='contact'),
  path('404/', custom_404_view, name='404'), 
]