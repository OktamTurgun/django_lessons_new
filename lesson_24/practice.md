# Amaliyot 24: Context_processor va get_context_data

## Amaliyotning maqsadi
Ushbu amaliyotda biz Django loyihamizga Context Processor va get_context_data metodlarini qo'shib, barcha sahifalarda umumiy ma'lumotlarni ko'rsatishni amalga oshiramiz.

## Boshlash oldidan
Loyihangiz ishga tushganligiga ishonch hosil qiling:
- Django server ishlayapti (`python manage.py runserver`)
- Ma'lumotlar bazasida News va Category modellari mavjud
- Bir nechta yangiliklar yaratilgan

## 1-qadam: Context Processor faylini yaratish

`news` ilovasida `context_processors.py` faylini yarating:

```bash
cd news/
touch context_processors.py
```

Faylga quyidagi kodni yozing:

```python
# news/context_processors.py
from django.db.models import Count
from .models import News, Category

def site_data(request):
    """
    Sayt uchun umumiy ma'lumotlar
    """
    return {
        'site_name': 'News Portal',
        'site_description': 'Eng so\'nggi yangiliklar va maqolalar',
        'site_author': 'News Team',
        'contact_email': 'info@newsportal.uz',
    }

def sidebar_data(request):
    """
    Sidebar uchun ma'lumotlar
    """
    try:
        # Eng oxirgi 5ta yangilik
        latest_news = News.published.all()[:5]
        
        # Kategoriyalar va ularning yangiliklar soni
        categories = Category.objects.annotate(
            news_count=Count('news', filter=models.Q(news__status='published'))
        ).filter(news_count__gt=0)
        
        return {
            'latest_news': latest_news,
            'sidebar_categories': categories,
        }
    except Exception as e:
        # Xato bo'lsa bo'sh natija qaytaring
        return {
            'latest_news': [],
            'sidebar_categories': [],
        }

def stats_data(request):
    """
    Sayt statistikasi
    """
    try:
        total_news = News.published.count()
        total_categories = Category.objects.count()
        
        return {
            'total_news_count': total_news,
            'total_categories_count': total_categories,
        }
    except Exception:
        return {
            'total_news_count': 0,
            'total_categories_count': 0,
        }
```

## 2-qadam: Settings.py'da Context Processor'ni ro'yxatga olish

`config/settings.py` faylini oching va TEMPLATES bo'limini yangilang:

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
                
                # O'zimizning context processor'larimiz
                'news.context_processors.site_data',
                'news.context_processors.sidebar_data',
                'news.context_processors.stats_data',
            ],
        },
    },
]
```

## 3-qadam: View'larda get_context_data metodini ishlatish

`news/views.py` faylini yangilang:

```python
# news/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import News, Category

# Function-based view misoli
def home_view(request):
    """
    Bosh sahifa - function based view
    """
    featured_news = News.published.filter(featured=True)[:6]
    recent_news = News.published.all()[:8]
    
    context = {
        'featured_news': featured_news,
        'recent_news': recent_news,
        'page_title': 'Bosh sahifa',
        'page_description': 'Eng yangi va muhim yangiliklar',
    }
    return render(request, 'news/home.html', context)

# Class-based view'lar
class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return News.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Barcha yangiliklar'
        context['page_description'] = 'Saytimizda nashr qilingan barcha yangiliklar'
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        
        # O'xshash yangiliklar
        related_news = News.published.filter(
            category=news.category
        ).exclude(id=news.id)[:4]
        
        context.update({
            'related_news': related_news,
            'page_title': news.title,
            'page_description': news.body[:150] + '...',
        })
        return context

class CategoryDetailView(ListView):
    template_name = 'news/category_detail.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return News.published.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'page_title': f'{self.category.name} kategoriyasi',
            'page_description': f'{self.category.name} bo\'yicha yangiliklar',
            'news_count': self.get_queryset().count(),
        })
        return context
