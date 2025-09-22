from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import dashboard_view, user_login
from .forms import CustomPasswordChangeForm
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', user_login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
     path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="logged_out"),
        name="logout",
    ),
    path(
        "logged-out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),
    path('password_change/', 
         PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/accounts/password_change/done/',
             form_class=CustomPasswordChangeForm
         ), 
         name='password_change'),
    
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),
    path('profile/', dashboard_view, name='user_profile'),
]