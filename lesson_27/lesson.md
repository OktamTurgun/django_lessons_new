# Dars 27: Yangiliklar sayti sahifalarini yaratish

## Dars maqsadi
Ushbu darsda biz yangiliklar sayti uchun turli xil sahifalar yaratamiz. Har bir yangilik xabari uchun alohida view'lar, template'lar va URL'larni sozlaymiz. Loyihaning barcha kerakli sahifalarini to'liq funksional holatga keltiramiz.

## Nazariy qism

### View turlari
Django'da sahifalar yaratish uchun turli xil view'lardan foydalanishimiz mumkin:
- **Function-based views (FBV)** - oddiy funksiyalar
- **Class-based views (CBV)** - klassga asoslangan view'lar
- **Generic views** - tayyor view'lar (ListView, DetailView, va boshqalar)

### URL routing
Har bir view uchun URL yo'lini belgilashimiz kerak. Bu `urls.py` fayllarida amalga oshiriladi.

## Amaliy qism

### 1-bosqich: URLs.py fayllarini yaratish

Avval loyiha asosiy `urls.py` faylini yangilaymiz:

**mysite/urls.py:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls', namespace='news')),
]

# Media fayllar uchun (development rejimida)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Endi `news` ilovasi uchun URL'lar yaratamiz:

**news/urls.py:**
```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Bosh sahifa
    path('', views.HomePageView.as_view(), name='home'),
    
    # Yangiliklar ro'yxati
    path('news/', views.NewsListView.as_view(), name='news_list'),
    
    # Yangilik batafsil
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Kategoriya bo'yicha yangiliklar
    path('category/<slug:category_slug>/', views.CategoryNewsView.as_view(), name='category_news'),
    
    # Qidiruv
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Kontakt sahifasi
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # About sahifasi
    path('about/', views.AboutView.as_view(), name='about'),
]
```

### 2-bosqich: View'larni yaratish

**news/views.py:**
```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import News, Category
from .forms import ContactForm

class HomePageView(TemplateView):
    """Bosh sahifa view'i"""
    template_name = 'news/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategoriyalar bo'yicha yangiliklar
        categories = Category.objects.all()
        news_by_category = {}
        
        for category in categories[:4]:  # Faqat 4 ta kategoriya
            news_list = News.published.filter(category=category)[:3]  # Har kategoriyadan 3 ta
            if news_list:
                news_by_category[category] = news_list
        
        # So'nggi yangiliklar
        latest_news = News.published.order_by('-publish_time')[:5]
        
        # Mashhur yangiliklar (ko'p ko'rilgan)
        popular_news = News.published.order_by('-views')[:5]
        
        context.update({
            'news_by_category': news_by_category,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'categories': categories,
        })
        
        return context

class NewsListView(ListView):
    """Barcha yangiliklar sahifasi"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 6  # Har sahifada 6 ta yangilik
    
    def get_queryset(self):
        queryset = News.published.select_related('category', 'author')
        
        # Kategoriya bo'yicha filtrlash
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        
        # Saralash
        sort_by = self.request.GET.get('sort', '-publish_time')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class NewsDetailView(DetailView):
    """Yangilik batafsil sahifasi"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.published.select_related('category', 'author')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Ko'rishlar sonini oshirish
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object
        
        # O'xshash yangiliklar (bir xil kategoriyadan)
        related_news = News.published.filter(
            category=news.category
        ).exclude(id=news.id)[:4]
        
        context['related_news'] = related_news
        return context

class CategoryNewsView(ListView):
    """Kategoriya bo'yicha yangiliklar"""
    model = News
    template_name = 'news/category_news.html'
    context_object_name = 'news_list'
    paginate_by = 8
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return News.published.filter(category=self.category).select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['news_count'] = self.get_queryset().count()
        return context

class SearchView(ListView):
    """Qidiruv sahifasi"""
    model = News
    template_name = 'news/search.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return News.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).select_related('category', 'author')
        return News.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_results'] = self.get_queryset().count()
        return context

class ContactView(FormView):
    """Kontakt sahifasi"""
    template_name = 'news/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        # Formani saqlash yoki email yuborish
        form.save()
        messages.success(self.request, 'Xabaringiz muvaffaqiyatli yuborildi!')
        return super().form_valid(form)

class AboutView(TemplateView):
    """Biz haqimizda sahifasi"""
    template_name = 'news/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Statistika ma'lumotlari
        context['total_news'] = News.published.count()
        context['total_categories'] = Category.objects.count()
        return context
```

