# 25-dars: Template teglari - Amaliyot

## Amaliyot maqsadi
Ushbu amaliyotda Django template teglarini qo'llash orqali yangiliklar loyihasini to'liq ishlaydigan holatga keltiramiz. Barcha sahifalarni dinamik qilib, foydalanuvchi tajribasini yaxshilaymiz.

## Bosqichma-bosqich amaliyot

### 1-bosqich: Loyihani tayyorlash

Avvalo loyihangizni ishga tushiring va kerakli fayllarni yarating:

```bash
# Terminal
cd yangiliklar_loyihasi
python manage.py runserver
```

Loyiha tuzilmasi quyidagicha bo'lishi kerak:
```
yangiliklar_loyihasi/
├── templates/
│   ├── base.html
│   └── news/
│       ├── home.html
│       ├── detail.html
│       ├── category.html
│       └── all_news.html
├── static/
│   └── css/
│       └── style.css
└── news/
    ├── models.py
    ├── views.py
    └── urls.py
```

### 2-bosqich: Base template yaratish

`templates/base.html` faylini yarating:

```html
<!-- templates/base.html -->
{% load static %}
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
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Header Navigation -->
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <!-- Brand -->
                <a class="navbar-brand fw-bold" href="{% url 'news:home' %}">
                    <i class="fas fa-newspaper"></i> Yangiliklar
                </a>
                
                <!-- Mobile toggle -->
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <!-- Navigation links -->
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:home' %}">
                                <i class="fas fa-home"></i> Bosh sahifa
                            </a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-list"></i> Kategoriyalar
                            </a>
                            <ul class="dropdown-menu">
                                {% for kategoriya in kategoriyalar %}
                                <li>
                                    <a class="dropdown-item" href="{% url 'news:category' kategoriya.slug %}">
                                        {{ kategoriya.nom }}
                                    </a>
                                </li>
                                {% endfor %}
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:all_news' %}">
                                <i class="fas fa-newspaper"></i> Barcha yangiliklar
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:contact' %}">
                                <i class="fas fa-envelope"></i> Aloqa
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main content -->
    <main class="min-vh-100">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-newspaper"></i> Yangiliklar sayti</h5>
                    <p class="small">Eng so'nggi va ishonchli yangiliklar bilan tanishing</p>
                </div>
                <div class="col-md-3">
                    <h6>Foydali havolalar</h6>
                    <ul class="list-unstyled small">
                        <li><a href="{% url 'news:home' %}" class="text-light text-decoration-none">Bosh sahifa</a></li>
                        <li><a href="{% url 'news:all_news' %}" class="text-light text-decoration-none">Barcha yangiliklar</a></li>
                        <li><a href="{% url 'news:contact' %}" class="text-light text-decoration-none">Aloqa</a></li>
                    </ul>
                </div>
                <div class="col-md-3">
                    <h6>Ijtimoiy tarmoqlar</h6>
                    <div class="d-flex gap-2">
                        <a href="#" class="text-light"><i class="fab fa-facebook"></i></a>
                        <a href="#" class="text-light"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-light"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="text-light"><i class="fab fa-telegram"></i></a>
                    </div>
                </div>
            </div>
            <hr class="my-3">
            <div class="text-center small">
                <p>&copy; {% now "Y" %} Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 3-bosqich: Bosh sahifa templateni to'ldirish

`templates/news/home.html` faylini yarating:

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="container py-4">
    <!-- Hero Banner -->
    <div class="jumbotron bg-gradient text-white p-5 rounded-3 mb-5" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="row align-items-center">
            <div class="col-md-8">
                <h1 class="display-4 fw-bold">So'nggi yangiliklar</h1>
                <p class="lead">Dunyodagi eng muhim voqealar va yangiliklar bilan tanishib boring</p>
                <a href="{% url 'news:all_news' %}" class="btn btn-light btn-lg mt-3">
                    <i class="fas fa-arrow-right"></i> Barcha yangiliklarni ko'rish
                </a>
            </div>
            <div class="col-md-4 text-center">
                <i class="fas fa-globe-americas fa-5x opacity-50"></i>
            </div>
        </div>
    </div>

    <!-- Trending News -->
    {% if featured_news %}
    <section class="mb-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="h3 fw-bold">
                <i class="fas fa-fire text-danger"></i> Eng ommabop yangiliklar
            </h2>
            <span class="badge bg-primary">{{ featured_news|length }} ta yangilik</span>
        </div>
        
        <div class="row g-4">
            {% for yangilik in featured_news %}
            <div class="col-lg-6">
                <article class="card h-100 shadow-sm hover-shadow">
                    <div class="row g-0 h-100">
                        {% if yangilik.rasm %}
                        <div class="col-md-5">
                            <img src="{{ yangilik.rasm.url }}" 
                                 class="img-fluid h-100 w-100" 
                                 style="object-fit: cover;" 
                                 alt="{{ yangilik.sarlavha }}">
                        </div>
                        <div class="col-md-7">
                        {% else %}
                        <div class="col-12">
                        {% endif %}
                            <div class="card-body d-flex flex-column h-100">
                                <div class="mb-2">
                                    <span class="badge bg-{{ yangilik.kategoriya.rang|default:'secondary' }}">
                                        {{ yangilik.kategoriya.nom }}
                                    </span>
                                    <small class="text-muted ms-2">
                                        <i class="fas fa-eye"></i> {{ yangilik.ko_rishlar_soni }}
                                    </small>
                                </div>
                                
                                <h5 class="card-title">
                                    <a href="{% url 'news:detail' yangilik.pk %}" 
                                       class="text-decoration-none text-dark">
                                        {{ yangilik.sarlavha }}
                                    </a>
                                </h5>
                                
                                <p class="card-text flex-grow-1">
                                    {{ yangilik.qisqa_mazmun|truncatewords:15 }}
                                </p>
                                
                                <div class="d-flex justify-content-between align-items-center mt-auto">
                                    <small class="text-muted">
                                        <i class="fas fa-calendar-alt"></i> 
                                        {{ yangilik.yaratilgan_sana|date:"d M, Y" }}
                                    </small>
                                    <a href="{% url 'news:detail' yangilik.pk %}" 
                                       class="btn btn-outline-primary btn-sm">
                                        Batafsil <i class="fas fa-arrow-right"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- News by Categories -->
    <section>
        <h2 class="h3 fw-bold mb-4">
            <i class="fas fa-th-large"></i> Kategoriyalar bo'yicha yangiliklar
        </h2>
        
        {% for kategoriya, yangiliklar in yangiliklar_by_category.items %}
        {% if yangiliklar %}
        <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="h4">
                    <span class="badge bg-{{ kategoriya.rang|default:'info' }} fs-6">
                        <i class="fas fa-tag"></i> {{ kategoriya.nom }}
                    </span>
                </h3>
                <a href="{% url 'news:category' kategoriya.slug %}" 
                   class="text-decoration-none small">
                    Barchasini ko'rish <i class="fas fa-arrow-right"></i>
                </a>
            </div>
            
            <div class="row g-3">
                {% for yangilik in yangiliklar %}
                <div class="col-md-6 col-lg-4">
                    <article class="card h-100 border-0 shadow-sm">
                        {% if yangilik.rasm %}
                        <div class="position-relative">
                            <img src="{{ yangilik.rasm.url }}" 
                                 class="card-img-top" 
                                 style="height: 200px; object-fit: cover;" 
                                 alt="{{ yangilik.sarlavha }}">
                            <div class="position-absolute top-0 start-0 m-2">
                                <span class="badge bg-dark bg-opacity-75">
                                    {{ yangilik.kategoriya.nom }}
                                </span>
                            </div>
                        </div>
                        {% endif %}
                        
                        <div class="card-body">
                            <h6 class="card-title">
                                <a href="{% url 'news:detail' yangilik.pk %}" 
                                   class="text-decoration-none text-dark">
                                    {{ yangilik.sarlavha|truncatechars:60 }}
                                </a>
                            </h6>
                            
                            <p class="card-text small text-muted">
                                {{ yangilik.qisqa_mazmun|truncatewords:12 }}
                            </p>
                            
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    {{ yangilik.yaratilgan_sana|date:"d M" }}
                                </small>
                                <a href="{% url 'news:detail' yangilik.pk %}" 
                                   class="btn btn-sm btn-outline-primary">
                                    O'qish
                                </a>
                            </div>
                        </div>
                    </article>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        {% empty %}
        <div class="text-center py-5">
            <i class="fas fa-newspaper fa-3x text-muted mb-3"></i>
            <h4 class="text-muted">Hozircha yangilik yo'q</h4>
            <p class="text-muted">Tez orada yangi yangiliklar qo'shiladi.</p>
        </div>
        {% endfor %}
    </section>
</div>

<!-- Custom CSS for hover effects -->
<style>
.hover-shadow {
    transition: box-shadow 0.3s ease;
}
.hover-shadow:hover {
    box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important;
}
</style>
{% endblock %}
```