```

## 4-qadam: Base template yaratish

`templates/base.html` faylini yarating yoki yangilang:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title|default:site_name }}{% endblock %}</title>
    <meta name="description" content="{% block description %}{{ page_description|default:site_description }}{% endblock %}">
    <meta name="author" content="{{ site_author }}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header -->
    <header class="bg-primary text-white">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand fw-bold" href="{% url 'news:home' %}">
                    {{ site_name }}
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
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:news-list' %}">Barcha yangiliklar</a>
                        </li>
                        <!-- Kategoriyalar dropdown -->
                        {% if sidebar_categories %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" 
                               role="button" data-bs-toggle="dropdown">
                                Kategoriyalar
                            </a>
                            <ul class="dropdown-menu">
                                {% for category in sidebar_categories %}
                                <li>
                                    <a class="dropdown-item" href="{% url 'news:category' category.slug %}">
                                        {{ category.name }} ({{ category.news_count }})
                                    </a>
                                </li>
                                {% endfor %}
                            </ul>
                        </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="py-4">
        <div class="container">
            <div class="row">
                <!-- Content -->
                <div class="col-lg-8">
                    {% block content %}
                    {% endblock %}
                </div>
                
                <!-- Sidebar -->
                <div class="col-lg-4">
                    <div class="sticky-top">
                        <!-- Sayt statistikasi -->
                        <div class="card mb-4">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0">Sayt statistikasi</h5>
                        </div>
                        </div>
                        {% endif %}

                        <!-- Kategoriyalar -->
                        {% if sidebar_categories %}
                        <div class="card mb-4">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0">Kategoriyalar</h5>
                            </div>
                            <div class="card-body">
                                {% for category in sidebar_categories %}
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <a href="{% url 'news:category' category.slug %}" 
                                       class="text-decoration-none">
                                        {{ category.name }}
                                    </a>
                                    <span class="badge bg-secondary">{{ category.news_count }}</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}

                        <!-- Kategoriyalar -->
                        {% if sidebar_categories %}
                        <div class="card mb-4">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0">Kategoriyalar</h5>
                            </div>
                            <div class="card-body">
                                {% for category in sidebar_categories %}
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <a href="{% url 'news:category' category.slug %}" 
                                       class="text-decoration-none">
                                        {{ category.name }}
                                    </a>
                                    <span class="badge bg-secondary">{{ category.news_count }}</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}

                        {% block sidebar %}
                        {% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>{{ site_name }}</h5>
                    <p>{{ site_description }}</p>
                </div>
                <div class="col-md-6">
                    <h5>Aloqa</h5>
                    <p>Email: {{ contact_email }}</p>
                    <p>&copy; 2024 {{ site_name }}. Barcha huquqlar himoyalangan.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 5-qadam: Home page template yaratish

`templates/news/home.html` faylini yarating:

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}

{% block content %}
    <!-- Hero section -->
    <div class="jumbotron bg-light p-5 rounded mb-4">
        <div class="container-fluid py-2">
            <h1 class="display-5 fw-bold">{{ site_name }}ga xush kelibsiz!</h1>
            <p class="fs-4">{{ site_description }}</p>
            <p>Bizda {{ total_news_count }} ta yangilik va {{ total_categories_count }} ta kategoriya mavjud.</p>
        </div>
    </div>

    <!-- Tanlangan yangiliklar -->
    {% if featured_news %}
    <section class="mb-5">
        <h2 class="mb-4">Tanlangan yangiliklar</h2>
        <div class="row">
            {% for news in featured_news %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" 
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                <i class="fas fa-folder"></i> {{ news.category.name }} | 
                                <i class="fas fa-calendar"></i> {{ news.published_date|date:"d.m.Y" }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- Oxirgi yangiliklar -->
    {% if recent_news %}
    <section class="mb-5">
        <h2 class="mb-4">Oxirgi yangiliklar</h2>
        <div class="row">
            {% for news in recent_news %}
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-4">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-8{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <h6 class="card-title">
                                    <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                        {{ news.title|truncatewords:12 }}
                                    </a>
                                </h6>
                                <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                                <small class="text-muted">
                                    {{ news.category.name }} | {{ news.published_date|date:"d.m.Y" }}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="text-center">
            <a href="{% url 'news:news-list' %}" class="btn btn-primary">
                Barcha yangiliklarni ko'rish
            </a>
        </div>
    </section>
    {% endif %}
{% endblock %}
```

## 6-qadam: News detail template yaratish

`templates/news/news_detail.html` faylini yarating:

```html
<!-- templates/news/news_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <article class="mb-5">
        <!-- Yangilik sarlavhasi -->
        <header class="mb-4">
            <h1 class="display-6">{{ news.title }}</h1>
            <div class="text-muted mb-3">
                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                <i class="fas fa-calendar me-1"></i> {{ news.published_date|date:"d F Y, H:i" }}
                <i class="fas fa-user ms-3 me-1"></i> {{ news.author.get_full_name|default:news.author.username }}
            </div>
        </header>

        <!-- Yangilik rasmi -->
        {% if news.image %}
        <div class="mb-4">
            <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                 class="img-fluid rounded" style="max-height: 400px; width: 100%; object-fit: cover;">
        </div>
        {% endif %}

        <!-- Yangilik matni -->
        <div class="news-content">
            {{ news.body|linebreaks }}
        </div>

        <!-- Teglar -->
        {% if news.tags.all %}
        <div class="mt-4">
            <h6>Teglar:</h6>
            {% for tag in news.tags.all %}
                <span class="badge bg-light text-dark me-1">#{{ tag.name }}</span>
            {% endfor %}
        </div>
        {% endif %}
    </article>

    <!-- O'xshash yangiliklar -->
    {% if related_news %}
    <section class="mt-5">
        <h3 class="mb-4">O'xshash yangiliklar</h3>
        <div class="row">
            {% for news in related_news %}
            <div class="col-md-6 mb-4">
                <div class="card">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 150px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body">
                        <h6 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h6>
                        <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                        <small class="text-muted">{{ news.published_date|date:"d.m.Y" }}</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
{% endblock %}

{% block sidebar %}
    <!-- Qo'shimcha sidebar elementi -->
    <div class="card">
        <div class="card-header bg-secondary text-white">
            <h6 class="mb-0">Yangilik haqida</h6>
        </div>
        <div class="card-body">
            <p><strong>Kategoriya:</strong> {{ news.category.name }}</p>
            <p><strong>Muallif:</strong> {{ news.author.get_full_name|default:news.author.username }}</p>
            <p><strong>Nashr etildi:</strong> {{ news.published_date|date:"d F Y" }}</p>
            {% if news.updated_date != news.published_date %}
            <p><strong>Yangilandi:</strong> {{ news.updated_date|date:"d F Y" }}</p>
            {% endif %}
        </div>
    </div>
{% endblock %}
```

## 7-qadam: URL konfiguratsiyasini yangilash

