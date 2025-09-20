# Lesson 33 Practice: Login va Logout Amaliyoti

## Amaliyot maqsadi

Bu amaliyotda siz Django loyihangizdagi yangiliklar saytiga to'liq login va logout funksiyasini qo'shishni o'rganasiz. Siz foydalanuvchilar uchun kirish-chiqish tizimini yaratib, himoyalangan sahifalar yasaydigan bo'lasiz.

## Boshlash oldidan

Oldingi darslardan yangiliklar loyihangiz tayyor bo'lishi kerak:
- `News` modeli
- Asosiy sahifalar (home, detail, category)
- Base template
- Bootstrap CSS

## 1-bosqich: URL konfiguratsiyasi

### 1.1. Asosiy URLs.py ni yangilash

`config/urls.py` faylini quyidagicha o'zgartiring:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Yangi qo'shing
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 1.2. URL'larni tekshirish

Terminalda quyidagi buyruqni bajaring:

```bash
python manage.py show_urls
```

Agar `show_urls` ishlamasa, quyidagi URL'lar mavjudligini tekshiring:
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/password_change/`
- `/accounts/password_reset/`

## 2-bosqich: Template'lar yaratish

### 2.1. Registration papkasini yaratish

```bash
# Terminal'da loyiha papkasida
mkdir -p templates/registration
```

### 2.2. Login template yaratish

`templates/registration/login.html` faylini yarating:

```html
<!-- templates/registration/login.html -->
{% load static %}
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saytga kirish - Yangiliklar</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container">
        <div class="row justify-content-center" style="min-height: 100vh; align-items: center;">
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-lg">
                    <div class="card-header bg-primary text-white text-center">
                        <h3 class="mb-0">
                            <i class="fas fa-sign-in-alt me-2"></i>Saytga kirish
                        </h3>
                    </div>
                    <div class="card-body p-4">
                        <!-- Xato xabarlari -->
                        {% if form.errors %}
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <strong>Xato!</strong>
                                {% if form.non_field_errors %}
                                    {{ form.non_field_errors.0 }}
                                {% else %}
                                    Foydalanuvchi nomi yoki parol noto'g'ri.
                                {% endif %}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endif %}

                        <!-- Login forma -->
                        <form method="post">
                            {% csrf_token %}
                            
                            <div class="mb-3">
                                <label for="{{ form.username.id_for_label }}" class="form-label">
                                    <i class="fas fa-user me-1"></i>Foydalanuvchi nomi
                                </label>
                                <input type="text" 
                                       name="{{ form.username.name }}" 
                                       id="{{ form.username.id_for_label }}"
                                       class="form-control form-control-lg {% if form.username.errors %}is-invalid{% endif %}"
                                       value="{{ form.username.value|default_if_none:'' }}"
                                       required>
                                {% if form.username.errors %}
                                    <div class="invalid-feedback">
                                        {{ form.username.errors.0 }}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="mb-3">
                                <label for="{{ form.password.id_for_label }}" class="form-label">
                                    <i class="fas fa-lock me-1"></i>Parol
                                </label>
                                <input type="password" 
                                       name="{{ form.password.name }}" 
                                       id="{{ form.password.id_for_label }}"
                                       class="form-control form-control-lg {% if form.password.errors %}is-invalid{% endif %}"
                                       required>
                                {% if form.password.errors %}
                                    <div class="invalid-feedback">
                                        {{ form.password.errors.0 }}
                                    </div>
                                {% endif %}
                            </div>

                            <div class="d-grid mb-3">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-sign-in-alt me-2"></i>Kirish
                                </button>
                            </div>
                            
                            <input type="hidden" name="next" value="{{ next }}" />
                        </form>
                        
                        <!-- Qo'shimcha havolalar -->
                        <div class="text-center">
                            <div class="row">
                                <div class="col-12 mb-2">
                                    <a href="#" class="text-decoration-none small">
                                        Parolni unutdingizmi?
                                    </a>
                                </div>
                                <div class="col-12 mb-2">
                                    <a href="#" class="text-decoration-none small">
                                        Ro'yxatdan o'tish
                                    </a>
                                </div>
                                <div class="col-12">
                                    <a href="{% url 'news:home' %}" class="btn btn-outline-secondary">
                                        <i class="fas fa-home me-1"></i>Bosh sahifaga qaytish
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Font Awesome va Bootstrap JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 2.3. Logged_out template yaratish