### 3-bosqich: Forms yaratish

**news/forms.py:**
```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """Kontakt formasi"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzilingizni kiriting'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xabar mavzusi'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Xabaringizni yozing'
            }),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Ism kamida 2 ta belgidan iborat bo\'lishi kerak.')
        return name
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgidan iborat bo\'lishi kerak.')
        return message

class SearchForm(forms.Form):
    """Qidiruv formasi"""
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qidirish...',
            'required': True,
        })
    )
```

### 4-bosqich: Template'lar yaratish

#### Base template

**templates/base.html:**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar Sayti{% endblock %}</title>
    {% load static %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:home' %}">Bosh sahifa</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:news_list' %}">Yangiliklar</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:about' %}">Biz haqimizda</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:contact' %}">Aloqa</a>
                    </li>
                </ul>
                <form class="d-flex" method="get" action="{% url 'news:search' %}">
                    <input class="form-control me-2" type="search" name="q" 
                           placeholder="Qidirish..." value="{{ request.GET.q }}">
                    <button class="btn btn-outline-light" type="submit">Qidirish</button>
                </form>
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

    <!-- Main Content -->
    <main class="py-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Yangiliklar Sayti</h5>
                    <p>Eng so'nggi va dolzarb yangiliklar bilan tanishing.</p>
                </div>
                <div class="col-md-6">
                    <h5>Kategoriyalar</h5>
                    <ul class="list-unstyled">
                        {% for category in categories %}
                        <li><a href="{% url 'news:category_news' category.slug %}" class="text-light">{{ category.name }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            <hr>
            <div class="text-center">
                <p>&copy; 2024 Yangiliklar Sayti. Barcha huquqlar himoyalangan.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### Home sahifa template'i

**templates/news/home.html:**
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa - Yangiliklar{% endblock %}

{% block content %}
<div class="container">
    <!-- Hero section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="bg-primary text-white p-5 rounded">
                <h1 class="display-4">So'nggi yangiliklar</h1>
                <p class="lead">Eng muhim va dolzarb yangiliklar bilan tanishing</p>
            </div>
        </div>
    </div>

    <!-- Kategoriyalar bo'yicha yangiliklar -->
    {% for category, news_list in news_by_category.items %}
    <section class="mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>{{ category.name }}</h2>
            <a href="{% url 'news:category_news' category.slug %}" class="btn btn-outline-primary">
                Barchasini ko'rish
            </a>
        </div>
        
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if news.photo %}
                    <img src="{{ news.photo.url }}" class="card-img-top" alt="{{ news.title }}" style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <div class="mb-2">
                            <small class="text-muted">{{ news.publish_time|date:"d M Y" }}</small>
                        </div>
                        <h5 class="card-title">
                            <a href="{% url 'news:news_detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatechars:60 }}
                            </a>
                        </h5>
                        <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">{{ news.author.get_full_name|default:news.author.username }}</small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% empty %}
    <div class="text-center">
        <h2>Hozircha yangiliklar mavjud emas</h2>
        <p>Tez orada yangi materiallar qo'shiladi.</p>
    </div>
    {% endfor %}

    <!-- Sidebar -->
    <div class="row mt-5">
        <div class="col-md-8">
            <h3>So'nggi yangiliklar</h3>
            <div class="row">
                {% for news in latest_news %}
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">
                                <a href="{% url 'news:news_detail' news.slug %}">{{ news.title|truncatechars:50 }}</a>
                            </h6>
                            <small class="text-muted">{{ news.publish_time|timesince }} oldin</small>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="col-md-4">
            <h3>Mashhur kategoriyalar</h3>
            <div class="list-group">
                {% for category in categories %}
                <a href="{% url 'news:category_news' category.slug %}" class="list-group-item list-group-item-action">
                    {{ category.name }}
                </a>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Yangilik detail sahifa template'i

