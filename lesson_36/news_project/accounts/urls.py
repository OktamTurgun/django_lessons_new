from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import dashboard_view, user_login, signup_view
from .forms import CustomPasswordChangeForm
from django.views.generic import TemplateView

app_name = "accounts"

urlpatterns = [
    path('login/', user_login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="accounts:logged_out"),
        name="logout",
    ),
    path(
        "logged-out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),
    path('signup/', signup_view, name='register'),
    path(
        'password_change/', 
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url='/accounts/password_change/done/',
            form_class=CustomPasswordChangeForm
        ), 
        name='password_change'
    ),
    
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
    
    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'
    ),
    
    path(
        'password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    
    path(
        'password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    
    path('profile/', dashboard_view, name='user_profile'),
]