### 4-bosqich: Detail sahifani yaratish

`templates/news/detail.html` faylini to'ldiring:

```html
<!-- templates/news/detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ yangilik.sarlavha }} - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="container py-4">
    <article>
        <!-- Breadcrumb -->
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="{% url 'news:home' %}" class="text-decoration-none">
                        <i class="fas fa-home"></i> Bosh sahifa
                    </a>
                </li>
                <li class="breadcrumb-item">
                    <a href="{% url 'news:category' yangilik.kategoriya.slug %}" 
                       class="text-decoration-none">
                        {{ yangilik.kategoriya.nom }}
                    </a>
                </li>
                <li class="breadcrumb-item active">
                    {{ yangilik.sarlavha|truncatewords:8 }}
                </li>
            </ol>
        </nav>

        <!-- Article Header -->
        <header class="mb-4">
            <div class="mb-3">
                <span class="badge bg-primary fs-6 me-2">
                    <i class="fas fa-tag"></i> {{ yangilik.kategoriya.nom }}
                </span>
                {% if yangilik.teglar.all %}
                    {% for teg in yangilik.teglar.all %}
                    <span class="badge bg-secondary me-1">#{{ teg.nom }}</span>
                    {% endfor %}
                {% endif %}
            </div>
            
            <h1 class="display-5 fw-bold mb-4">{{ yangilik.sarlavha }}</h1>
            
            <!-- Article Meta -->
            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="d-flex align-items-center text-muted">
                        <i class="fas fa-user-circle me-2"></i>
                        <span>{{ yangilik.muallif.get_full_name|default:yangilik.muallif.username }}</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex align-items-center text-muted">
                        <i class="fas fa-calendar-alt me-2"></i>
                        <span>{{ yangilik.yaratilgan_sana|date:"d F, Y H:i" }}</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex align-items-center text-muted">
                        <i class="fas fa-eye me-2"></i>
                        <span>{{ yangilik.ko_rishlar_soni }} marta ko'rilgan</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex align-items-center text-muted">
                        <i class="fas fa-clock me-2"></i>
                        <span>O'qish vaqti: ~{{ yangilik.matn|wordcount|floatformat:0|add:"60"|div:200 }} daqiqa</span>
                    </div>
                </div>
            </div>
            
            <!-- Featured Image -->
            {% if yangilik.rasm %}
            <div class="mb-4">
                <img src="{{ yangilik.rasm.url }}" 
                     class="img-fluid rounded shadow" 
                     alt="{{ yangilik.sarlavha }}"
                     style="width: 100%; max-height: 400px; object-fit: cover;">
            </div>
            {% endif %}
            
            <!-- Article Summary -->
            {% if yangilik.qisqa_mazmun %}
            <div class="alert alert-info border-start border-primary border-4 mb-4">
                <h6 class="fw-bold"><i class="fas fa-info-circle"></i> Qisqacha:</h6>
                <p class="mb-0">{{ yangilik.qisqa_mazmun }}</p>
            </div>
            {% endif %}
        </header>

        <!-- Article Content -->
        <div class="article-content mb-5">
            <div class="fs-5 lh-lg">
                {{ yangilik.matn|linebreaks }}
            </div>
        </div>

        <!-- Social Sharing -->
        <div class="border-top border-bottom py-4 mb-4">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <h6 class="mb-2 mb-md-0">
                        <i class="fas fa-share-alt"></i> Yangilikning boshqalar bilan bo'lishing:
                    </h6>
                </div>
                <div class="col-md-6">
                    <div class="d-flex gap-2 justify-content-md-end">
                        <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}" 
                           class="btn btn-outline-primary btn-sm" target="_blank">
                            <i class="fab fa-facebook-f"></i> Facebook
                        </a>
                        <a href="https://twitter.com/intent/tweet?url={{ request.build_absolute_uri }}&text={{ yangilik.sarlavha }}" 
                           class="btn btn-outline-info btn-sm" target="_blank">
                            <i class="fab fa-twitter"></i> Twitter
                        </a>
                        <a href="https://t.me/share/url?url={{ request.build_absolute_uri }}&text={{ yangilik.sarlavha }}" 
                           class="btn btn-outline-primary btn-sm" target="_blank">
                            <i class="fab fa-telegram"></i> Telegram
                        </a>
                        <button class="btn btn-outline-secondary btn-sm" 
                                onclick="navigator.clipboard.writeText('{{ request.build_absolute_uri }}')">
                            <i class="fas fa-link"></i> Nusxa olish
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </article>

    <!-- Related Articles -->
    {% if tegdosh_yangiliklar %}
    <section>
        <h3 class="h4 fw-bold mb-4">
            <i class="fas fa-newspaper"></i> Shunga o'xshash yangiliklar
        </h3>
        
        <div class="row g-4">
            {% for yangilik in tegdosh_yangiliklar %}
            <div class="col-md-6 col-lg-4">
                <article class="card h-100 border-0 shadow-sm">
                    {% if yangilik.rasm %}
                    <div class="position-relative">
                        <img src="{{ yangilik.rasm.url }}" 
                             class="card-img-top" 
                             style="height: 200px; object-fit: cover;">
                        <div class="position-absolute top-0 end-0 m-2">
                            <span class="badge bg-dark bg-opacity-75">
                                {{ yangilik.yaratilgan_sana|date:"d M" }}
                            </span>
                        </div>
                    </div>
                    {% endif %}
                    
                    <div class="card-body">
                        <span class="badge bg-primary mb-2">{{ yangilik.kategoriya.nom }}</span>
                        <h6 class="card-title">
                            <a href="{% url 'news:detail' yangilik.pk %}" 
                               class="text-decoration-none text-dark">
                                {{ yangilik.sarlavha }}
                            </a>
                        </h6>
                        <p class="card-text small text-muted">
                            {{ yangilik.qisqa_mazmun|truncatewords:15 }}
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                <i class="fas fa-eye"></i> {{ yangilik.ko_rishlar_soni }}
                            </small>
                            <a href="{% url 'news:detail' yangilik.pk %}" 
                               class="btn btn-sm btn-primary">
                                O'qish <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </article>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
    
    <!-- Navigation buttons -->
    <div class="d-flex justify-content-between mt-5">
        <a href="{% url 'news:category' yangilik.kategoriya.slug %}" 
           class="btn btn-outline-secondary">
            <i class="fas fa-arrow-left"></i> {{ yangilik.kategoriya.nom }} kategoriyasiga qaytish
        </a>
        <a href="{% url 'news:home' %}" 
           class="btn btn-outline-primary">
            Bosh sahifaga qaytish <i class="fas fa-home"></i>
        </a>
    </div>
</div>

<!-- Custom CSS -->
<style>
.article-content p {
    margin-bottom: 1.5rem;
}
.article-content h2, .article-content h3 {
    margin-top: 2rem;
    margin-bottom: 1rem;
}
</style>
{% endblock %}
```

