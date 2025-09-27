# Lesson 39 - Amaliyot: Login_required dekoratori va LoginRequiredMixin

## Amaliyot maqsadi
Ushbu amaliyotda biz news loyihamizdagi mavjud view'larni himoyalash va foydalanuvchi profili sahifalarini yaratish bilan shug'ullanamiz.

## Bosqich 1: Loyiha tuzilmasini tayyorlash

### 1.1 Accounts app'ini yaratish (agar hali yaratilmagan bo'lsa)

```bash
# Terminal'da
python manage.py startapp accounts
```

### 1.2 Settings.py'ga app qo'shish

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
    'accounts',  # Yangi qo'shildi
]

# Login/logout URL'larni sozlash
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

## Bosqich 2: Accounts app'ida view'larni yaratish

### 2.1 accounts/views.py faylini yaratish

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    """Maxsus Login View"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, f'Xush kelibsiz, {self.request.user.username}!')
        return reverse_lazy('news:home')

class CustomLogoutView(LogoutView):
    """Maxsus Logout View"""
    next_page = reverse_lazy('news:home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Siz tizimdan chiqdingiz.')
        return super().dispatch(request, *args, **kwargs)

# Function-based view misol
@login_required
def profile_view(request):
    """Foydalanuvchi profili sahifasi"""
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'title': 'Mening Profilim'
    })

@login_required
def edit_profile_view(request):
    """Profilni tahrirlash sahifasi"""
    if request.method == 'POST':
        user = request.user
        
        # Ma'lumotlarni yangilash
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        
        try:
            user.save()
            messages.success(request, 'Profil ma\'lumotlari muvaffaqiyatli yangilandi!')
            return redirect('accounts:profile')
        except Exception as e:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.')
    
    return render(request, 'accounts/edit_profile.html', {
        'user': request.user,
        'title': 'Profilni Tahrirlash'
    })

# Class-based view misol
class ProfileView(LoginRequiredMixin, TemplateView):
    """Class-based Profile View"""
    template_name = 'accounts/profile_class.html'
    login_url = '/accounts/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title'] = 'Mening Profilim (Class-based)'
        return context
```

### 2.2 accounts/urls.py yaratish

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URL'lar
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Profile URL'lar (Function-based)
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    
    # Profile URL'lar (Class-based) - test uchun
    path('profile-class/', views.ProfileView.as_view(), name='profile_class'),
]
```

## Bosqich 3: Template'lar yaratish

### 3.1 Registration template'larini yaratish

```bash
# Terminal'da template papkalarni yaratish
mkdir -p templates/registration
mkdir -p templates/accounts
```

### 3.2 Login template yaratish

```html
<!-- templates/registration/login.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Tizimga kirish{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">Tizimga kirish</h4>
                </div>
                <div class="card-body">
                    {% if form.errors %}
                        <div class="alert alert-danger">
                            {{ form.errors }}
                        </div>
                    {% endif %}
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">
                                Foydalanuvchi nomi
                            </label>
                            {{ form.username }}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password.id_for_label }}" class="form-label">
                                Parol
                            </label>
                            {{ form.password }}
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">Kirish</button>
                        </div>
                        
                        <div class="text-center mt-3">
                            <small>
                                Hisobingiz yo'qmi? 
                                <a href="{% url 'accounts:signup' %}">Ro'yxatga oling</a>
                            </small>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3.3 Profile template yaratish

```html
<!-- templates/accounts/profile.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">Foydalanuvchi profili</h4>
                    <small class="text-muted">Function-based View</small>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="text-center">
                                <div class="bg-secondary rounded-circle d-inline-flex align-items-center justify-content-center" 
                                     style="width: 100px; height: 100px;">
                                    <i class="fas fa-user fa-3x text-white"></i>
                                </div>
                                <h5 class="mt-2">{{ user.username }}</h5>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <table class="table table-borderless">
                                <tr>
                                    <td><strong>Username:</strong></td>
                                    <td>{{ user.username }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Ism:</strong></td>
                                    <td>{{ user.first_name|default:"Kiritilmagan" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Familiya:</strong></td>
                                    <td>{{ user.last_name|default:"Kiritilmagan" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Email:</strong></td>
                                    <td>{{ user.email|default:"Kiritilmagan" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Ro'yxatga olindi:</strong></td>
                                    <td>{{ user.date_joined|date:"d.m.Y H:i" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Oxirgi kirish:</strong></td>
                                    <td>{{ user.last_login|date:"d.m.Y H:i"|default:"Hech qachon" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Status:</strong></td>
                                    <td>
                                        {% if user.is_active %}
                                            <span class="badge bg-success">Faol</span>
                                        {% else %}
                                            <span class="badge bg-danger">Faol emas</span>
                                        {% endif %}
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'accounts:edit_profile' %}" class="btn btn-primary">
                            <i class="fas fa-edit"></i> Profilni tahrirlash
                        </a>
                        <a href="{% url 'accounts:profile_class' %}" class="btn btn-outline-info">
                            Class-based View ni ko'rish
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">Qo'shimcha ma'lumotlar</h6>
                </div>
                <div class="card-body">
                    <p><small class="text-muted">
                        Bu sahifa @login_required dekorator bilan himoyalangan.
                        Faqat tizimga kirgan foydalanuvchilar ko'rishi mumkin.
                    </small></p>
                    
                    <hr>
                    
                    <h6>Tezkor havolalar:</h6>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'news:home' %}" class="text-decoration-none">
                            <i class="fas fa-home"></i> Bosh sahifa
                        </a></li>
                        <li><a href="{% url 'news:create' %}" class="text-decoration-none">
                            <i class="fas fa-plus"></i> Yangilik qo'shish
                        </a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3.4 Edit profile template yaratish

```html
<!-- templates/accounts/edit_profile.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Profilni tahrirlash</h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="first_name" class="form-label">Ism</label>
                                    <input type="text" 
                                           class="form-control" 
                                           id="first_name" 
                                           name="first_name" 
                                           value="{{ user.first_name }}"
                                           placeholder="Ismingizni kiriting">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="last_name" class="form-label">Familiya</label>
                                    <input type="text" 
                                           class="form-control" 
                                           id="last_name" 
                                           name="last_name" 
                                           value="{{ user.last_name }}"
                                           placeholder="Familiyangizni kiriting">
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">Email manzil</label>
                            <input type="email" 
                                   class="form-control" 
                                   id="email" 
                                   name="email" 
                                   value="{{ user.email }}"
                                   placeholder="email@example.com">
                        </div>
                        
                        <div class="mb-3">
                            <small class="form-text text-muted">
                                <strong>Eslatma:</strong> Username va parolni o'zgartirish uchun 
                                alohida sahifalar mavjud.
                            </small>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-save"></i> Saqlash
                            </button>
                            <a href="{% url 'accounts:profile' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Bekor qilish
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

## Bosqich 4: News app'idagi view'larni himoyalash

### 4.1 news/views.py ni yangilash

```python
# news/views.py (mavjud view'larga qo'shimcha)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Mavjud CreateView'ni yangilash
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/create_news.html'
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    login_url = '/accounts/login/'  # Login sahifasi
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Yangilik muvaffaqiyatli yaratildi!')
        return super().form_valid(form)

# Mavjud UpdateView'ni yangilash
class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'news/update_news.html' 
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    login_url = '/accounts/login/'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_staff:
            messages.error(request, 'Faqat o\'z yangiligingizni tahrirlashingiz mumkin!')
            return redirect('news:detail', slug=obj.slug)
        return super().dispatch(request, *args, **kwargs)

# Function-based view misol
@login_required
def my_news_list(request):
    """Foydalanuvchining o'z yangiliklarini ko'rsatish"""
    user_news = News.published.filter(author=request.user).order_by('-created_time')
    
    context = {
        'news_list': user_news,
        'title': 'Mening yangilikfarim',
    }
    return render(request, 'news/my_news_list.html', context)
```

## Bosqich 5: URL konfiguratsiyasini yangilash

### 5.1 Asosiy urls.py ni yangilash

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Accounts URL'lari
    path('', include('news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 5.2 news/urls.py ni yangilash

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='home'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    
    # Himoyalangan URL'lar
    path('create/', views.NewsCreateView.as_view(), name='create'),
    path('news/<slug:slug>/edit/', views.NewsUpdateView.as_view(), name='update'),
    path('my-news/', views.my_news_list, name='my_news'),
    
    # Kategoriya bo'yicha
    path('category/<slug:slug>/', views.NewsByCategoryView.as_view(), name='category'),
]
```

## Bosqich 6: Navigation bar'ni yangilash

### 6.1 Base template'ni yangilash

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:home' %}">
                <i class="fas fa-newspaper"></i> Yangiliklar
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                    data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:home' %}">Bosh sahifa</a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:create' %}">
                                <i class="fas fa-plus"></i> Yangilik qo'shish
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:my_news' %}">
                                <i class="fas fa-list"></i> Mening yangilikfarim
                            </a>
                        </li>
                    {% endif %}
                </ul>
                
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" 
                               data-bs-toggle="dropdown">
                                <i class="fas fa-user"></i> {{ user.username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li>
                                    <a class="dropdown-item" href="{% url 'accounts:profile' %}">
                                        <i class="fas fa-user-circle"></i> Profil
                                    </a>
                                </li>
                                <li>
                                    <a class="dropdown-item" href="{% url 'accounts:edit_profile' %}">
                                        <i class="fas fa-edit"></i> Profilni tahrirlash
                                    </a>
                                </li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <a class="dropdown-item" href="{% url 'accounts:logout' %}">
                                        <i class="fas fa-sign-out-alt"></i> Chiqish
                                    </a>
                                </li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:login' %}">
                                <i class="fas fa-sign-in-alt"></i> Kirish
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:signup' %}">
                                <i class="fas fa-user-plus"></i> Ro'yxatga olish
                            </a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Content -->
    {% block content %}
    {% endblock %}

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p>&copy; 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Bosqich 7: Qo'shimcha template'lar yaratish

### 7.1 Mening yangilikfarim template'si

```html
<!-- templates/news/my_news_list.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>{{ title }}</h2>
                <a href="{% url 'news:create' %}" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Yangi yangilik qo'shish
                </a>
            </div>
            
            {% if news_list %}
                <div class="row">
                    {% for news in news_list %}
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card h-100">
                                {% if news.image %}
                                    <img src="{{ news.image.url }}" class="card-img-top" 
                                         alt="{{ news.title }}" style="height: 200px; object-fit: cover;">
                                {% else %}
                                    <div class="card-img-top bg-light d-flex align-items-center justify-content-center" 
                                         style="height: 200px;">
                                        <i class="fas fa-image fa-3x text-muted"></i>
                                    </div>
                                {% endif %}
                                
                                <div class="card-body d-flex flex-column">
                                    <h5 class="card-title">{{ news.title }}</h5>
                                    <p class="card-text text-muted small">
                                        {{ news.body|truncatewords:20 }}
                                    </p>
                                    
                                    <div class="mt-auto">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <small class="text-muted">
                                                {{ news.created_time|date:"d.m.Y" }}
                                            </small>
                                            <span class="badge bg-{% if news.status == 'PB' %}success{% else %}warning{% endif %}">
                                                {% if news.status == 'PB' %}Nashr etilgan{% else %}Kutilmoqda{% endif %}
                                            </span>
                                        </div>
                                        
                                        <div class="mt-2">
                                            <a href="{% url 'news:detail' slug=news.slug %}" 
                                               class="btn btn-sm btn-outline-primary">Ko'rish</a>
                                            <a href="{% url 'news:update' slug=news.slug %}" 
                                               class="btn btn-sm btn-outline-secondary">Tahrirlash</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-newspaper fa-4x text-muted mb-3"></i>
                    <h4 class="text-muted">Hali hech qanday yangilik yo'q</h4>
                    <p class="text-muted">Birinchi yangilikningizni yarating!</p>
                    <a href="{% url 'news:create' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Yangilik qo'shish
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### 7.2 Class-based Profile template'si

```html
<!-- templates/accounts/profile_class.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card border-info">
                <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">Foydalanuvchi profili</h4>
                    <small class="badge bg-light text-dark">Class-based View</small>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        <strong>Eslatma:</strong> Bu sahifa LoginRequiredMixin orqali himoyalangan.
                        Class-based view'lar uchun mo'ljallangan.
                    </div>
                    
                    <div class="row">
                        <div class="col-md-4 text-center">
                            <div class="bg-info rounded-circle d-inline-flex align-items-center justify-content-center" 
                                 style="width: 120px; height: 120px;">
                                <i class="fas fa-user fa-4x text-white"></i>
                            </div>
                            <h4 class="mt-3 text-info">{{ user.username }}</h4>
                        </div>
                        <div class="col-md-8">
                            <h6 class="text-info">Shaxsiy ma'lumotlar:</h6>
                            <table class="table table-hover">
                                <tr>
                                    <td><strong>To'liq ism:</strong></td>
                                    <td>
                                        {% if user.first_name and user.last_name %}
                                            {{ user.first_name }} {{ user.last_name }}
                                        {% else %}
                                            <span class="text-muted">Kiritilmagan</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Email:</strong></td>
                                    <td>{{ user.email|default:"Kiritilmagan" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Ro'yxatga olingan sana:</strong></td>
                                    <td>{{ user.date_joined|date:"d F Y, H:i" }}</td>
                                </tr>
                                <tr>
                                    <td><strong>Faollik holati:</strong></td>
                                    <td>
                                        {% if user.is_active %}
                                            <span class="badge bg-success">
                                                <i class="fas fa-check"></i> Faol
                                            </span>
                                        {% else %}
                                            <span class="badge bg-danger">
                                                <i class="fas fa-times"></i> Faol emas
                                            </span>
                                        {% endif %}
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="d-flex gap-2 flex-wrap">
                        <a href="{% url 'accounts:profile' %}" class="btn btn-outline-primary">
                            <i class="fas fa-arrow-left"></i> Function-based View
                        </a>
                        <a href="{% url 'accounts:edit_profile' %}" class="btn btn-info">
                            <i class="fas fa-edit"></i> Tahrirlash
                        </a>
                        <a href="{% url 'news:my_news' %}" class="btn btn-outline-success">
                            <i class="fas fa-newspaper"></i> Mening yangilikfarim
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">LoginRequiredMixin xususiyatlari</h6>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li><i class="fas fa-check text-success"></i> Avtomatik autentifikatsiya</li>
                        <li><i class="fas fa-check text-success"></i> Login URL'ni sozlash</li>
                        <li><i class="fas fa-check text-success"></i> Redirect after login</li>
                        <li><i class="fas fa-check text-success"></i> Class-based view'lar uchun</li>
                    </ul>
                    
                    <hr>
                    
                    <h6>Function vs Class farklar:</h6>
                    <small class="text-muted">
                        Function-based: @login_required dekorator<br>
                        Class-based: LoginRequiredMixin meros
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Bosqich 8: Testlash va debug

### 8.1 Migration qilish

```bash
# Terminal'da
python manage.py makemigrations
python manage.py migrate
```

### 8.2 Test foydalanuvchi yaratish

```bash
python manage.py createsuperuser
```

### 8.3 Serverni ishga tushirish va test qilish

```bash
python manage.py runserver
```

**Test qilinadigan sahifalar:**

1. `/accounts/login/` - Login sahifasi
2. `/accounts/profile/` - Profil sahifasi (login talab qilinadi)
3. `/accounts/edit-profile/` - Profil tahrirlash (login talab qilinadi)
4. `/create/` - Yangilik yaratish (login talab qilinadi)
5. `/my-news/` - Foydalanuvchining yangiliklarini ko'rish

## Bosqich 9: Xavfsizlik va optimizatsiya

### 9.1 Custom middleware yaratish (ixtiyoriy)

```python
# accounts/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class LoginRequiredMiddleware:
    """Global login required middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Himoyalanmaydigan URL'lar ro'yxati
        self.exempt_urls = [
            '/accounts/login/',
            '/accounts/signup/',
            '/',  # Bosh sahifa
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            # Himoyalanmaydigan URL'larni tekshirish
            if not any(path.startswith(url) for url in self.exempt_urls):
                if path.startswith('/admin/') or path.startswith('/accounts/'):
                    pass  # Admin va accounts URL'lari uchun maxsus
                else:
                    messages.info(request, 'Bu sahifaga kirish uchun tizimga kirishingiz kerak.')
                    return redirect('accounts:login')

        response = self.get_response(request)
        return response
```

### 9.2 Custom dekorator yaratish

```python
# accounts/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def staff_required(view_func):
    """Faqat staff foydalanuvchilar uchun"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Bu sahifaga kirish uchun admin huquqi kerak.')
            return redirect('news:home')
        return view_func(request, *args, **kwargs)
    return wrapper

# Ishlatish:
from .decorators import staff_required

@login_required
@staff_required
def admin_only_view(request):
    return render(request, 'admin_page.html')
```

## Xulosa va keyingi qadamlar

Ushbu amaliyotda biz:

✅ **@login_required** dekorator bilan function-based view'larni himoya qildik
✅ **LoginRequiredMixin** bilan class-based view'larni himoya qildik  
✅ Profil sahifalarini yaratdik va tahrirlash imkoniyatini qo'shdik
✅ Navigation bar'da autentifikatsiya holatini ko'rsatdik
✅ Xatoliklarni to'g'ri boshqardik va foydalanuvchiga tushuntirishlar berdik
✅ Template'larda himoya holatini ko'rsatdik

**Keyingi darsda:**
- Profil modelini yaratamiz
- Rasm yuklash funksiyasini qo'shamiz  
- Avatar va qo'shimcha ma'lumotlar bilan ishlaymiz

**Maslahatlar:**
- Har doim CSRF himoyasidan foydalaning
- Template'larda user.is_authenticated ni tekshiring
- Xatolik holatlarini to'g'ri boshqaring
- Messages framework'dan foydalanib foydalanuvchiga ma'lumot bering