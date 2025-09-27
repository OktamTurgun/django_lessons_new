# Lesson 39: Login_required dekoratori va LoginRequiredMixin

## Dars maqsadi
Bu darsda biz Django'da foydalanuvchi autentifikatsiyasini tekshirish uchun ishlatladigan `@login_required` dekoratori va `LoginRequiredMixin` class-i bilan ishlashni o'rganamiz. Bu vositalar orqali faqat tizimga kirgan foydalanuvchilar ma'lum sahifalarga kirishiga ruxsat beramiz.

## Nazariy qism

### Login_required dekoratori nima?

`@login_required` - bu Django'ning o'rnatilgan dekoratori bo'lib, u funksiyaga asoslangan view'larni himoya qilish uchun ishlatiladi. Bu dekorator tekshiradi:

1. Foydalanuvchi tizimga kirganmi?
2. Agar kirmagan bo'lsa, uni login sahifasiga yo'naltiradi
3. Agar kirgan bo'lsa, view'ni normal ishlashiga ruxsat beradi

### LoginRequiredMixin nima?

`LoginRequiredMixin` - bu class-based view'lar uchun mo'ljallangan mixin class. U xuddi `@login_required` dekorator kabi ishlaydi, lekin class-based view'lar bilan ishlatiladi.

## Praktik misol: Function-based view bilan

### 1. Kerakli import'larni qo'shish

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
```

### 2. Login_required dekoratori bilan himoyalangan view

```python
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    """Foydalanuvchi profili sahifasi - faqat login qilganlar kirishi mumkin"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })

@login_required
def edit_profile_view(request):
    """Profilni tahrirlash sahifasi"""
    if request.method == 'POST':
        # Profil ma'lumotlarini yangilash logikasi
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html', {
        'user': request.user
    })
```

### 3. Settings.py da LOGIN_URL ni sozlash

```python
# settings.py
LOGIN_URL = '/accounts/login/'  # Login sahifasining manzili
LOGIN_REDIRECT_URL = '/'        # Login dan keyin yo'naltiriladigan sahifa
```

## Class-based view'lar bilan ishlash

### 1. LoginRequiredMixin import qilish

```python
# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.models import User
```

### 2. LoginRequiredMixin bilan himoyalangan class-based view

```python
# views.py
class ProfileView(LoginRequiredMixin, TemplateView):
    """Foydalanuvchi profili sahifasi - faqat login qilganlar"""
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    """Profilni tahrirlash sahifasi"""
    model = User
    template_name = 'accounts/edit_profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/accounts/profile/'
    
    def get_object(self):
        return self.request.user
```

### 3. Custom login_url belgilash

```python
# views.py
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = '/custom-login/'  # Maxsus login sahifasi
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
```

## URL konfiguratsiyasi

### 1. accounts/urls.py

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    
    # Function-based view'lar uchun
    # path('profile/', views.profile_view, name='profile'),
    # path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
```

### 2. Asosiy urls.py

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('news.urls')),  # Bosh sahifa
]
```

## Template'lar yaratish

### 1. Profile template

```html
<!-- templates/accounts/profile.html -->
{% extends 'base.html' %}

{% block title %}Profil - {{ user.username }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4>Foydalanuvchi profili</h4>
                </div>
                <div class="card-body">
                    <p><strong>Username:</strong> {{ user.username }}</p>
                    <p><strong>Ism:</strong> {{ user.first_name|default:"Kiritilmagan" }}</p>
                    <p><strong>Familiya:</strong> {{ user.last_name|default:"Kiritilmagan" }}</p>
                    <p><strong>Email:</strong> {{ user.email|default:"Kiritilmagan" }}</p>
                    <p><strong>Ro'yxatga olindi:</strong> {{ user.date_joined|date:"d.m.Y H:i" }}</p>
                    
                    <div class="mt-3">
                        <a href="{% url 'accounts:edit_profile' %}" class="btn btn-primary">
                            Profilni tahrirlash
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 2. Edit profile template

```html
<!-- templates/accounts/edit_profile.html -->
{% extends 'base.html' %}

{% block title %}Profilni tahrirlash{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h4>Profilni tahrirlash</h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="first_name" class="form-label">Ism</label>
                            <input type="text" class="form-control" id="first_name" 
                                   name="first_name" value="{{ user.first_name }}">
                        </div>
                        
                        <div class="mb-3">
                            <label for="last_name" class="form-label">Familiya</label>
                            <input type="text" class="form-control" id="last_name" 
                                   name="last_name" value="{{ user.last_name }}">
                        </div>
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" 
                                   name="email" value="{{ user.email }}">
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-success">Saqlash</button>
                            <a href="{% url 'accounts:profile' %}" class="btn btn-secondary">
                                Bekor qilish
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Xatoliklarni boshqarish

### 1. Permission Denied exception

```python
# views.py
from django.core.exceptions import PermissionDenied

class CustomProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Bu sahifaga kirish uchun tizimga kirishingiz kerak")
        return super().dispatch(request, *args, **kwargs)
```

### 2. Custom redirect message

```python
# views.py
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

@login_required
def custom_protected_view(request):
    messages.info(request, 'Xush kelibsiz! Siz muvaffaqiyatli tizimga kirdingiz.')
    return render(request, 'protected_page.html')
```

## Navigation bar'da autentifikatsiya holati

```html
<!-- templates/base.html -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
        
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" 
                       data-bs-toggle="dropdown">
                        {{ user.username }}
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">
                            Profil
                        </a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">
                            Chiqish
                        </a></li>
                    </ul>
                </li>
            {% else %}
                <a class="nav-link" href="{% url 'accounts:login' %}">Kirish</a>
                <a class="nav-link" href="{% url 'accounts:signup' %}">Ro'yxatga olish</a>
            {% endif %}
        </div>
    </div>
</nav>
```

## Xavfsizlik va Best Practice'lar

### 1. CSRF himoyasi
- Har doim `{% csrf_token %}` dan foydalaning
- POST so'rovlarda CSRF token majburiy

### 2. User ma'lumotlarini tekshirish
```python
@login_required
def secure_view(request):
    if not request.user.is_active:
        messages.error(request, 'Hisobingiz faol emas')
        return redirect('accounts:login')
    
    return render(request, 'secure_page.html')
```

### 3. Permission-based himoya
```python
from django.contrib.auth.decorators import user_passes_test

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
@login_required
def admin_only_view(request):
    return render(request, 'admin_page.html')
```

## Xulosa

`@login_required` dekoratori va `LoginRequiredMixin` Django'da autentifikatsiyani boshqarishning asosiy vositalari hisoblanadi. Ular orqali:

- Foydalanuvchi tizimga kirganligini tekshiramiz
- Himoyalangan sahifalarga kirishni cheklaymiz
- Xavfsiz va foydalanuvchi-do'st interfeys yaratamiz
- Autentifikatsiya oqimini boshqaramiz

**Keyingi darsda:**
40 - darsda profilda rasm va boshqa ma'lumotlarni qo'shishni o'rganamiz.