### 5-bosqich: Views.py ni yangilash

Template teglarini to'liq ishlatish uchun `news/views.py` faylini yangilang:

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Yangilik, Kategoriya

class HomeView(ListView):
    """Bosh sahifa view"""
    model = Yangilik
    template_name = 'news/home.html'
    context_object_name = 'yangiliklar'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Asosiy yangiliklar (eng ko'p ko'rilgan)
        context['featured_news'] = Yangilik.objects.filter(
            nashr_etilgan=True
        ).order_by('-ko_rishlar_soni', '-yaratilgan_sana')[:4]
        
        # Kategoriyalar bo'yicha yangiliklar
        kategoriyalar = Kategoriya.objects.all()
        yangiliklar_by_category = {}
        
        for kategoriya in kategoriyalar:
            yangiliklar = Yangilik.objects.filter(
                kategoriya=kategoriya,
                nashr_etilgan=True
            ).order_by('-yaratilgan_sana')[:3]
            
            if yangiliklar.exists():
                yangiliklar_by_category[kategoriya] = yangiliklar
        
        context['yangiliklar_by_category'] = yangiliklar_by_category
        
        # Navigatsiya uchun kategoriyalar
        context['kategoriyalar'] = kategoriyalar
        
        return context

class YangiliklarDetailView(DetailView):
    """Yangilik batafsil ko'rish"""
    model = Yangilik
    template_name = 'news/detail.html'
    context_object_name = 'yangilik'
    
    def get_object(self):
        # Ko'rishlar sonini oshirish
        obj = super().get_object()
        obj.ko_rishlar_soni = obj.ko_rishlar_soni + 1
        obj.save(update_fields=['ko_rishlar_soni'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        yangilik = self.object
        
        # Tegdosh yangiliklar (bir xil kategoriyada)
        context['tegdosh_yangiliklar'] = Yangilik.objects.filter(
            kategoriya=yangilik.kategoriya,
            nashr_etilgan=True
        ).exclude(id=yangilik.id)[:3]
        
        # Navigatsiya uchun kategoriyalar
        context['kategoriyalar'] = Kategoriya.objects.all()
        
        return context

class KategoriyaView(ListView):
    """Kategoriya bo'yicha yangiliklar"""
    model = Yangilik
    template_name = 'news/category.html'
    context_object_name = 'yangiliklar'
    paginate_by = 9
    
    def get_queryset(self):
        self.kategoriya = get_object_or_404(Kategoriya, slug=self.kwargs['slug'])
        return Yangilik.objects.filter(
            kategoriya=self.kategoriya,
            nashr_etilgan=True
        ).order_by('-yaratilgan_sana')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategoriya'] = self.kategoriya
        context['kategoriyalar'] = Kategoriya.objects.all()
        return context

class AllNewsView(ListView):
    """Barcha yangiliklar"""
    model = Yangilik
    template_name = 'news/all_news.html'
    context_object_name = 'yangiliklar'
    paginate_by = 12
    
    def get_queryset(self):
        return Yangilik.objects.filter(
            nashr_etilgan=True
        ).order_by('-yaratilgan_sana')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategoriyalar'] = Kategoriya.objects.all()
        return context
```

### 6-bosqich: URLs.py ni yangilash

`news/urls.py` faylini to'ldiring:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('yangilik/<int:pk>/', views.YangiliklarDetailView.as_view(), name='detail'),
    path('kategoriya/<slug:slug>/', views.KategoriyaView.as_view(), name='category'),
    path('barcha-yangiliklar/', views.AllNewsView.as_view(), name='all_news'),
    path('aloqa/', views.ContactView.as_view(), name='contact'),
]
```

### 7-bosqich: Context processor yaratish

Barcha sahifalarda kategoriyalar ko'rinishi uchun context processor yarating.

`news/context_processors.py` faylini yarating:

```python
# news/context_processors.py
from .models import Kategoriya

def kategoriyalar_context(request):
    """Barcha sahifalarda kategoriyalarni ko'rsatish"""
    return {
        'kategoriyalar': Kategoriya.objects.all()
    }
```

`settings.py` da context processor qo'shing:

```python
# config/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news.context_processors.kategoriyalar_context',  # Qo'shildi
            ],
        },
    },
]
```

### 8-bosqich: CSS stillarini qo'shish

`static/css/style.css` faylini yarating:

```css
/* static/css/style.css */

/* Custom styles */
.hover-effect {
    transition: all 0.3s ease;
}

.hover-effect:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.article-content img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1rem 0;
}

.article-content p {
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
}

.article-content h2 {
    margin-top: 2.5rem;
    margin-bottom: 1.2rem;
    color: #2c3e50;
}

.card-hover {
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
}

.card-hover:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-color: #007bff;
}

/* Responsive typography */
@media (max-width: 768px) {
    .display-4 {
        font-size: 2rem;
    }
    
    .display-5 {
        font-size: 1.8rem;
    }
    
    .article-content p {
        font-size: 1rem;
    }
}

/* Custom badge colors */
.bg-sport { background-color: #28a745 !important; }
.bg-texnologiya { background-color: #007bff !important; }
.bg-siyosat { background-color: #dc3545 !important; }
.bg-iqtisod { background-color: #ffc107 !important; color: #000; }
.bg-madaniyat { background-color: #6f42c1 !important; }

/* Loading animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

### 9-bosqich: Barcha yangiliklar sahifasini yaratish

`templates/news/all_news.html` faylini yarating:

```html
<!-- templates/news/all_news.html -->
{% extends 'base.html' %}

{% block title %}Barcha yangiliklar - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="fw-bold">
            <i class="fas fa-newspaper"></i> Barcha yangiliklar
        </h1>
        <span class="badge bg-primary fs-6">
            {{ paginator.count }} ta yangilik
        </span>
    </div>
    
    <!-- Filter section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-0 bg-light">
                <div class="card-body">
                    <h6 class="card-title">Kategoriyalar:</h6>
                    <div class="d-flex flex-wrap gap-2">
                        <a href="{% url 'news:all_news' %}" 
                           class="btn btn-sm btn-outline-secondary">
                            Barchasi
                        </a>
                        {% for kat in kategoriyalar %}
                        <a href="{% url 'news:category' kat.slug %}" 
                           class="btn btn-sm btn-outline-primary">
                            {{ kat.nom }}
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- News grid -->
    <div class="row g-4">
        {% for yangilik in yangiliklar %}
        <div class="col-lg-4 col-md-6">
            <article class="card h-100 border-0 shadow-sm card-hover">
                {% if yangilik.rasm %}
                <div class="position-relative">
                    <img src="{{ yangilik.rasm.url }}" 
                         class="card-img-top" 
                         style="height: 250px; object-fit: cover;">
                    <div class="position-absolute top-0 start-0 m-3">
                        <span class="badge bg-primary">
                            {{ yangilik.kategoriya.nom }}
                        </span>
                    </div>
                    <div class="position-absolute top-0 end-0 m-3">
                        <span class="badge bg-dark bg-opacity-75">
                            <i class="fas fa-eye"></i> {{ yangilik.ko_rishlar_soni }}
                        </span>
                    </div>
                </div>
                {% endif %}
                
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">
                        <a href="{% url 'news:detail' yangilik.pk %}" 
                           class="text-decoration-none text-dark">
                            {{ yangilik.sarlavha }}
                        </a>
                    </h5>
                    
                    <p class="card-text flex-grow-1">
                        {{ yangilik.qisqa_mazmun|truncatewords:20 }}
                    </p>
                    
                    <div class="d-flex justify-content-between align-items-center mt-auto">
                        <small class="text-muted">
                            <i class="fas fa-calendar-alt"></i>
                            {{ yangilik.yaratilgan_sana|date:"d M, Y" }}
                        </small>
                        <a href="{% url 'news:detail' yangilik.pk %}" 
                           class="btn btn-primary btn-sm">
                            Batafsil
                        </a>
                    </div>
                </div>
            </article>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="text-center py-5">
                <i class="fas fa-newspaper fa-3x text-muted mb-3"></i>
                <h4 class="text-muted">Yangilik topilmadi</h4>
                <p class="text-muted">Hozircha bu bo'limda yangilik yo'q.</p>
                <a href="{% url 'news:home' %}" class="btn btn-primary">
                    Bosh sahifaga qaytish
                </a>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Pagination -->
    {% if is_paginated %}
    <nav class="mt-5">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1">
                        <i class="fas fa-angle-double-left"></i> Birinchi
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}">
                        <i class="fas fa-angle-left"></i> Oldingi
                    </a>
                </li>
            {% endif %}
            
            <li class="page-item active">
                <span class="page-link">
                    {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
                </span>
            </li>
            
            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}">
                        Keyingi <i class="fas fa-angle-right"></i>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">
                        Oxirgi <i class="fas fa-angle-double-right"></i>
                    </a>
                </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

### 10-bosqich: Custom template teglari yaratish (ixtiyoriy)

`news/templatetags/` papka yaratib, `__init__.py` va `news_tags.py` fayllarini qo'shing:

```python
# news/templatetags/__init__.py
# Bo'sh fayl

# news/templatetags/news_tags.py
from django import template
from django.utils.safestring import mark_safe
from ..models import Yangilik, Kategoriya
import random

register = template.Library()

@register.simple_tag
def popular_news(count=5):
    """Eng ommabop yangiliklar"""
    return Yangilik.objects.filter(
        nashr_etilgan=True
    ).order_by('-ko_rishlar_soni')[:count]

@register.simple_tag
def random_news(count=3):
    """Tasodifiy yangiliklar"""
    yangiliklar = list(Yangilik.objects.filter(nashr_etilgan=True))
    return random.sample(yangiliklar, min(count, len(yangiliklar)))

@register.filter
def reading_time(text):
    """O'qish vaqtini hisoblash"""
    words = len(text.split())
    minutes = max(1, words // 200)  # Daqiqada 200 so'z
    return f"{minutes} daqiqa"

@register.inclusion_tag('news/tags/category_stats.html')
def category_stats():
    """Kategoriyalar statistikasi"""
    stats = []
    for kat in Kategoriya.objects.all():
        count = Yangilik.objects.filter(
            kategoriya=kat, 
            nashr_etilgan=True
        ).count()
        stats.append({'kategoriya': kat, 'count': count})
    
    return {'stats': sorted(stats, key=lambda x: x['count'], reverse=True)}

@register.simple_tag
def get_recent_news(days=7, count=5):
    """So'nggi X kun yangiliklari"""
    from datetime import datetime, timedelta
    date_limit = datetime.now() - timedelta(days=days)
    
    return Yangilik.objects.filter(
        nashr_etilgan=True,
        yaratilgan_sana__gte=date_limit
    ).order_by('-yaratilgan_sana')[:count]
```

Template tag uchun qo'shimcha template yarating:

```html
<!-- templates/news/tags/category_stats.html -->
<div class="list-group">
    {% for item in stats %}
    <a href="{% url 'news:category' item.kategoriya.slug %}" 
       class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
        <span>{{ item.kategoriya.nom }}</span>
        <span class="badge bg-primary rounded-pill">{{ item.count }}</span>
    </a>
    {% endfor %}
</div>
```

### 11-bosqich: Components yaratish

Qayta ishlatiladigan karta komponenti yarating:

```html
<!-- templates/news/components/news_card.html -->
<article class="card h-100 border-0 shadow-sm card-hover">
    {% if yangilik.rasm %}
    <div class="position-relative">
        <img src="{{ yangilik.rasm.url }}" 
             class="card-img-top" 
             style="height: {{ image_height|default:'250px' }}; object-fit: cover;">
        <div class="position-absolute top-0 start-0 m-2">
            <span class="badge bg-{{ yangilik.kategoriya.rang|default:'primary' }}">
                {{ yangilik.kategoriya.nom }}
            </span>
        </div>
        {% if show_views %}
        <div class="position-absolute top-0 end-0 m-2">
            <span class="badge bg-dark bg-opacity-75">
                <i class="fas fa-eye"></i> {{ yangilik.ko_rishlar_soni }}
            </span>
        </div>
        {% endif %}
    </div>
    {% endif %}
    
    <div class="card-body d-flex flex-column">
        <h{{ title_size|default:'5' }} class="card-title">
            <a href="{% url 'news:detail' yangilik.pk %}" 
               class="text-decoration-none text-dark">
                {{ yangilik.sarlavha|truncatechars:title_length|default:yangilik.sarlavha }}
            </a>
        </h{{ title_size|default:'5' }}>
        
        {% if show_summary %}
        <p class="card-text flex-grow-1">
            {{ yangilik.qisqa_mazmun|truncatewords:summary_length|default:20 }}
        </p>
        {% endif %}
        
        <div class="d-flex justify-content-between align-items-center mt-auto">
            <small class="text-muted">
                <i class="fas fa-calendar-alt"></i>
                {{ yangilik.yaratilgan_sana|date:"d M, Y" }}
            </small>
            <a href="{% url 'news:detail' yangilik.pk %}" 
               class="btn btn-{{ button_style|default:'primary' }} btn-sm">
                {{ button_text|default:'Batafsil' }}
            </a>
        </div>
    </div>
</article>
```

Komponentni ishlatish:

```html
<!-- Home.html da ishlatish -->
{% for yangilik in featured_news %}
<div class="col-lg-6">
    {% include 'news/components/news_card.html' with yangilik=yangilik show_views=True show_summary=True %}
</div>
{% endfor %}
```

### 12-bosqich: Sidebar komponenti yaratish

`templates/news/components/sidebar.html` yarating:

```html
<!-- templates/news/components/sidebar.html -->
<aside class="col-lg-3">
    <!-- Popular News -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">
                <i class="fas fa-fire text-danger"></i> Ommabop yangiliklar
            </h6>
        </div>
        <div class="card-body p-0">
            {% load news_tags %}
            {% popular_news 5 as pop_news %}
            
            {% for yangilik in pop_news %}
            <div class="d-flex p-3 {% if not forloop.last %}border-bottom{% endif %}">
                {% if yangilik.rasm %}
                <img src="{{ yangilik.rasm.url }}" 
                     class="me-3 rounded" 
                     style="width: 60px; height: 60px; object-fit: cover;">
                {% endif %}
                <div class="flex-grow-1">
                    <h6 class="mb-1">
                        <a href="{% url 'news:detail' yangilik.pk %}" 
                           class="text-decoration-none text-dark small">
                            {{ yangilik.sarlavha|truncatechars:50 }}
                        </a>
                    </h6>
                    <small class="text-muted">
                        <i class="fas fa-eye"></i> {{ yangilik.ko_rishlar_soni }}
                        · {{ yangilik.yaratilgan_sana|date:"d M" }}
                    </small>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Categories Stats -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">
                <i class="fas fa-chart-pie"></i> Kategoriyalar statistikasi
            </h6>
        </div>
        <div class="card-body p-0">
            {% category_stats %}
        </div>
    </div>

    <!-- Recent News -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">
                <i class="fas fa-clock"></i> So'nggi yangiliklar
            </h6>
        </div>
        <div class="card-body p-0">
            {% get_recent_news 3 5 as recent_news %}
            
            {% for yangilik in recent_news %}
            <div class="p-3 {% if not forloop.last %}border-bottom{% endif %}">
                <h6 class="mb-1">
                    <a href="{% url 'news:detail' yangilik.pk %}" 
                       class="text-decoration-none text-dark small">
                        {{ yangilik.sarlavha|truncatechars:60 }}
                    </a>
                </h6>
                <small class="text-muted">
                    {{ yangilik.yaratilgan_sana|timesince }} oldin
                </small>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Newsletter Signup -->
    <div class="card">
        <div class="card-body text-center">
            <h6><i class="fas fa-envelope"></i> Obuna bo'ling</h6>
            <p class="small text-muted">
                Eng so'nggi yangiliklar haqida xabardor bo'ling
            </p>
            <div class="input-group">
                <input type="email" class="form-control form-control-sm" 
                       placeholder="Email manzilingiz">
                <button class="btn btn-primary btn-sm">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
</aside>
```

### 13-bosqich: Sidebar bilan sahifalarni yangilash

Home sahifasini 2-ustunli layout qilib yangilang:

```html
<!-- templates/news/home.html - Updated with sidebar -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-4">
    <!-- Hero Banner -->
    <div class="jumbotron bg-gradient text-white p-5 rounded-3 mb-5" 
         style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <!-- Hero content... -->
    </div>

    <div class="row">
        <!-- Main content -->
        <div class="col-lg-9">
            <!-- Featured News section -->
            {% if featured_news %}
            <section class="mb-5">
                <!-- Content... -->
            </section>
            {% endif %}

            <!-- Categories section -->
            <section>
                <!-- Content... -->
            </section>
        </div>

        <!-- Sidebar -->
        {% include 'news/components/sidebar.html' %}
    </div>
</div>
{% endblock %}
```

### 14-bosqich: Admin panel yaxshilash

Admin panel uchun custom display qo'shing:

```python
# news/admin.py - Enhanced version
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Yangilik, Kategoriya, Teg

@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'yangiliklar_soni', 'rang_display')
    list_filter = ('rang',)
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}
    
    def yangiliklar_soni(self, obj):
        count = obj.yangilik_set.filter(nashr_etilgan=True).count()
        url = reverse('admin:news_yangilik_changelist')
        return format_html(
            '<a href="{}?kategoriya__id__exact={}">{} ta</a>',
            url, obj.id, count
        )
    yangiliklar_soni.short_description = 'Yangiliklar soni'
    
    def rang_display(self, obj):
        return format_html(
            '<span class="badge" style="background-color: {}; color: white;">{}</span>',
            obj.get_rang_display() if obj.rang else '#6c757d',
            obj.rang or 'Default'
        )
    rang_display.short_description = 'Rang'

@admin.register(Yangilik)
class YangiliklarAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'kategoriya', 'muallif', 'nashr_etilgan', 
                   'ko_rishlar_soni', 'yaratilgan_sana')
    list_filter = ('nashr_etilgan', 'kategoriya', 'yaratilgan_sana')
    search_fields = ('sarlavha', 'qisqa_mazmun', 'matn')
    list_editable = ('nashr_etilgan',)
    date_hierarchy = 'yaratilgan_sana'
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('sarlavha', 'qisqa_mazmun', 'kategoriya')
        }),
        ('Kontent', {
            'fields': ('matn', 'rasm')
        }),
        ('Meta ma\'lumotlar', {
            'fields': ('muallif', 'teglar', 'nashr_etilgan')
        }),
        ('Statistika', {
            'fields': ('ko_rishlar_soni',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt
            obj.muallif = request.user
        super().save_model(request, obj, form, change)

@admin.register(Teg)
class TegAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'yangiliklar_soni')
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}
    
    def yangiliklar_soni(self, obj):
        return obj.yangilik_set.count()
    yangiliklar_soni.short_description = 'Yangiliklar soni'
```

## Xulosa va keyingi qadamlar

Bu amaliyotda siz quyidagilarni o'rgandingiz:

✅ **Template inheritance** - Base template yaratish va kengaytirish
✅ **Template tags** - `{% for %}`, `{% if %}`, `{% url %}`, `{% static %}`
✅ **Template filters** - `|date`, `|truncatewords`, `|length`
✅ **Context processors** - Global ma'lumotlar
✅ **Custom template tags** - O'z teglaringizni yaratish
✅ **Components** - Qayta ishlatiladigan elementlar
✅ **Responsive design** - Bootstrap bilan adaptive layout

### Keyingi bosqichlar:

1. **Search funksiyasi** qo'shish
2. **Comments tizimi** yaratish
3. **Ajax** bilan dinamik yuklash
4. **REST API** yaratish
5. **Caching** mexanizmi qo'shish
6. **SEO** optimizatsiyasi

**Eslatma:** Barcha kodlarni test qiling va o'z ehtiyojlaringizga moslang!