`news/urls.py` faylini yangilang:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
]
```

## 8-qadam: Category detail template yaratish

`templates/news/category_detail.html` faylini yarating:

```html
<!-- templates/news/category_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1>{{ category.name }}</h1>
            <p class="text-muted">{{ news_count }} ta yangilik topildi</p>
        </div>
        <div>
            <a href="{% url 'news:news-list' %}" class="btn btn-outline-primary">
                Barcha yangiliklar
            </a>
        </div>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                {{ news.published_date|date:"d.m.Y" }} | {{ news.author.get_full_name|default:news.author.username }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Oldingi</a>
                    </li>
                {% endif %}

                <li class="page-item active">
                    <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
                </li>

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>{{ category.name }} kategoriyasida hozircha yangiliklar yo'q.</p>
            <a href="{% url 'news:home' %}" class="btn btn-primary">Bosh sahifaga qaytish</a>
        </div>
    {% endif %}
{% endblock %}
```

## 9-qadam: News list template yaratish

`templates/news/news_list.html` faylini yarating:

```html
<!-- templates/news/news_list.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Barcha yangiliklar</h1>
        <p class="text-muted mb-0">{{ total_news_count }} ta yangilik</p>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-12 mb-4">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-3">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-9{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        <h5 class="card-title">
                                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                                {{ news.title }}
                                            </a>
                                        </h5>
                                        <p class="card-text">{{ news.body|truncatewords:25 }}</p>
                                        <p class="card-text">
                                            <small class="text-muted">
                                                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                                                {{ news.published_date|date:"d.m.Y" }} | 
                                                {{ news.author.get_full_name|default:news.author.username }}
                                            </small>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">&laquo; Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">&lsaquo; Oldingi</a>
                    </li>
                {% endif %}

                {% for i in page_obj.paginator.page_range %}
                    {% if page_obj.number == i %}
                        <li class="page-item active">
                            <span class="page-link">{{ i }}</span>
                        </li>
                    {% elif i > page_obj.number|add:'-3' and i < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}">{{ i }}</a>
                        </li>
                    {% endif %}
                {% endfor %}

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi &rsaquo;</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi &raquo;</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>Hozircha yangiliklar mavjud emas.</p>
        </div>
    {% endif %}
{% endblock %}
```

## 10-qadam: Testlash va debug qilish

### 1. Server'ni ishga tushiring:
```bash
python manage.py runserver
```

### 2. Context Processor ishlayotganini tekshirish:

`news/context_processors.py`ga debug qo'shing:

```python
# news/context_processors.py
import logging

logger = logging.getLogger(__name__)

def site_data(request):
    """
    Sayt uchun umumiy ma'lumotlar
    """
    logger.info("Site data context processor ishlayapti")
    return {
        'site_name': 'News Portal',
        'site_description': 'Eng so\'nggi yangiliklar va maqolalar',
        'site_author': 'News Team',
        'contact_email': 'info@newsportal.uz',
    }
```

### 3. Template'da debug:
```html
<!-- Template'ning istalgan joyiga qo'shing -->
<!-- DEBUG: Context processor ma'lumotlari -->
{% if debug %}
<div class="alert alert-warning">
    <h6>Debug ma'lumotlari:</h6>
    <p>Site name: {{ site_name }}</p>
    <p>Latest news count: {{ latest_news|length }}</p>
    <p>Categories count: {{ sidebar_categories|length }}</p>
</div>
{% endif %}
```

## 11-qadam: Xatolarga yo'l qo'ymaslik uchun tekshirish

### Umumiy xatolarni tekshirish:

1. **Import xatolari**:
```python
# models.py'da Q import qilishni unutmang
from django.db.models import Q, Count
```

2. **Template yo'llari**:
```python
# URL'larda app_name ishlatganingizga ishonch hosil qiling
app_name = 'news'
```

3. **Media fayllar sozlamasi**:
```python
# settings.py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4. **URL configuration**:
```python
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... boshqa URL'lar
    path('', include('news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Yakuniy natija

Ushbu amaliyotni bajargan so'ng, sizda quyidagilar bo'ladi:

✅ **Context Processor** orqali barcha sahifalarda umumiy ma'lumotlar
✅ **get_context_data()** yordamida har bir view'ga maxsus ma'lumotlar  
✅ Responsive va chiroyli template'lar
✅ Sidebar'da eng oxirgi yangiliklar va kategoriyalar
✅ Sayt statistikasi barcha sahifalarda

## Maslahatlar va Best Practices

### 1. Performance uchun:
- Context processor'larda og'ir operatsiyalar bajarmaslik
- Database so'rovlarini optimallashtirish
- Kerak bo'lganda keshlash qo'llash

### 2. Xavfsizlik uchun:
- Template'larda foydalanuvchi ma'lumotlarini filtrlab ko'rsatish
- XSS hujumlaridan himoyalanish
- Input validation qilish

### 3. Code organizatsiya:
- Context processor'larni alohida fayllarda saqlash
- Template'larni mantiqiy guruhlarga ajratish  
- DRY (Don't Repeat Yourself) printsipini qo'llash

### 4. Debug va testing:
- Development muhitida debug ma'lumotlarini ko'rsatish
- Production'da xato xabarlarini yashirish
- Context ma'lumotlarini tekshirish

## Keyingi qadam

Context Processor va get_context_data() metodlarini muvaffaqiyatli qo'llaganingizdan so'ng, keyingi darsda **Template Tags**'ni o'rganamiz va loyihaga yanada ko'proq funktionallik qo'shamiz.
                        </div>
                        {% endif %}

                        {% block sidebar %}
                        {% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>{{ site_name }}</h5>
                    <p>{{ site_description }}</p>
                </div>
                <div class="col-md-6">
                    <h5>Aloqa</h5>
                    <p>Email: {{ contact_email }}</p>
                    <p>&copy; 2024 {{ site_name }}. Barcha huquqlar himoyalangan.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

## 5-qadam: Home page template yaratish

`templates/news/home.html` faylini yarating:

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}

{% block content %}
    <!-- Hero section -->
    <div class="jumbotron bg-light p-5 rounded mb-4">
        <div class="container-fluid py-2">
            <h1 class="display-5 fw-bold">{{ site_name }}ga xush kelibsiz!</h1>
            <p class="fs-4">{{ site_description }}</p>
            <p>Bizda {{ total_news_count }} ta yangilik va {{ total_categories_count }} ta kategoriya mavjud.</p>
        </div>
    </div>

    <!-- Tanlangan yangiliklar -->
    {% if featured_news %}
    <section class="mb-5">
        <h2 class="mb-4">Tanlangan yangiliklar</h2>
        <div class="row">
            {% for news in featured_news %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" 
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                <i class="fas fa-folder"></i> {{ news.category.name }} | 
                                <i class="fas fa-calendar"></i> {{ news.published_date|date:"d.m.Y" }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- Oxirgi yangiliklar -->
    {% if recent_news %}
    <section class="mb-5">
        <h2 class="mb-4">Oxirgi yangiliklar</h2>
        <div class="row">
            {% for news in recent_news %}
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-4">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-8{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <h6 class="card-title">
                                    <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                        {{ news.title|truncatewords:12 }}
                                    </a>
                                </h6>
                                <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                                <small class="text-muted">
                                    {{ news.category.name }} | {{ news.published_date|date:"d.m.Y" }}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="text-center">
            <a href="{% url 'news:news-list' %}" class="btn btn-primary">
                Barcha yangiliklarni ko'rish
            </a>
        </div>
    </section>
    {% endif %}
{% endblock %}

## 6-qadam: News detail template yaratish

`templates/news/news_detail.html` faylini yarating:

```html
<!-- templates/news/news_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <article class="mb-5">
        <!-- Yangilik sarlavhasi -->
        <header class="mb-4">
            <h1 class="display-6">{{ news.title }}</h1>
            <div class="text-muted mb-3">
                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                <i class="fas fa-calendar me-1"></i> {{ news.published_date|date:"d F Y, H:i" }}
                <i class="fas fa-user ms-3 me-1"></i> {{ news.author.get_full_name|default:news.author.username }}
            </div>
        </header>

        <!-- Yangilik rasmi -->
        {% if news.image %}
        <div class="mb-4">
            <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                 class="img-fluid rounded" style="max-height: 400px; width: 100%; object-fit: cover;">
        </div>
        {% endif %}

        <!-- Yangilik matni -->
        <div class="news-content">
            {{ news.body|linebreaks }}
        </div>

        <!-- Teglar -->
        {% if news.tags.all %}
        <div class="mt-4">
            <h6>Teglar:</h6>
            {% for tag in news.tags.all %}
                <span class="badge bg-light text-dark me-1">#{{ tag.name }}</span>
            {% endfor %}
        </div>
        {% endif %}
    </article>

    <!-- O'xshash yangiliklar -->
    {% if related_news %}
    <section class="mt-5">
        <h3 class="mb-4">O'xshash yangiliklar</h3>
        <div class="row">
            {% for news in related_news %}
            <div class="col-md-6 mb-4">
                <div class="card">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 150px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body">
                        <h6 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h6>
                        <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                        <small class="text-muted">{{ news.published_date|date:"d.m.Y" }}</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
{% endblock %}

{% block sidebar %}
    <!-- Qo'shimcha sidebar elementi -->
    <div class="card">
        <div class="card-header bg-secondary text-white">
            <h6 class="mb-0">Yangilik haqida</h6>
        </div>
        <div class="card-body">
            <p><strong>Kategoriya:</strong> {{ news.category.name }}</p>
            <p><strong>Muallif:</strong> {{ news.author.get_full_name|default:news.author.username }}</p>
            <p><strong>Nashr etildi:</strong> {{ news.published_date|date:"d F Y" }}</p>
            {% if news.updated_date != news.published_date %}
            <p><strong>Yangilandi:</strong> {{ news.updated_date|date:"d F Y" }}</p>
            {% endif %}
        </div>
    </div>
{% endblock %}

## 7-qadam: URL konfiguratsiyasini yangilash

`news/urls.py` faylini yangilang:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
]

## 8-qadam: Category detail template yaratish

`templates/news/category_detail.html` faylini yarating:

```html
<!-- templates/news/category_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1>{{ category.name }}</h1>
            <p class="text-muted">{{ news_count }} ta yangilik topildi</p>
        </div>
        <div>
            <a href="{% url 'news:news-list' %}" class="btn btn-outline-primary">
                Barcha yangiliklar
            </a>
        </div>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                {{ news.published_date|date:"d.m.Y" }} | {{ news.author.get_full_name|default:news.author.username }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Oldingi</a>
                    </li>
                {% endif %}

                <li class="page-item active">
                    <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
                </li>

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>{{ category.name }} kategoriyasida hozircha yangiliklar yo'q.</p>
            <a href="{% url 'news:home' %}" class="btn btn-primary">Bosh sahifaga qaytish</a>
        </div>
    {% endif %}
{% endblock %}

## 9-qadam: News list template yaratish

`templates/news/news_list.html` faylini yarating:

```html
<!-- templates/news/news_list.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Barcha yangiliklar</h1>
        <p class="text-muted mb-0">{{ total_news_count }} ta yangilik</p>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-12 mb-4">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-3">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-9{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        <h5 class="card-title">
                                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                                {{ news.title }}
                                            </a>
                                        </h5>
                                        <p class="card-text">{{ news.body|truncatewords:25 }}</p>
                                        <p class="card-text">
                                            <small class="text-muted">
                                                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                                                {{ news.published_date|date:"d.m.Y" }} | 
                                                {{ news.author.get_full_name|default:news.author.username }}
                                            </small>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">&laquo; Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">&lsaquo; Oldingi</a>
                    </li>
                {% endif %}

                {% for i in page_obj.paginator.page_range %}
                    {% if page_obj.number == i %}
                        <li class="page-item active">
                            <span class="page-link">{{ i }}</span>
                        </li>
                    {% elif i > page_obj.number|add:'-3' and i < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}">{{ i }}</a>
                        </li>
                    {% endif %}
                {% endfor %}

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi &rsaquo;</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi &raquo;</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>Hozircha yangiliklar mavjud emas.</p>
        </div>
    {% endif %}
{% endblock %}

## 10-qadam: Testlash va debug qilish

### 1. Server'ni ishga tushiring:
```bash
python manage.py runserver
```

### 2. Context Processor ishlayotganini tekshirish:

`news/context_processors.py`ga debug qo'shing:

```python
# news/context_processors.py
import logging

logger = logging.getLogger(__name__)

def site_data(request):
    """
    Sayt uchun umumiy ma'lumotlar
    """
    logger.info("Site data context processor ishlayapti")
    return {
        'site_name': 'News Portal',
        'site_description': 'Eng so\'nggi yangiliklar va maqolalar',
        'site_author': 'News Team',
        'contact_email': 'info@newsportal.uz',
    }
```

### 3. Template'da debug:
```html
<!-- Template'ning istalgan joyiga qo'shing -->
<!-- DEBUG: Context processor ma'lumotlari -->
{% if debug %}
<div class="alert alert-warning">
    <h6>Debug ma'lumotlari:</h6>
    <p>Site name: {{ site_name }}</p>
    <p>Latest news count: {{ latest_news|length }}</p>
    <p>Categories count: {{ sidebar_categories|length }}</p>
</div>
{% endif %}
```

## 11-qadam: Xatolarga yo'l qo'ymaslik uchun tekshirish

### Umumiy xatolarani tekshirish:

1. **Import xatolari**:
```python
# models.py'da Q import qilishni unutmang
from django.db.models import Q, Count
```

2. **Template yo'llari**:
```python
# URL'larda app_name ishlatganingizga ishonch hosil qiling
app_name = 'news'
```

3. **Media fayllar sozlamasi**:
```python
# settings.py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4. **URL configuration**:
```python
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... boshqa URL'lar
    path('', include('news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Yakuniy natija

Ushbu amaliyotni bajargan so'ng, sizda quyidagilar bo'ladi:

✅ **Context Processor** orqali barcha sahifalarda umumiy ma'lumotlar
✅ **get_context_data()** yordamida har bir view'ga maxsus ma'lumotlar  
✅ Responsive va chiroyli template'lar
✅ Sidebar'da eng oxirgi yangiliklar va kategoriyalar
✅ Sayt statistikasi barcha sahifalarda

## Maslahatlar va Best Practices

### 1. Performance uchun:
- Context processor'larda og'ir operatsiyalar bajarmaslik
- Database so'rovlarini optimallashtirish
- Kerak bo'lganda keshlash qo'llash

### 2. Xavfsizlik uchun:
- Template'larda foydalanuvchi ma'lumotlarini filtrlab ko'rsatish
- XSS hujumlaridan himoyalanish
- Input validation qilish

### 3. Code organizatsiya:
- Context processor'larni alohida fayllarda saqlash
- Template'larni mantiqiy guruhlarga ajratish  
- DRY (Don't Repeat Yourself) printsipini qo'llash

### 4. Debug va testing:
- Development muhitida debug ma'lumotlarini ko'rsatish
- Production'da xato xabarlarini yashirish
- Context ma'lumotlarini tekshirish

## Keyingi qadam

Context Processor va get_context_data() metodlarini muvaffaqiyatli qo'llaganingizdan so'ng, keyingi darsda **Template Tags**'ni o'rganamiz va loyihaga yanada ko'proq funktionallik qo'shamiz.>
                    </div>
                    {% endif %}

                    <!-- Kategoriyalar -->
                    {% if sidebar_categories %}
                    <div class="card mb-4">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">Kategoriyalar</h5>
                        </div>
                        <div class="card-body">
                            {% for category in sidebar_categories %}
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <a href="{% url 'news:category' category.slug %}" 
                                   class="text-decoration-none">
                                    {{ category.name }}
                                </a>
                                <span class="badge bg-secondary">{{ category.news_count }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}

                    {% block sidebar %}
                    {% endblock %}
                </div>
            </div>
        </div>
    </div>
</main>

<!-- Footer -->
<footer class="bg-dark text-white py-4 mt-5">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <h5>{{ site_name }}</h5>
                <p>{{ site_description }}</p>
            </div>
            <div class="col-md-6">
                <h5>Aloqa</h5>
                <p>Email: {{ contact_email }}</p>
                <p>&copy; 2024 {{ site_name }}. Barcha huquqlar himoyalangan.</p>
            </div>
        </div>
    </div>
</footer>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}{% endblock %}
</body>
</html>>
                        </div>
                        {% endif %}

                        <!-- Kategoriyalar -->
                        {% if sidebar_categories %}
                        <div class="card mb-4">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0">Kategoriyalar</h5>
                            </div>
                            <div class="card-body">
                                {% for category in sidebar_categories %}
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <a href="{% url 'news:category' category.slug %}" 
                                       class="text-decoration-none">
                                        {{ category.name }}
                                    </a>
                                    <span class="badge bg-secondary">{{ category.news_count }}</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}

                        {% block sidebar %}
                        {% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>{{ site_name }}</h5>
                    <p>{{ site_description }}</p>
                </div>
                <div class="col-md-6">
                    <h5>Aloqa</h5>
                    <p>Email: {{ contact_email }}</p>
                    <p>&copy; 2024 {{ site_name }}. Barcha huquqlar himoyalangan.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 5-qadam: Home page template yaratish

`templates/news/home.html` faylini yarating:

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}

{% block content %}
    <!-- Hero section -->
    <div class="jumbotron bg-light p-5 rounded mb-4">
        <div class="container-fluid py-2">
            <h1 class="display-5 fw-bold">{{ site_name }}ga xush kelibsiz!</h1>
            <p class="fs-4">{{ site_description }}</p>
            <p>Bizda {{ total_news_count }} ta yangilik va {{ total_categories_count }} ta kategoriya mavjud.</p>
        </div>
    </div>

    <!-- Tanlangan yangiliklar -->
    {% if featured_news %}
    <section class="mb-5">
        <h2 class="mb-4">Tanlangan yangiliklar</h2>
        <div class="row">
            {% for news in featured_news %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" 
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                <i class="fas fa-folder"></i> {{ news.category.name }} | 
                                <i class="fas fa-calendar"></i> {{ news.published_date|date:"d.m.Y" }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- Oxirgi yangiliklar -->
    {% if recent_news %}
    <section class="mb-5">
        <h2 class="mb-4">Oxirgi yangiliklar</h2>
        <div class="row">
            {% for news in recent_news %}
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-4">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-8{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <h6 class="card-title">
                                    <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                        {{ news.title|truncatewords:12 }}
                                    </a>
                                </h6>
                                <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                                <small class="text-muted">
                                    {{ news.category.name }} | {{ news.published_date|date:"d.m.Y" }}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="text-center">
            <a href="{% url 'news:news-list' %}" class="btn btn-primary">
                Barcha yangiliklarni ko'rish
            </a>
        </div>
    </section>
    {% endif %}
{% endblock %}
```

## 6-qadam: News detail template yaratish

`templates/news/news_detail.html` faylini yarating:

```html
<!-- templates/news/news_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <article class="mb-5">
        <!-- Yangilik sarlavhasi -->
        <header class="mb-4">
            <h1 class="display-6">{{ news.title }}</h1>
            <div class="text-muted mb-3">
                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                <i class="fas fa-calendar me-1"></i> {{ news.published_date|date:"d F Y, H:i" }}
                <i class="fas fa-user ms-3 me-1"></i> {{ news.author.get_full_name|default:news.author.username }}
            </div>
        </header>

        <!-- Yangilik rasmi -->
        {% if news.image %}
        <div class="mb-4">
            <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                 class="img-fluid rounded" style="max-height: 400px; width: 100%; object-fit: cover;">
        </div>
        {% endif %}

        <!-- Yangilik matni -->
        <div class="news-content">
            {{ news.body|linebreaks }}
        </div>

        <!-- Teglar -->
        {% if news.tags.all %}
        <div class="mt-4">
            <h6>Teglar:</h6>
            {% for tag in news.tags.all %}
                <span class="badge bg-light text-dark me-1">#{{ tag.name }}</span>
            {% endfor %}
        </div>
        {% endif %}
    </article>

    <!-- O'xshash yangiliklar -->
    {% if related_news %}
    <section class="mt-5">
        <h3 class="mb-4">O'xshash yangiliklar</h3>
        <div class="row">
            {% for news in related_news %}
            <div class="col-md-6 mb-4">
                <div class="card">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 150px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body">
                        <h6 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title|truncatewords:10 }}
                            </a>
                        </h6>
                        <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                        <small class="text-muted">{{ news.published_date|date:"d.m.Y" }}</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
{% endblock %}

{% block sidebar %}
    <!-- Qo'shimcha sidebar elementi -->
    <div class="card">
        <div class="card-header bg-secondary text-white">
            <h6 class="mb-0">Yangilik haqida</h6>
        </div>
        <div class="card-body">
            <p><strong>Kategoriya:</strong> {{ news.category.name }}</p>
            <p><strong>Muallif:</strong> {{ news.author.get_full_name|default:news.author.username }}</p>
            <p><strong>Nashr etildi:</strong> {{ news.published_date|date:"d F Y" }}</p>
            {% if news.updated_date != news.published_date %}
            <p><strong>Yangilandi:</strong> {{ news.updated_date|date:"d F Y" }}</p>
            {% endif %}
        </div>
    </div>
{% endblock %}
```

## 7-qadam: URL konfiguratsiyasini yangilash

`news/urls.py` faylini yangilang:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
]
```

## 8-qadam: Category detail template yaratish

`templates/news/category_detail.html` faylini yarating:

```html
<!-- templates/news/category_detail.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1>{{ category.name }}</h1>
            <p class="text-muted">{{ news_count }} ta yangilik topildi</p>
        </div>
        <div>
            <a href="{% url 'news:news-list' %}" class="btn btn-outline-primary">
                Barcha yangiliklar
            </a>
        </div>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}"
                         style="height: 200px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                {{ news.title }}
                            </a>
                        </h5>
                        <p class="card-text flex-grow-1">{{ news.body|truncatewords:20 }}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                {{ news.published_date|date:"d.m.Y" }} | {{ news.author.get_full_name|default:news.author.username }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Oldingi</a>
                    </li>
                {% endif %}

                <li class="page-item active">
                    <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
                </li>

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>{{ category.name }} kategoriyasida hozircha yangiliklar yo'q.</p>
            <a href="{% url 'news:home' %}" class="btn btn-primary">Bosh sahifaga qaytish</a>
        </div>
    {% endif %}
{% endblock %}
```

## 9-qadam: News list template yaratish

`templates/news/news_list.html` faylini yarating:

```html
<!-- templates/news/news_list.html -->
{% extends 'base.html' %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Barcha yangiliklar</h1>
        <p class="text-muted mb-0">{{ total_news_count }} ta yangilik</p>
    </div>

    {% if news_list %}
        <div class="row">
            {% for news in news_list %}
            <div class="col-md-12 mb-4">
                <div class="card">
                    <div class="row g-0">
                        {% if news.image %}
                        <div class="col-md-3">
                            <img src="{{ news.image.url }}" class="img-fluid rounded-start h-100" 
                                 alt="{{ news.title }}" style="object-fit: cover;">
                        </div>
                        {% endif %}
                        <div class="{% if news.image %}col-md-9{% else %}col-md-12{% endif %}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        <h5 class="card-title">
                                            <a href="{% url 'news:detail' news.slug %}" class="text-decoration-none">
                                                {{ news.title }}
                                            </a>
                                        </h5>
                                        <p class="card-text">{{ news.body|truncatewords:25 }}</p>
                                        <p class="card-text">
                                            <small class="text-muted">
                                                <span class="badge bg-primary me-2">{{ news.category.name }}</span>
                                                {{ news.published_date|date:"d.m.Y" }} | 
                                                {{ news.author.get_full_name|default:news.author.username }}
                                            </small>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Pagination -->
        {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">&laquo; Birinchi</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">&lsaquo; Oldingi</a>
                    </li>
                {% endif %}

                {% for i in page_obj.paginator.page_range %}
                    {% if page_obj.number == i %}
                        <li class="page-item active">
                            <span class="page-link">{{ i }}</span>
                        </li>
                    {% elif i > page_obj.number|add:'-3' and i < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}">{{ i }}</a>
                        </li>
                    {% endif %}
                {% endfor %}

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi &rsaquo;</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Oxirgi &raquo;</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info">
            <h4>Yangiliklar topilmadi</h4>
            <p>Hozircha yangiliklar mavjud emas.</p>
        </div>
    {% endif %}
{% endblock %}
```

## 10-qadam: Testlash va debug qilish

### 1. Server'ni ishga tushiring:
```bash
python manage.py runserver
```

### 2. Context Processor ishlayotganini tekshirish:

`news/context_processors.py`ga debug qo'shing:

```python
# news/context_processors.py
import logging

logger = logging.getLogger(__name__)

def site_data(request):
    """
    Sayt uchun umumiy ma'lumotlar
    """
    logger.info("Site data context processor ishlayapti")
    return {
        'site_name': 'News Portal',
        'site_description': 'Eng so\'nggi yangiliklar va maqolalar',
        'site_author': 'News Team',
        'contact_email': 'info@newsportal.uz',
    }
```

### 3. Template'da debug:
```html
<!-- Template'ning istalgan joyiga qo'shing -->
<!-- DEBUG: Context processor ma'lumotlari -->
{% if debug %}
<div class="alert alert-warning">
    <h6>Debug ma'lumotlari:</h6>
    <p>Site name: {{ site_name }}</p>
    <p>Latest news count: {{ latest_news|length }}</p>
    <p>Categories count: {{ sidebar_categories|length }}</p>
</div>
{% endif %}
```

## 11-qadam: Xatolarga yo'l qo'ymaslik uchun tekshirish

### Umumiy xatolaani tekshirish:

1. **Import xatolari**:
```python
# models.py'da Q import qilishni unutmang
from django.db.models import Q, Count
```

2. **Template yo'llari**:
```python
# URL'larda app_name ishlatganingizga ishonch hosil qiling
app_name = 'news'
```

3. **Media fayllar sozlamasi**:
```python
# settings.py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4. **URL configuration**:
```python
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... boshqa URL'lar
    path('', include('news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Yakuniy natija

Ushbu amaliyotni bajarib bo'lgach, sizda:

✅ Context Processor orqali barcha sahifalarda umumiy ma'lumotlar ko'rsatiladi
✅ get_context_data() yordamida har bir view'ga maxsus ma'lumotlar qo'shiladi
✅ Responsive va chiroyli template'lar yaratiladi
✅ Sidebar'da eng oxirgi yangiliklar va kategoriyalar avtomatik ko'rsatiladi
✅ Sayt statistikasi barcha sahifalarda mavjud bo'ladi