**templates/news/news_detail.html:**
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'news:home' %}">Bosh sahifa</a></li>
            <li class="breadcrumb-item"><a href="{% url 'news:news_list' %}">Yangiliklar</a></li>
            <li class="breadcrumb-item"><a href="{% url 'news:category_news' news.category.slug %}">{{ news.category.name }}</a></li>
            <li class="breadcrumb-item active">{{ news.title|truncatechars:30 }}</li>
        </ol>
    </nav>

    <div class="row">
        <div class="col-lg-8">
            <!-- Yangilik asosiy qismi -->
            <article class="mb-4">
                <header class="mb-4">
                    <div class="mb-2">
                        <span class="badge bg-primary">{{ news.category.name }}</span>
                        <small class="text-muted ms-2">{{ news.publish_time|date:"d F Y, H:i" }}</small>
                    </div>
                    <h1>{{ news.title }}</h1>
                    <div class="text-muted">
                        <span>Muallif: {{ news.author.get_full_name|default:news.author.username }}</span>
                        {% if news.views %}
                        <span class="ms-3">Ko'rishlar: {{ news.views }}</span>
                        {% endif %}
                    </div>
                </header>

                {% if news.photo %}
                <div class="mb-4">
                    <img src="{{ news.photo.url }}" class="img-fluid rounded" alt="{{ news.title }}">
                </div>
                {% endif %}

                <div class="content">
                    {{ news.body|linebreaks }}
                </div>
            </article>
        </div>

        <div class="col-lg-4">
            <!-- O'xshash yangiliklar -->
            {% if related_news %}
            <div class="card">
                <div class="card-header">
                    <h5>O'xshash yangiliklar</h5>
                </div>
                <div class="card-body">
                    {% for related in related_news %}
                    <div class="mb-3">
                        <h6>
                            <a href="{% url 'news:news_detail' related.slug %}">
                                {{ related.title|truncatechars:60 }}
                            </a>
                        </h6>
                        <small class="text-muted">{{ related.publish_time|date:"d M Y" }}</small>
                    </div>
                    {% if not forloop.last %}<hr>{% endif %}
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

#### Yangiliklar ro'yxati template'i

**templates/news/news_list.html:**
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Barcha yangiliklar{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Barcha yangiliklar</h1>
                
                <!-- Filtrlash -->
                <form method="get" class="d-flex">
                    <select name="category" class="form-select me-2" onchange="this.form.submit()">
                        <option value="">Barcha kategoriyalar</option>
                        {% for category in categories %}
                        <option value="{{ category.id }}" 
                            {% if request.GET.category == category.id|stringformat:"s" %}selected{% endif %}>
                            {{ category.name }}
                        </option>
                        {% endfor %}
                    </select>
                    
                    <select name="sort" class="form-select" onchange="this.form.submit()">
                        <option value="-publish_time" 
                            {% if request.GET.sort == "-publish_time" or not request.GET.sort %}selected{% endif %}>
                            So'nggi
                        </option>
                        <option value="title" 
                            {% if request.GET.sort == "title" %}selected{% endif %}>
                            Nomi bo'yicha
                        </option>
                        <option value="-views" 
                            {% if request.GET.sort == "-views" %}selected{% endif %}>
                            Ko'p ko'rilgan
                        </option>
                    </select>
                </form>
            </div>

            <!-- Yangiliklar -->
            {% for news in news_list %}
            <div class="card mb-4">
                <div class="row g-0">
                    {% if news.photo %}
                    <div class="col-md-4">
                        <img src="{{ news.photo.url }}" class="img-fluid rounded-start h-100" style="object-fit: cover;" alt="{{ news.title }}">
                    </div>
                    <div class="col-md-8">
                    {% else %}
                    <div class="col-12">
                    {% endif %}
                        <div class="card-body">
                            <div class="mb-2">
                                <span class="badge bg-primary">{{ news.category.name }}</span>
                                <small class="text-muted ms-2">{{ news.publish_time|date:"d M Y, H:i" }}</small>
                            </div>
                            <h5 class="card-title">
                                <a href="{% url 'news:news_detail' news.slug %}" class="text-decoration-none">
                                    {{ news.title }}
                                </a>
                            </h5>
                            <p class="card-text">{{ news.body|truncatewords:25 }}</p>
                            <div class="d-flex justify-content-between">
                                <small class="text-muted">{{ news.author.get_full_name|default:news.author.username }}</small>
                                {% if news.views %}
                                <small class="text-muted">{{ news.views }} ko'rish</small>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="text-center">
                <h3>Hech qanday yangilik topilmadi</h3>
                <p>Boshqa filtrlardan foydalanib ko'ring.</p>
            </div>
            {% endfor %}

            <!-- Pagination -->
            {% if is_paginated %}
            <nav>
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1{% if request.GET.category %}&category={{ request.GET.category }}{% endif %}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}">Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if request.GET.category %}&category={{ request.GET.category }}{% endif %}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}">Oldingi</a>
                    </li>
                    {% endif %}

                    <li class="page-item active">
                        <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
                    </li>

                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if request.GET.category %}&category={{ request.GET.category }}{% endif %}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}">Keyingi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if request.GET.category %}&category={{ request.GET.category }}{% endif %}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}">Oxirgi</a>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>

        <!-- Sidebar -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Kategoriyalar</h5>
                </div>
                <div class="list-group list-group-flush">
                    {% for category in categories %}
                    <a href="{% url 'news:category_news' category.slug %}" class="list-group-item list-group-item-action">
                        {{ category.name }}
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5-bosqich: Qolgan template'larni yaratish

