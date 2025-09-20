from django.urls import path
from .views import(
  HomePageView, 
  SinglePageView, 
  NewsListView, 
  AboutPageView, 
  ContactPageView, 
  custom_404_view, 
  CategoryDetailView, 
  NewsCreateView, 
  NewsUpdateView, 
  NewsDeleteView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path("news/create/", NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path('news/<slug:slug>/', SinglePageView.as_view(), name='news_detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('404/', custom_404_view, name='404'),
]