`templates/registration/logged_out.html` yarating:

```html
<!-- templates/registration/logged_out.html -->
{% extends 'base.html' %}

{% block title %}Saytdan chiqildi{% endblock title %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h2 class="text-success">
                        <i class="fas fa-check-circle me-2"></i>
                        Muvaffaqiyatli chiqildi!
                    </h2>
                    <p class="lead">Siz muvaffaqiyatli tarzda saytdan chiqildinggiz.</p>
                    <div class="d-grid gap-2">
                        <a href="{% url 'news:home' %}" class="btn btn-primary">
                            <i class="fas fa-home me-2"></i>Bosh sahifaga o'tish
                        </a>
                        <a href="{% url 'login' %}" class="btn btn-outline-primary">
                            <i class="fas fa-sign-in-alt me-2"></i>Qayta kirish
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

## 3-bosqich: Base template'ni yangilash

### 3.1. Navigation'ga authentication qo'shish

`templates/base.html` faylini yangilang:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
{% load static %}
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock title %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{% url 'news:home' %}">
                <i class="fas fa-newspaper me-2"></i>Yangiliklar
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <!-- Sol tomon menu -->
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:home' %}">
                            <i class="fas fa-home me-1"></i>Bosh sahifa
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:category_list' %}">
                            <i class="fas fa-list me-1"></i>Kategoriyalar
                        </a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-plus me-1"></i>Yangilik qo'shish
                            </a>
                        </li>
                    {% endif %}
                </ul>
                
                <!-- O'ng tomon authentication -->
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user-circle me-1"></i>{{ user.username }}
                                {% if user.is_superuser %}
                                    <span class="badge bg-warning text-dark">Admin</span>
                                {% endif %}
                            </a>
                            <ul class="dropdown-menu">
                                <li>
                                    <h6 class="dropdown-header">
                                        <i class="fas fa-info-circle me-1"></i>Profil ma'lumotlari
                                    </h6>
                                </li>
                                <li><a class="dropdown-item" href="#">
                                    <i class="fas fa-user me-2"></i>Profil
                                </a></li>
                                <li><a class="dropdown-item" href="#">
                                    <i class="fas fa-cog me-2"></i>Sozlamalar
                                </a></li>
                                <li><a class="dropdown-item" href="#">
                                    <i class="fas fa-key me-2"></i>Parolni o'zgartirish
                                </a></li>
                                {% if user.is_staff %}
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item" href="{% url 'admin:index' %}">
                                        <i class="fas fa-tools me-2"></i>Admin panel
                                    </a></li>
                                {% endif %}
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="{% url 'logout' %}">
                                    <i class="fas fa-sign-out-alt me-2"></i>Chiqish
                                </a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">
                                <i class="fas fa-sign-in-alt me-1"></i>Kirish
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-user-plus me-1"></i>Ro'yxatdan o'tish
                            </a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main content -->
    <main class="py-4">
        {% block content %}
        {% endblock content %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Yangiliklar sayti</h5>
                    <p class="mb-0">Eng so'nggi yangiliklar bilan tanishing.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="mb-0">© 2024 Barcha huquqlar himoyalangan.</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## 4-bosqich: Settings.py ni sozlash

### 4.1. Authentication sozlamalarini qo'shish

`config/settings.py` faylining oxiriga qo'shing:

```python
# config/settings.py

# ... boshqa sozlamalar

# Authentication sozlamalari
LOGIN_URL = 'login'  # Login sahifasi URL nomi
LOGIN_REDIRECT_URL = '/'  # Login qilgandan keyin yo'naltirish
LOGOUT_REDIRECT_URL = '/'  # Logout qilgandan keyin yo'naltirish