**templates/news/category_news.html:**
```html
{% extends 'base.html' %}

{% block title %}{{ category.name }} - Yangiliklar{% endblock %}

{% block content %}
<div class="container">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'news:home' %}">Bosh sahifa</a></li>
            <li class="breadcrumb-item"><a href="{% url 'news:news_list' %}">Yangiliklar</a></li>
            <li class="breadcrumb-item active">{{ category.name }}</li>
        </ol>
    </nav>

    <div class="mb-4">
        <h1>{{ category.name }}</h1>
        <p class="text-muted">Jami: {{ news_count }} yangilik</p>
    </div>

    <div class="row">
        {% for news in news_list %}
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" class="card-img-top" style="height: 200px; object-fit: cover;">
                {% endif %}
                <div class="card-body d-flex flex-column">
                    <div class="mb-2">
                        <small class="text-muted">{{ news.publish_time|date:"d M Y" }}</small>
                        {% if news.views %}
                        <small class="text-muted ms-2">{{ news.views }} ko'rish</small>
                        {% endif %}
                    </div>
                    <h5 class="card-title">
                        <a href="{% url 'news:news_detail' news.slug %}">{{ news.title }}</a>
                    </h5>
                    <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                    <div class="mt-auto">
                        <small class="text-muted">{{ news.author.get_full_name|default:news.author.username }}</small>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center">
            <h3>{{ category.name }} kategoriyasida yangiliklar mavjud emas</h3>
            <p><a href="{% url 'news:news_list' %}">Barcha yangiliklarni ko'rish</a></p>
        </div>
        {% endfor %}
    </div>

    <!-- Pagination -->
    {% if is_paginated %}
    <nav>
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Oldingi</a>
            </li>
            {% endif %}

            {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
            <li class="page-item active">
                <span class="page-link">{{ num }}</span>
            </li>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
            <li class="page-item">
                <a class="page-link" href="?page={{ num }}">{{ num }}</a>
            </li>
            {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

**templates/news/search.html:**
```html
{% extends 'base.html' %}

{% block title %}Qidiruv natijalari{% endblock %}

{% block content %}
<div class="container">
    <div class="mb-4">
        <h1>Qidiruv natijalari</h1>
        {% if query %}
        <p class="text-muted">"{{ query }}" uchun {{ total_results }} ta natija topildi</p>
        {% endif %}
    </div>

    <!-- Qidiruv formasi -->
    <form method="get" class="mb-4">
        <div class="input-group">
            <input type="text" name="q" class="form-control" placeholder="Qidirish..." value="{{ query }}">
            <button class="btn btn-primary" type="submit">Qidirish</button>
        </div>
    </form>

    <!-- Natijalar -->
    {% if query %}
    <div class="row">
        {% for news in news_list %}
        <div class="col-12 mb-4">
            <div class="card">
                <div class="row g-0">
                    {% if news.photo %}
                    <div class="col-md-3">
                        <img src="{{ news.photo.url }}" class="img-fluid rounded-start h-100" style="object-fit: cover;">
                    </div>
                    <div class="col-md-9">
                    {% else %}
                    <div class="col-12">
                    {% endif %}
                        <div class="card-body">
                            <div class="mb-2">
                                <span class="badge bg-primary">{{ news.category.name }}</span>
                                <small class="text-muted ms-2">{{ news.publish_time|date:"d M Y" }}</small>
                            </div>
                            <h5 class="card-title">
                                <a href="{% url 'news:news_detail' news.slug %}">{{ news.title }}</a>
                            </h5>
                            <p class="card-text">{{ news.body|truncatewords:30 }}</p>
                            <small class="text-muted">{{ news.author.get_full_name|default:news.author.username }}</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center">
            <h3>Hech narsa topilmadi</h3>
            <p>Boshqa kalit so'zlar bilan qidirish uchun harakat qiling.</p>
        </div>
        {% endfor %}
    </div>

    <!-- Pagination -->
    {% if is_paginated %}
    <nav>
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Oldingi</a>
            </li>
            {% endif %}

            <li class="page-item active">
                <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
            </li>

            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Keyingi</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
    {% endif %}
