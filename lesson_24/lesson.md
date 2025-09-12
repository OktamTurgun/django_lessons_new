# Dars 24: Context_processor va get_context_data

## Darsning maqsadi
Ushbu darsda biz Django'da **Context Processor** va **get_context_data** metodlari bilan ishlashni o'rganamiz. Bu vositalar orqali template'larga ma'lumotlarni uzatish va barcha sahifalarda umumiy ma'lumotlarni ko'rsatishni amalga oshiramiz.

## Nazariy qism

### Context nima?
**Context** - bu template'ga uzatiladigan ma'lumotlar to'plami. Bu Python dictionary formatida bo'lib, template ichida o'zgaruvchilar sifatida ishlatiladi.

### Context Processor nima?
**Context Processor** - bu barcha template'larga avtomatik ravishda ma'lumot uzatuvchi maxsus funksiya. Bu funksiya har bir so'rov (request) uchun ishga tushadi va qaytaradigan ma'lumotlar barcha template'larda mavjud bo'ladi.

### get_context_data() metodi
**get_context_data()** - bu Class-Based View'larda context'ni boshqarish uchun ishlatiladigan metod. Bu metod orqali view'dan template'ga qo'shimcha ma'lumotlar uzatish mumkin.

## 1-bosqich: Context Processor yaratish

### Context Processor funksiyasini yaratish

Avval `news/context_processors.py` faylini yaratamiz:

```python
# news/context_processors.py
from .models import News, Category

def latest_news(request):
    """
    Eng oxirgi yangiliklarni barcha sahifalarda ko'rsatish uchun
    context processor
    """
    latest = News.published.all()[:5]  # Eng oxirgi 5ta yangilik
    return {
        'latest_news': latest
    }

def categories_processor(request):
    """
    Barcha kategoriyalarni sidebar'da ko'rsatish uchun
    context processor
    """
    categories = Category.objects.all()
    return {
        'categories': categories
    }

def site_info(request):
    """
    Sayt haqida umumiy ma'lumotlar
    """
    return {
        'site_name': 'Yangiliklar Sayti',
        'site_description': 'Eng oxirgi yangiliklar va maqolalar',
        'contact_email': 'info@news.uz'
    }
```

### Context Processor'ni settings.py'da ro'yxatdan o'tkazish

`config/settings.py` faylida TEMPLATES bo'limini yangilaymiz:

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
                'news.context_processors.latest_news',
                'news.context_processors.categories_processor',
                'news.context_processors.site_info',
            ],
        },
    },
]
```

## 2-bosqich: get_context_data() metodini ishlatish

### Oddiy Function-Based View'da context

```python
# news/views.py
from django.shortcuts import render
from .models import News, Category

def home_view(request):
    """
    Bosh sahifa uchun oddiy function-based view
    """
    featured_news = News.published.filter(status='published')[:6]
    
    context = {
        'featured_news': featured_news,
        'page_title': 'Bosh sahifa',
    }
    # Context processor'dan kelayotgan ma'lumotlar avtomatik qo'shiladi
    return render(request, 'news/home.html', context)
```

### Class-Based View'da get_context_data()

```python
# news/views.py
from django.views.generic import ListView, DetailView
from .models import News, Category

class HomeView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news_list'
    paginate_by = 6
    
    def get_queryset(self):
        """
        Faqat nashr qilingan yangiliklarni olish
        """
        return News.published.filter(status='published')
    
    def get_context_data(self, **kwargs):
        """
        Template'ga qo'shimcha ma'lumotlar uzatish
        """
        context = super().get_context_data(**kwargs)
        
        # Qo'shimcha ma'lumotlarni qo'shish
        context['featured_news'] = News.published.filter(featured=True)[:3]
        context['page_title'] = 'Bosh sahifa - Yangiliklar'
        context['total_news'] = News.published.count()
        
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        """
        Yangilik detail sahifasi uchun qo'shimcha context
        """
        context = super().get_context_data(**kwargs)
        
        # Tegishli yangiliklarni olish
        current_news = self.get_object()
        related_news = News.published.filter(
            category=current_news.category
        ).exclude(id=current_news.id)[:4]
        
        context['related_news'] = related_news
        context['page_title'] = current_news.title
        
        return context

class CategoryNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Kategoriya bo'yicha yangiliklarni filtrlash
        """
        category_slug = self.kwargs['slug']
        return News.published.filter(
            category__slug=category_slug,
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        
        context['category'] = category
        context['page_title'] = f'{category.name} - Kategoriya'
        context['news_count'] = self.get_queryset().count()
        
        return context
```

## 3-bosqich: Template'larda ishlatish

### Base template'da context processor ma'lumotlarini ishlatish

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site_name }}{% endblock %}</title>
    <meta name="description" content="{{ site_description }}">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <a href="{% url 'news:home' %}" class="brand">
                    {{ site_name }}
                </a>
                
                <!-- Kategoriyalar menusi -->
                <ul class="nav-menu">
                    <li><a href="{% url 'news:home' %}">Bosh sahifa</a></li>
                    {% for category in categories %}
                        <li>
                            <a href="{% url 'news:category' category.slug %}">
                                {{ category.name }}
                            </a>
                        </li>
                    {% endfor %}
                    <li><a href="{% url 'news:contact' %}">Aloqa</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <div class="container">
            <div class="row">
                <div class="col-md-8">
                    {% block content %}
                    {% endblock %}
                </div>
                
                <div class="col-md-4">
                    <!-- Sidebar - Eng oxirgi yangiliklar -->
                    <div class="sidebar">
                        <div class="widget">
                            <h3>Eng oxirgi yangiliklar</h3>
                            {% for news in latest_news %}
                                <div class="latest-news-item">
                                    <h5>
                                        <a href="{% url 'news:detail' news.slug %}">
                                            {{ news.title|truncatewords:8 }}
                                        </a>
                                    </h5>
                                    <p class="text-muted">
                                        {{ news.published_date|date:"d.m.Y" }}
                                    </p>
                                </div>
                            {% endfor %}
                        </div>
                        
                        <div class="widget">
                            <h3>Kategoriyalar</h3>
                            <ul class="category-list">
                                {% for category in categories %}
                                    <li>
                                        <a href="{% url 'news:category' category.slug %}">
                                            {{ category.name }}
                                            <span class="badge">{{ category.news_set.count }}</span>
                                        </a>
                                    </li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 {{ site_name }}. Barcha huquqlar himoyalangan.</p>
            <p>Aloqa: {{ contact_email }}</p>
        </div>
    </footer>
</body>
</html>
```

### Home page template'da get_context_data ma'lumotlarini ishlatish

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
    <div class="hero-section">
        <h1>{{ site_name }}ga xush kelibsiz!</h1>
        <p>{{ site_description }}</p>
    </div>

    <!-- Asosiy yangiliklarni ko'rsatish -->
    {% if featured_news %}
        <section class="featured-news">
            <h2>Tanlangan yangiliklar</h2>
            <div class="row">
                {% for news in featured_news %}
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            {% if news.image %}
                                <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}">
                            {% endif %}
                            <div class="card-body">
                                <h5 class="card-title">
                                    <a href="{% url 'news:detail' news.slug %}">
                                        {{ news.title }}
                                    </a>
                                </h5>
                                <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                                <div class="card-meta">
                                    <small class="text-muted">
                                        {{ news.category.name }} | {{ news.published_date|date:"d.m.Y" }}
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}

    <!-- Barcha yangiliklar -->
    <section class="all-news">
        <h2>Barcha yangiliklar</h2>
        <p>Jami {{ total_news }} ta yangilik</p>
        
        <div class="row">
            {% for news in news_list %}
                <div class="col-md-6 mb-4">
                    <div class="card">
                        <div class="row no-gutters">
                            <div class="col-md-4">
                                {% if news.image %}
                                    <img src="{{ news.image.url }}" class="card-img" alt="{{ news.title }}">
                                {% endif %}
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <a href="{% url 'news:detail' news.slug %}">
                                            {{ news.title }}
                                        </a>
                                    </h6>
                                    <p class="card-text">{{ news.body|truncatewords:15 }}</p>
                                    <small class="text-muted">
                                        {{ news.published_date|date:"d.m.Y" }}
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        {% include 'partials/pagination.html' %}
    </section>
{% endblock %}
```

## 4-bosqich: URLlar va to'liq integratsiya

### URL konfiguratsiyasi

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryNewsView.as_view(), name='category'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
```

### Kengaytirilgan Context Processor

```python
# news/context_processors.py
from django.db.models import Count
from .models import News, Category

def comprehensive_context(request):
    """
    Keng qamrovli context processor
    """
    return {
        # Statistika
        'total_news_count': News.published.count(),
        'total_categories': Category.objects.count(),
        
        # Eng ko'p o'qilgan yangiliklar
        'popular_news': News.published.order_by('-views_count')[:5],
        
        # Kategoriyalar yangiliklarini sanash bilan
        'categories_with_count': Category.objects.annotate(
            news_count=Count('news')
        ),
        
        # Sayt sozlamalari
        'site_settings': {
            'name': 'Yangiliklar Sayti',
            'description': 'Eng oxirgi yangiliklar va maqolalar',
            'keywords': 'yangiliklar, maqolalar, sport, siyosat',
            'author': 'News Team',
            'contact_email': 'info@news.uz',
            'phone': '+998 90 123 45 67',
        }
    }
```

## Xatolarga e'tibor berish

### 1. Context Processor xatolari

```python
# news/context_processors.py
from django.db import DatabaseError
from .models import News, Category

def safe_latest_news(request):
    """
    Xavfsiz context processor - xatolarga chidamli
    """
    try:
        latest = News.published.all()[:5]
        return {'latest_news': latest}
    except DatabaseError:
        return {'latest_news': []}

def safe_categories(request):
    """
    Kategoriyalar uchun xavfsiz context processor
    """
    try:
        categories = Category.objects.all()
        return {'categories': categories}
    except DatabaseError:
        return {'categories': []}
```

### 2. Template'da xatolarga e'tibor

```html
<!-- Xavfsiz template kodi -->
{% if latest_news %}
    <div class="latest-news">
        <h3>Eng oxirgi yangiliklar</h3>
        {% for news in latest_news %}
            <div class="news-item">
                <a href="{% url 'news:detail' news.slug %}">
                    {{ news.title|default:"Sarlavha mavjud emas" }}
                </a>
            </div>
        {% empty %}
            <p>Hozircha yangiliklar yo'q.</p>
        {% endfor %}
    </div>
{% endif %}
```

## Best Practices va Tavsiyalar

### 1. Context Processor'larni optimallashtirish
- Faqat zarur ma'lumotlarni qaytaring
- Database so'rovlarini kamaytiring
- Keshdan foydalaning

### 2. get_context_data() ni to'g'ri ishlatish
- Har doim `super().get_context_data(**kwargs)` ni chaqiring
- Context nomlarini aniq va tushunarli qiling
- Ortiqcha ma'lumot uzatmang

### 3. Xavfsizlik
- Foydalanuvchi ma'lumotlarini tekshiring
- XSS hujumlaridan himoyalaning
- Template'da ma'lumotlarni filtrlang

### 4. Performance
- Context processor'lar har so'rovda ishlaydi
- Og'ir operatsiyalardan saqlaning
- Kerak bo'lganda keshlash qo'llang

## Xulosa

Context Processor va get_context_data() metodlari Django'da ma'lumotlarni template'larga uzatishning qudratli vositalaridir:

- **Context Processor** - barcha sahifalarda umumiy ma'lumotlar uchun
- **get_context_data()** - alohida view'lar uchun maxsus ma'lumotlar
- Ikkalasi ham template'larda foydalanish uchun ma'lumotlarni tayyorlaydi
- To'g'ri ishlatilganda sayt performance va foydalanuvchi tajribasini yaxshilaydi

**Keyingi darsda:**
Template teglari va filtrlar bilan ishlashni o'rganamiz.