# Session sozlamalari
SESSION_COOKIE_AGE = 86400  # 24 soat (sekund)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
```

### 4.2. Static va Media sozlamalarini tekshirish

```python
# config/settings.py

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 5-bosqich: Views'ni yangilash

### 5.1. Himoyalangan sahifalar yaratish

`news/views.py` faylini yangilang:

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import News, Category

class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news_list'
    paginate_by = 6
    
    def get_queryset(self):
        return News.objects.filter(status=News.Status.Published).select_related('category')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.filter(status=News.Status.Published)

class CategoryListView(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

# Himoyalangan view'lar (faqat login qilganlar uchun)
class NewsCreateView(LoginRequiredMixin, CreateView):
    """Yangilik qo'shish - faqat login qilganlar uchun"""
    model = News
    fields = ['title', 'slug', 'body', 'category', 'photo']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = News.Status.Published
        messages.success(self.request, 'Yangilik muvaffaqiyatli qo\'shildi!')
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Yangilikni tahrirlash - faqat muallif uchun"""
    model = News
    fields = ['title', 'slug', 'body', 'category', 'photo']
    template_name = 'news/news_form.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser
    
    def form_valid(self, form):
        messages.success(self.request, 'Yangilik muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Yangilikni o'chirish - faqat muallif uchun"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:home')
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Yangilik muvaffaqiyatli o\'chirildi!')
        return super().delete(request, *args, **kwargs)

# Login talab qiladigan funksiya view
@login_required
def user_profile(request):
    """Foydalanuvchi profili - faqat login qilganlar uchun"""
    user_news = News.objects.filter(author=request.user)
    context = {
        'user_news': user_news,
        'total_news': user_news.count(),
        'published_news': user_news.filter(status=News.Status.Published).count(),
        'draft_news': user_news.filter(status=News.Status.Draft).count(),
    }
    return render(request, 'news/user_profile.html', context)

# AJAX view (himoyalangan)
@login_required
def like_news(request):
    """Yangiliklarni like qilish - faqat login qilganlar uchun"""
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        news = get_object_or_404(News, id=news_id)
        # Like logikasi bu yerda bo'ladi
        return JsonResponse({'status': 'success', 'message': 'Like qo\'shildi!'})
    return JsonResponse({'status': 'error', 'message': 'Xato so\'rov!'})
```

### 5.2. URL'larni yangilash

`news/urls.py` faylini yangilang:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    
    # Himoyalangan sahifalar
    path('add/', views.NewsCreateView.as_view(), name='news_add'),
    path('news/<slug:slug>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<slug:slug>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # AJAX
    path('like/', views.like_news, name='like_news'),
]
```

## 6-bosqich: Himoyalangan template'lar yaratish

### 6.1. Yangilik qo'shish forması

`templates/news/news_form.html` yarating:

```html
<!-- templates/news/news_form.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}
    {% if form.instance.pk %}Yangiliklarni tahrirlash{% else %}Yangilik qo'shish{% endif %}
{% endblock title %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-{% if form.instance.pk %}edit{% else %}plus{% endif %} me-2"></i>
                        {% if form.instance.pk %}Yangiliklarni tahrirlash{% else %}Yangilik qo'shish{% endif %}
                    </h4>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="id_title" class="form-label">Sarlavha *</label>
                            {{ form.title }}
                            {% if form.title.errors %}
                                <div class="text-danger">{{ form.title.errors.0 }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_slug" class="form-label">Slug *</label>
                            {{ form.slug }}
                            <div class="form-text">URL uchun ishlatiladi. Masalan: yangi-yangilik</div>
                            {% if form.slug.errors %}
                                <div class="text-danger">{{ form.slug.errors.0 }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_category" class="form-label">Kategoriya *</label>
                            {{ form.category }}
                            {% if form.category.errors %}
                                <div class="text-danger">{{ form.category.errors.0 }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_photo" class="form-label">Rasm</label>
                            {{ form.photo }}
                            {% if form.instance.photo %}
                                <div class="mt-2">
                                    <img src="{{ form.instance.photo.url }}" alt="Current photo" class="img-thumbnail" width="200">
                                    <p class="small text-muted">Joriy rasm</p>
                                </div>
                            {% endif %}
                            {% if form.photo.errors %}
                                <div class="text-danger">{{ form.photo.errors.0 }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_body" class="form-label">Matn *</label>
                            {{ form.body }}
                            {% if form.body.errors %}
                                <div class="text-danger">{{ form.body.errors.0 }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'news:home' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left me-2"></i>Bekor qilish
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-save me-2"></i>Saqlash
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 6.2. Yangilik o'chirish tasdiqi

`templates/news/news_confirm_delete.html` yarating:

```html
<!-- templates/news/news_confirm_delete.html -->
{% extends 'base.html' %}

{% block title %}Yangiliklarni o'chirish{% endblock title %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>O'chirish tasdiqi
                    </h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning">
                        <i class="fas fa-warning me-2"></i>
                        <strong>Diqqat!</strong> Bu amalni qaytarib bo'lmaydi.
                    </div>
                    
                    <p>Quyidagi yangilikni o'chirishni xohlaysizmi?</p>
                    
                    <div class="border rounded p-3 mb-3 bg-light">
                        <h5 class="mb-1">{{ object.title }}</h5>
                        <small class="text-muted">
                            {{ object.created_time|date:"d.m.Y H:i" }} | {{ object.category }}
                        </small>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-between">
                            <a href="{{ object.get_absolute_url }}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left me-2"></i>Bekor qilish
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash me-2"></i>O'chirish
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 6.3. Foydalanuvchi profili

`templates/news/user_profile.html` yarating:

```html
<!-- templates/news/user_profile.html -->
{% extends 'base.html' %}

{% block title %}{{ user.username }} - Profil{% endblock title %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-user-circle fa-5x text-primary"></i>
                    </div>
                    <h4>{{ user.get_full_name|default:user.username }}</h4>
                    <p class="text-muted">{{ user.email }}</p>
                    <small class="text-muted">
                        Qo'shilgan sana: {{ user.date_joined|date:"d.m.Y" }}
                    </small>
                </div>
            </div>
            
            <div class="card mt-3">
                <div class="card-header">
                    <h5 class="mb-0">Statistika</h5>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="border-end">
                                <h4 class="text-primary">{{ total_news }}</h4>
                                <small>Jami</small>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="border-end">
                                <h4 class="text-success">{{ published_news }}</h4>
                                <small>Nashr</small>
                            </div>
                        </div>
                        <div class="col-4">
                            <h4 class="text-warning">{{ draft_news }}</h4>
                            <small>Qoralama</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-8">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Mening yangiliklar</h5>
                    <a href="{% url 'news:news_add' %}" class="btn btn-primary btn-sm">
                        <i class="fas fa-plus me-1"></i>Yangi qo'shish
                    </a>
                </div>
                <div class="card-body">
                    {% if user_news %}
                        {% for news in user_news %}
                            <div class="card mb-3">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-3">
                                            {% if news.photo %}
                                                <img src="{{ news.photo.url }}" alt="{{ news.title }}" 
                                                     class="img-fluid rounded">
                                            {% else %}
                                                <div class="bg-light rounded d-flex align-items-center justify-content-center" 
                                                     style="height: 100px;">
                                                    <i class="fas fa-image fa-2x text-muted"></i>
                                                </div>
                                            {% endif %}
                                        </div>
                                        <div class="col-md-9">
                                            <h6>
                                                <a href="{{ news.get_absolute_url }}" class="text-decoration-none">
                                                    {{ news.title }}
                                                </a>
                                                <span class="badge bg-{% if news.status == 'PB' %}success{% else %}warning{% endif %} ms-2">
                                                    {{ news.get_status_display }}
                                                </span>
                                            </h6>
                                            <p class="text-muted small mb-2">
                                                <i class="fas fa-calendar me-1"></i>{{ news.created_time|date:"d.m.Y H:i" }} |
                                                <i class="fas fa-folder me-1"></i>{{ news.category }}
                                            </p>
                                            <p class="text-truncate">{{ news.body|truncatewords:15 }}</p>
                                            <div class="btn-group btn-group-sm">
                                                <a href="{{ news.get_absolute_url }}" class="btn btn-outline-primary">
                                                    <i class="fas fa-eye me-1"></i>Ko'rish
                                                </a>
                                                <a href="{% url 'news:news_edit' news.slug %}" class="btn btn-outline-warning">
                                                    <i class="fas fa-edit me-1"></i>Tahrirlash
                                                </a>
                                                <a href="{% url 'news:news_delete' news.slug %}" class="btn btn-outline-danger">
                                                    <i class="fas fa-trash me-1"></i>O'chirish
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <div class="text-center py-5">
                            <i class="fas fa-newspaper fa-3x text-muted mb-3"></i>
                            <h5>Yangiliklar topilmadi</h5>
                            <p class="text-muted">Siz hali birorta yangilik qo'shmagansiz.</p>
                            <a href="{% url 'news:news_add' %}" class="btn btn-primary">
                                <i class="fas fa-plus me-2"></i>Birinchi yangilikni qo'shing
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

## 7-bosqich: News detail template'ni yangilash

### 7.1. Himoyalangan harakatlarni qo'shish

`templates/news/news_detail.html` ni yangilang:

```html
<!-- templates/news/news_detail.html ga qo'shish -->
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <!-- Yangilik ma'lumotlari -->
            <article class="mb-4">
                <!-- ... oldingi kod ... -->
                
                <!-- Harakatlar (Actions) -->
                <div class="card mt-4">
                    <div class="card-body">
                        {% if user.is_authenticated %}
                            <div class="row">
                                <div class="col-md-6">
                                    <!-- Like va Share tugmalari -->
                                    <button class="btn btn-outline-success btn-sm me-2" onclick="likeNews({{ news.id }})">
                                        <i class="fas fa-thumbs-up me-1"></i>Like
                                    </button>
                                    <button class="btn btn-outline-info btn-sm me-2">
                                        <i class="fas fa-share me-1"></i>Ulashish
                                    </button>
                                    <button class="btn btn-outline-warning btn-sm">
                                        <i class="fas fa-bookmark me-1"></i>Saqlash
                                    </button>
                                </div>
                                <div class="col-md-6 text-end">
                                    {% if user == news.author or user.is_superuser %}
                                        <!-- Faqat muallif yoki admin ko'ra oladi -->
                                        <div class="btn-group">
                                            <a href="{% url 'news:news_edit' news.slug %}" class="btn btn-warning btn-sm">
                                                <i class="fas fa-edit me-1"></i>Tahrirlash
                                            </a>
                                            <a href="{% url 'news:news_delete' news.slug %}" class="btn btn-danger btn-sm">
                                                <i class="fas fa-trash me-1"></i>O'chirish
                                            </a>
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                        {% else %}
                            <div class="alert alert-info text-center">
                                <i class="fas fa-info-circle me-2"></i>
                                Izoh qoldirish va boshqa harakatlar uchun 
                                <a href="{% url 'login' %}?next={{ request.path }}" class="alert-link">saytga kiring</a>.
                            </div>
                        {% endif %}
                    </div>
                </div>
            </article>
        </div>
        
        <!-- Sidebar -->
        <div class="col-md-4">
            <!-- ... sidebar kontenti ... -->
        </div>
    </div>
</div>

<!-- JavaScript -->
<script>
function likeNews(newsId) {
    {% if user.is_authenticated %}
        fetch('{% url "news:like_news" %}', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'news_id=' + newsId
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
            }
        });
    {% else %}
        window.location.href = '{% url "login" %}?next={{ request.path }}';
    {% endif %}
}
</script>
{% endblock content %}
```

## 8-bosqich: Test foydalanuvchilar yaratish

### 8.1. Superuser yaratish

```bash
python manage.py createsuperuser
```

Ma'lumotlarni kiriting:
- Username: admin
- Email: admin@example.com  
- Password: (kuchli parol)

### 8.2. Oddiy foydalanuvchi yaratish

Django shell orqali:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Oddiy foydalanuvchi yaratish
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)

print(f"Foydalanuvchi yaratildi: {user.username}")
exit()
```

## 9-bosqich: Test qilish

### 9.1. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 9.2. Sahifalarni sinab ko'rish

1. **Login sahifasi:** `http://127.0.0.1:8000/accounts/login/`
2. **Admin panel:** `http://127.0.0.1:8000/admin/`  
3. **Bosh sahifa:** `http://127.0.0.1:8000/`

### 9.3. Testlar ro'yxati

✅ **Login funksiyasi:**
- [ ] Login sahifasi ochiladi
- [ ] To'g'ri ma'lumotlar bilan kirish
- [ ] Noto'g'ri ma'lumotlar bilan xato
- [ ] Login qilgandan keyin bosh sahifaga yo'naltirish

✅ **Logout funksiyasi:**
- [ ] Logout tugmasi navigation'da ko'rinadi
- [ ] Logout qilgandan keyin bosh sahifaga yo'naltirish
- [ ] Logged out sahifasi ko'rsatiladi

✅ **Navigation:**
- [ ] Login qilmagan: "Kirish" va "Ro'yxat" ko'rinadi
- [ ] Login qilgan: Username va dropdown menu ko'rinadi
- [ ] Admin badge superuser uchun ko'rinadi

✅ **Himoyalangan sahifalar:**
- [ ] `/add/` - login talab qiladi
- [ ] `/profile/` - login talab qiladi
- [ ] Edit va Delete tugmalari faqat muallif uchun

## 10-bosqich: Xatolarni tuzatish

### 10.1. Keng uchraydigan xatolar va yechimlar

**1. Template topilmadi:**
```
TemplateDoesNotExist: registration/login.html
```
**Yechim:** 
- `templates/registration/` papka yaratilganligini tekshiring
- `TEMPLATES` sozlamalarida `'DIRS': [BASE_DIR / 'templates']` borligini tekshiring

**2. CSRF xatosi:**
```
Forbidden (403) CSRF verification failed
```  
**Yechim:**
- Barcha formalariga `{% csrf_token %}` qo'shing
- AJAX so'rovlarda CSRF token jo'nating

**3. URL xatosi:**
```
NoReverseMatch: Reverse for 'login' not found
```
**Yechim:**
- `config/urls.py` da `path('accounts/', include('django.contrib.auth.urls'))` borligini tekshiring

**4. Static fayllar yuklanmaydi:**
**Yechim:**
```python
# config/urls.py ga qo'shing
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**5. Permission xatosi:**
```
PermissionDenied
```
**Yechim:**
- `UserPassesTestMixin` da `test_func` to'g'ri yozilganligini tekshiring
- Foydalanuvchi huquqlari to'g'riligini tekshiring

## Xulosa

Bu amaliyotda siz quyidagilarni amalga oshirdingiz:

1. ✅ Django authentication tizimini sozladingiz
2. ✅ Login va logout sahifalari yaratdingiz  
3. ✅ Navigation'da authentication holati ko'rsatildi
4. ✅ Himoyalangan sahifalar yaratdingiz
5. ✅ Foydalanuvchi profili qo'shdingiz
6. ✅ CRUD operatsiyalari uchun ruxsatnomalar sozladingiz
7. ✅ Test foydalanuvchilar yaratdingiz

## Keyingi qadamlar

1. **Foydalanuvchi ro'yxatdan o'tish** - signup funksiyasi
2. **Parol tiklash** - password reset
3. **Profil ma'lumotlarini tahrirlash**
4. **Foydalanuvchi rasmlari** - avatar upload
5. **Social authentication** - Google, Facebook login

## Maslahatlar

1. **Xavfsizlik:** Har doim strong password policy qo'llang
2. **UX:** Login/logout jarayonini sodda va tushunarli qiling  
3. **Testing:** Authentication bilan bog'liq barcha funksiyalarni test qiling
4. **Error Handling:** Foydalanuvchilarga tushunarli xato xabarlari ko'rsating
5. **Responsive:** Mobile qurilmalarda ham yaxshi ko'rinishi kerak