</div>
{% endblock %}
```

**templates/news/contact.html:**
```html
{% extends 'base.html' %}

{% block title %}Aloqa{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8 mx-auto">
            <h1 class="mb-4">Biz bilan bog'laning</h1>
            
            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="{{ form.name.id_for_label }}" class="form-label">Ism</label>
                            {{ form.name }}
                            {% if form.name.errors %}
                            <div class="text-danger">
                                {% for error in form.name.errors %}
                                <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.email.id_for_label }}" class="form-label">Email</label>
                            {{ form.email }}
                            {% if form.email.errors %}
                            <div class="text-danger">
                                {% for error in form.email.errors %}
                                <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.subject.id_for_label }}" class="form-label">Mavzu</label>
                            {{ form.subject }}
                            {% if form.subject.errors %}
                            <div class="text-danger">
                                {% for error in form.subject.errors %}
                                <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.message.id_for_label }}" class="form-label">Xabar</label>
                            {{ form.message }}
                            {% if form.message.errors %}
                            <div class="text-danger">
                                {% for error in form.message.errors %}
                                <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>

                        <button type="submit" class="btn btn-primary">Yuborish</button>
                    </form>
                </div>
            </div>

            <!-- Kontakt ma'lumotlari -->
            <div class="row mt-5">
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5>Telefon</h5>
                            <p>+998 90 123 45 67</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5>Email</h5>
                            <p>info@yangiliklar.uz</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5>Manzil</h5>
                            <p>Toshkent, O'zbekiston</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**templates/news/about.html:**
```html
{% extends 'base.html' %}

{% block title %}Biz haqimizda{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <h1 class="mb-4">Biz haqimizda</h1>
            
            <div class="card mb-4">
                <div class="card-body">
                    <p class="lead">Bizning yangiliklar saytimiz eng so'nggi va ishonchli ma'lumotlarni taqdim etishga bag'ishlangan.</p>
                    
                    <p>2024-yilda tashkil etilgan saytimiz turli sohalardagi yangiliklar, tahlillar va maqolalarni o'quvchilarga yetkazish maqsadida faoliyat yuritadi. Bizning maqsadimiz - jamiyatni eng muhim voqealar haqida xabardor qilish va sifatli axborot manbai bo'lishdir.</p>
                    
                    <h3>Bizning qiymatlarimiz:</h3>
                    <ul>
                        <li><strong>Ishonchlilik:</strong> Barcha ma'lumotlarni tekshirish va tasdiqlash</li>
                        <li><strong>Tezlik:</strong> Muhim yangiliklarni tez yetkazish</li>
                        <li><strong>Objektiv:</strong> Barcha tomonlarni hisobga olish</li>
                        <li><strong>Sifat:</strong> Yuqori sifatli kontent yaratish</li>
                    </ul>
                    
                    <h3>Bizning jamoamiz:</h3>
                    <p>Tajribali jurnalistlar, muharrirlar va dasturchilardan iborat jamoamiz har kuni yangi va qiziqarli materiallar yaratish uchun mehnat qilmoqda.</p>
                </div>
            </div>

            <!-- Statistika -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2 class="text-primary">{{ total_news }}</h2>
                            <p>Jami yangiliklar</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2 class="text-success">{{ total_categories }}</h2>
                            <p>Kategoriyalar soni</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6-bosqich: Models.py ga qo'shimcha model qo'shish

**news/models.py ga Contact modeli qo'shamiz:**
```python
class Contact(models.Model):
    """Kontakt formasi modeli"""
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Kontakt xabari"
        verbose_name_plural = "Kontakt xabarlari"
        ordering = ['-created_time']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
