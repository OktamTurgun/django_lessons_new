from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard_view, user_login

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', dashboard_view, name='user_profile'),
]