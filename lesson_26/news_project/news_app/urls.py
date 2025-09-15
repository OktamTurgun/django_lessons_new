from django.urls import path
from .views import HomePageView, SinglePageView, NewsListView, AboutPageView, ContactPageView, custom_404_view, CategoryDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', SinglePageView.as_view(), name='news_detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('404/', custom_404_view, name='404'),
]