```

### 7-bosqich: Admin.py ga Contact modelini qo'shish

**news/admin.py:**
```python
from django.contrib import admin
from .models import Category, News, Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_time']
    list_filter = ['created_time']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_time']
    
    def has_add_permission(self, request):
        return False  # Admin paneldan qo'shishni cheklash
```

### 8-bosqich: Static fayllar (CSS) yaratish

**static/css/style.css:**
```css
/* Asosiy stillar */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navbar stillar */
.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

/* Card stillar */
.card {
    transition: transform 0.2s;
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Image stillar */
.card-img-top {
    transition: transform 0.3s;
}

.card:hover .card-img-top {
    transform: scale(1.05);
}

/* Link stillar */
a {
    text-decoration: none !important;
    color: inherit;
}

a:hover {
    color: #0d6efd;
}

/* Breadcrumb stillar */
.breadcrumb {
    background: transparent;
    padding: 0;
}

/* Footer stillar */
footer {
    margin-top: auto;
}

/* Badge stillar */
.badge {
    font-size: 0.8em;
}

/* Pagination stillar */
.pagination .page-link {
    color: #0d6efd;
    border-color: #dee2e6;
}

.pagination .page-item.active .page-link {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

/* Alert stillar */
.alert {
    border: none;
    border-radius: 8px;
}

/* Form stillar */
.form-control:focus {
    border-color: #86b7fe;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Search form */
.input-group .form-control:focus {
    z-index: 3;
}

/* Responsive stillar */
@media (max-width: 768px) {
    .card-title {
        font-size: 1.1rem;
    }
    
    .display-4 {
        font-size: 2rem;
    }
}

/* Loading animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

### 9-bosqich: Migration yaratish va qo'llash

```bash
# Contact modelini yaratish uchun migration
python manage.py makemigrations

# Migration ni qo'llash
python manage.py migrate

# Superuser yaratish (agar hali yaratilmagan bo'lsa)
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

### 10-bosqich: Test ma'lumotlar qo'shish

Admin panelga kirib, test uchun bir nechta kategoriya va yangilik qo'shishingiz mumkin.

## Xulosa

Ushbu darsda biz:

1. **URL routing** tizimini yaratdik
2. **Turli xil view'lar** ishlatdik (CBV va FBV)
3. **Template'lar** yaratdik va ularni bir-biriga bog'ladik
4. **Forms** bilan ishladik
5. **Static fayllar** qo'shdik
6. **Responsive design** qo'lladik
7. **Pagination** ni amalga oshirdik
8. **Search funksiyasi** yaratdik
9. **Contact forma** qo'shdik

### Muhim tushunchalar:
- **URL patterns** - sahifalar uchun yo'llar
- **View classes** - sahifa mantiqini boshqarish
- **Template inheritance** - kodni takrorlamaslik
- **Context data** - template'larga ma'lumot uzatish
- **Pagination** - sahifalashni amalga oshirish
- **Form validation** - formalarni tekshirish
- **Static files** - CSS, JS, rasm fayllar bilan ishlash

### Keyingi qadamlar:
1. **Ajax** bilan dinamik yuklash qo'shish
2. **Caching** tizimini joriy etish
3. **SEO optimizatsiya** (meta taglar, sitemap)
4. **User authentication** (ro'yxatdan o'tish, kirish)
5. **Comment tizimi** qo'shish
6. **Social media** integratsiyasi
7. **Email newsletter** funksiyasi
8. **API** yaratish (Django REST framework bilan)

### Texnik tavsiyalar:
- Kodni muntazam ravishda backup qiling
- Git versiya nazorati ishlatting
- Virtual environment ishlatishni unutmang
- Production uchun DEBUG = False qiling
- ALLOWED_HOSTS ni to'g'ri sozlang

Bu dars bilan bizning yangiliklar saytimiz to'liq funksional holatga keldi va foydalanuvchilar barcha sahifalardan foydalanishlari mumkin. Sayt responsive bo'lib, mobil qurilmalarda ham yaxshi ishlaydi.