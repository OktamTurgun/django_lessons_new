# Dars 22 - Amaliyot: Bosh sahifada yangiliklarni kategoriya bo'yicha ko'rsatish (1-qism)

## Maqsad
Bu amaliyotda siz yangilik saytining bosh sahifasini yaratib, yangiliklarni kategoriyalar bo'yicha chiroyli va samarali tarzda ko'rsatishni o'rganasiz.

## Loyiha tuzilmasi
```
news_site/
  ├── models.py          # Category, News modellari
  ├── managers.py        # Custom manager va QuerySet
  ├── views.py          # HomeView va boshqa view'lar
  ├── urls.py           # URL konfiguratsiyasi
  ├── admin.py          # Admin interface
  └── templates/
      ├── base.html
      ├── home.html     # Bosh sahifa
      ├── category_detail.html
      └── includes/
          ├── news_card.html
          └── category_section.html
```

## 1-bosqich: Modellarni yaratish va yaxshilash

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    """Yangilik kategoriyalari"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Kategoriya nomi')
    slug = models.SlugField(unique=True, verbose_name='URL nomi')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    color = models.CharField(
        max_length=20, 
        default='primary', 
        verbose_name='Bootstrap rang',
        help_text='primary, success, danger, warning, info, dark'
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name='FontAwesome icon',
        help_text='Masalan: newspaper, laptop, futbol'
    )
    is_featured = models.BooleanField(
        default=False, 
        verbose_name='Bosh sahifada ko\'rsatish'
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name='Tartib raqami',
        help_text='Kichik raqam birinchi ko\'rsatiladi'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
    def get_published_news_count(self):
        """Nashr etilgan yangiliklar soni"""
        return self.news_set.filter(published=True).count()
    
    def get_latest_news(self, count=6):
        """Eng yangi yangiliklar"""
        return self.news_set.filter(published=True)\
            .select_related('author')\
            .order_by('-created_at')[:count]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class News(models.Model):
    """Yangiliklar modeli"""
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    slug = models.SlugField(unique=True, verbose_name='URL nomi')
    content = models.TextField(verbose_name='To\'liq matn')
    summary = models.TextField(
        max_length=300, 
        blank=True, 
        verbose_name='Qisqacha mazmuni',
        help_text='Bo\'sh qoldirilsa, avtomatik yaratiladi'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Muallif'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='Kategoriya'
    )
    image = models.ImageField(
        upload_to='news/%Y/%m/', 
        blank=True, 
        verbose_name='Asosiy rasm'
    )
    published = models.BooleanField(default=False, verbose_name='Nashr etilsinmi')
    is_featured = models.BooleanField(
        default=False, 
        verbose_name='Asosiy yangilik (Hero)',
        help_text='Bosh sahifada katta ko\'rsatiladi'
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name='Ko\'rishlar soni')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['published', '-created_at']),
            models.Index(fields=['category', 'published']),
            models.Index(fields=['is_featured', 'published']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})
    
    def get_summary(self):
        """Qisqacha matn yaratish"""
        if self.summary:
            return self.summary
        
        # HTML taglarini olib tashlash va qisqartirish
        import re
        text = re.sub(r'<[^>]+>', '', self.content)
        return text[:200] + '...' if len(text) > 200 else text
    
    def increment_views(self):
        """Ko'rishlar sonini oshirish"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        
        # Avtomatik summary yaratish
        if not self.summary and self.content:
            import re
            text = re.sub(r'<[^>]+>', '', self.content)
            self.summary = text[:250] + '...' if len(text) > 250 else text
        
        super().save(*args, **kwargs)
```

## 2-bosqich: Custom Manager va QuerySet

```python
# managers.py
from django.db import models
from django.db.models import Count, Q, Prefetch

class NewsQuerySet(models.QuerySet):
    """Custom QuerySet for News"""
    
    def published(self):
        """Nashr etilgan yangiliklar"""
        return self.filter(published=True)
    
    def featured(self):
        """Asosiy yangiliklar"""
        return self.filter(is_featured=True)
    
    def by_category(self, category):
        """Kategoriya bo'yicha"""
        if isinstance(category, str):
            return self.filter(category__slug=category)
        return self.filter(category=category)
    
    def with_relations(self):
        """Bog'langan obyektlar bilan"""
        return self.select_related('category', 'author')
    
    def latest_first(self):
        """Eng yangilar birinchi"""
        return self.order_by('-created_at')
    
    def popular(self):
        """Mashhur yangiliklar (ko'p ko'rilgan)"""
        return self.filter(views_count__gt=0).order_by('-views_count')
    
    def search(self, query):
        """Qidiruv"""
        return self.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(summary__icontains=query)
        )

class NewsManager(models.Manager):
    """Custom Manager for News"""
    
    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured(self):
        return self.get_queryset().published().featured()
    
    def by_category(self, category):
        return self.get_queryset().published().by_category(category)
    
    def latest(self, count=10):
        return self.get_queryset().published().with_relations().latest_first()[:count]
    
    def popular(self, count=5):
        return self.get_queryset().published().popular()[:count]
    
    def search(self, query):
        return self.get_queryset().published().search(query).with_relations()

class CategoryQuerySet(models.QuerySet):
    """Custom QuerySet for Category"""
    
    def featured(self):
        """Bosh sahifada ko'rsatiladigan kategoriyalar"""
        return self.filter(is_featured=True)
    
    def with_news_count(self):
        """Yangiliklar soni bilan"""
        return self.annotate(
            published_news_count=Count(
                'news',
                filter=Q(news__published=True)
            )
        )
    
    def has_news(self):
        """Yangiliği bor kategoriyalar"""
        return self.filter(news__published=True).distinct()
    
    def with_latest_news(self, count=6):
        """Eng yangi yangilikar bilan"""
        return self.prefetch_related(
            Prefetch(
                'news_set',
                queryset=models.Q(published=True).order_by('-created_at')[:count],
                to_attr='latest_news'
            )
        )

class CategoryManager(models.Manager):
    """Custom Manager for Category"""
    
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
    
    def featured(self):
        return self.get_queryset().featured()
    
    def with_news(self):
        return self.get_queryset().has_news().with_news_count()
    
    def for_homepage(self):
        """Bosh sahifa uchun kategoriyalar"""
        from .models import News
        return self.get_queryset().featured().prefetch_related(
            Prefetch(
                'news_set',
                queryset=News.objects.published().select_related('author').order_by('-created_at')[:6],
                to_attr='latest_news'
            )
        ).annotate(
            published_count=Count('news', filter=Q(news__published=True))
        ).filter(published_count__gt=0)

# models.py ga qo'shish
from .managers import NewsManager, CategoryManager

class Category(models.Model):
    # ... maydonlar ...
    
    objects = CategoryManager()  # Custom manager
    
    # ... metodlar ...

class News(models.Model):
    # ... maydonlar ...
    
    objects = NewsManager()  # Custom manager
    
    # ... metodlar ...
```

## 3-bosqich: View'larni yaratish

```python
# views.py
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Prefetch
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.cache import cache
from .models import Category, News

class HomeView(TemplateView):
    """Bosh sahifa"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cache'dan ma'lumotlarni olishga harakat qilish
        cache_timeout = 300  # 5 daqiqa
        
        # 1. Hero section uchun asosiy yangilik
        featured_news = cache.get('home_featured_news')
        if not featured_news:
            featured_news = News.objects.featured().with_relations().first()
            cache.set('home_featured_news', featured_news, cache_timeout)
        context['featured_news'] = featured_news
        
        # 2. Kategoriyalar va ularning yangiliklarini olish
        categories_data = cache.get('home_categories_data')
        if not categories_data:
            categories_data = self.get_categories_with_news()
            cache.set('home_categories_data', categories_data, cache_timeout)
        context['categories_with_news'] = categories_data
        
        # 3. Eng mashhur yangiliklar
        popular_news = cache.get('home_popular_news')
        if not popular_news:
            popular_news = News.objects.popular(8)
            cache.set('home_popular_news', popular_news, cache_timeout)
        context['popular_news'] = popular_news
        
        # 4. Eng yangi yangiliklar (sidebar uchun)
        latest_news = cache.get('home_latest_news')
        if not latest_news:
            latest_news = News.objects.latest(10)
            cache.set('home_latest_news', latest_news, cache_timeout)
        context['latest_news'] = latest_news
        
        # 5. Statistika
        context['stats'] = self.get_site_stats()
        
        return context
    
    def get_categories_with_news(self):
        """Kategoriyalar va ularning yangiliklarini olish"""
        return Category.objects.for_homepage()
    
    def get_site_stats(self):
        """Sayt statistikasi"""
        stats_cache_key = 'home_site_stats'
        stats = cache.get(stats_cache_key)
        
        if not stats:
            stats = {
                'total_news': News.objects.published().count(),
                'total_categories': Category.objects.has_news().count(),
                'total_views': News.objects.published().aggregate(
                    total=models.Sum('views_count')
                )['total'] or 0,
            }
            cache.set(stats_cache_key, stats, 600)  # 10 daqiqa cache
        
        return stats

class CategoryDetailView(DetailView):
    """Kategoriya sahifasi"""
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategoriya yangiliklarini sahifalash
        news_list = News.objects.by_category(self.object).with_relations()
        paginator = Paginator(news_list, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['news_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        
        # Boshqa kategoriyalar
        context['other_categories'] = Category.objects.featured().exclude(
            id=self.object.id
        )[:5]
        
        return context

class NewsDetailView(DetailView):
    """Yangilik sahifasi"""
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.published().with_relations()
    
    def get_object(self):
        obj = super().get_object()
        # Ko'rishlar sonini oshirish
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # O'xshash yangiliklar
        context['related_news'] = News.objects.by_category(
            self.object.category
        ).exclude(id=self.object.id)[:4]
        
        return context

class SearchView(ListView):
    """Qidiruv sahifasi"""
    model = News
    template_name = 'search.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return News.objects.search(query)
        return News.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_results'] = self.get_queryset().count()
        return context

# AJAX view'lar
class PopularNewsAjaxView(ListView):
    """AJAX orqali mashhur yangiliklar"""
    model = News
    template_name = 'includes/popular_news_list.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        period = self.request.GET.get('period', 'week')  # day, week, month, all
        limit = int(self.request.GET.get('limit', 5))
        
        if period == 'day':
            from datetime import datetime, timedelta
            date_from = datetime.now() - timedelta(days=1)
            queryset = News.objects.published().filter(
                created_at__gte=date_from
            ).popular()
        elif period == 'week':
            from datetime import datetime, timedelta
            date_from = datetime.now() - timedelta(days=7)
            queryset = News.objects.published().filter(
                created_at__gte=date_from
            ).popular()
        elif period == 'month':
            from datetime import datetime, timedelta
            date_from = datetime.now() - timedelta(days=30)
            queryset = News.objects.published().filter(
                created_at__gte=date_from
            ).popular()
        else:  # all
            queryset = News.objects.popular()
        
        return queryset[:limit]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return super().render_to_response(context, **response_kwargs)
        return JsonResponse({'error': 'Only AJAX requests allowed'})
```

## 4-bosqich: URL konfiguratsiyasi

```python
# urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Asosiy sahifalar
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # AJAX endpoints
    path('ajax/popular-news/', views.PopularNewsAjaxView.as_view(), name='popular_news_ajax'),
]
```

## 5-bosqich: Admin interface

```python
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_display', 'icon_display', 'is_featured', 'news_count', 'order']
    list_editable = ['is_featured', 'order']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_display(self, obj):
        return format_html(
            '<span class="badge" style="background-color: {}; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = 'Rang'
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="fas fa-{}"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = 'Icon'
    
    def news_count(self, obj):
        return obj.get_published_news_count()
    news_count.short_description = 'Yangiliklar soni'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published', 'is_featured', 'views_count', 'created_at']
    list_editable = ['published', 'is_featured']
    list_filter = ['published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    raw_id_fields = ['author']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Kontent', {
            'fields': ('summary', 'content', 'image')
        }),
        ('Sozlamalar', {
            'fields': ('published', 'is_featured'),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')
```

## 6-bosqich: Base template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{% block description %}Eng so'nggi yangiliklar va ma'lumotlar{% endblock %}">
    <title>{% block title %}Bosh sahifa{% endblock %} | Yangiliklar portali</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <style>
        .navbar-brand { font-weight: bold; }
        .hero-section { margin-bottom: 3rem; }
        .hero-section .card { border: none; border-radius: 15px; overflow: hidden; }
        .hero-section .card-img-overlay { background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0.2)); }
        .category-section { margin-bottom: 3rem; }
        .section-title { border-left: 4px solid var(--bs-primary); padding-left: 1rem; margin-bottom: 1.5rem; }
        .news-card { transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .news-card img { transition: transform 0.3s ease; }
        .news-card:hover img { transform: scale(1.05); }
        .badge-category { font-size: 0.75rem; }
        .stats-section { background: linear-gradient(135deg, var(--bs-primary), var(--bs-info)); color: white; }
        .footer { background-color: var(--bs-dark); }
        
        /* Loading spinner */
        .spinner-border-sm { width: 1rem; height: 1rem; }
        
        /* Custom scrollbar */
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: var(--bs-primary); border-radius: 3px; }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header -->
    <header>
        <!-- Top bar -->
        <div class="bg-dark text-white py-2">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <small>
                            <i class="fas fa-clock"></i>
                            <span id="current-time"></span>
                        </small>
                    </div>
                    <div class="col-md-6 text-md-end">
                        <small>
                            <a href="#" class="text-white-50 text-decoration-none me-3">
                                <i class="fab fa-telegram"></i> Telegram
                            </a>
                            <a href="#" class="text-white-50 text-decoration-none">
                                <i class="fab fa-instagram"></i> Instagram
                            </a>
                        </small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main navigation -->
        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
            <div class="container">
                <a class="navbar-brand text-primary" href="{% url 'news:home' %}">
                    <i class="fas fa-newspaper"></i> YangiliklarPortali
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'news:home' %}">
                                <i class="fas fa-home"></i> Bosh sahifa
                            </a>
                        </li>
                        
                        <!-- Kategoriyalar dropdown -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-list"></i> Kategoriyalar
                            </a>
                            <ul class="dropdown-menu">
                                {% for category in request.featured_categories %}
                                <li>
                                    <a class="dropdown-item" href="{{ category.get_absolute_url }}">
                                        {% if category.icon %}
                                            <i class="fas fa-{{ category.icon }}"></i>
                                        {% endif %}
                                        {{ category.name }}
                                    </a>
                                </li>
                                {% endfor %}
                            </ul>
                        </li>
                    </ul>
                    
                    <!-- Search form -->
                    <form class="d-flex" action="{% url 'news:search' %}" method="get">
                        <div class="input-group">
                            <input class="form-control" type="search" name="q" placeholder="Qidiruv..." 
                                   value="{{ request.GET.q }}" required>
                            <button class="btn btn-outline-primary" type="submit">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main content -->
    <main class="py-4">
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer mt-5 py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5 class="text-white">YangiliklarPortali</h5>
                    <p class="text-white-50">Eng so'nggi va ishonchli yangiliklar manbai</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="text-white-50 mb-0">
                        &copy; 2024 YangiliklarPortali. Barcha huquqlar himoyalangan.
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script>
        // Vaqtni ko'rsatish
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleString('uz-UZ', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            document.getElementById('current-time').textContent = timeString;
        }
        
        // Sahifa yuklanganda va har daqiqada yangilash
        updateTime();
        setInterval(updateTime, 60000);
        
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 7-bosqich: Bosh sahifa template

```html
<!-- templates/home.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa{% endblock %}

{% block description %}Eng so'nggi yangiliklar, sport, texnologiya, siyosat va boshqa kategoriyalardan ma'lumotlar{% endblock %}

{% block content %}
<!-- Hero Section - Asosiy yangilik -->
{% if featured_news %}
<section class="hero-section">
    <div class="card bg-dark text-white position-relative">
        {% if featured_news.image %}
        <img src="{{ featured_news.image.url }}" class="card-img" alt="{{ featured_news.title }}" 
             style="height: 500px; object-fit: cover;">
        <div class="card-img-overlay d-flex align-items-end">
        {% else %}
        <div class="card-body py-5" style="background: linear-gradient(135deg, var(--bs-primary), var(--bs-info));">
        {% endif %}
            <div class="container">
                <div class="row">
                    <div class="col-lg-8">
                        <span class="badge bg-{{ featured_news.category.color }} badge-category mb-2">
                            {% if featured_news.category.icon %}
                                <i class="fas fa-{{ featured_news.category.icon }}"></i>
                            {% endif %}
                            {{ featured_news.category.name }}
                        </span>
                        
                        <h1 class="display-4 fw-bold mb-3">{{ featured_news.title }}</h1>
                        
                        <p class="lead mb-4">{{ featured_news.get_summary|truncatechars:200 }}</p>
                        
                        <div class="d-flex align-items-center mb-3">
                            <div class="me-4">
                                <small>
                                    <i class="fas fa-user"></i>
                                    {{ featured_news.author.get_full_name|default:featured_news.author.username }}
                                </small>
                            </div>
                            <div class="me-4">
                                <small>
                                    <i class="fas fa-clock"></i>
                                    {{ featured_news.created_at|timesince }} oldin
                                </small>
                            </div>
                            {% if featured_news.views_count > 0 %}
                            <div>
                                <small>
                                    <i class="fas fa-eye"></i>
                                    {{ featured_news.views_count|floatformat:0 }} ko'rishlar
                                </small>
                            </div>
                            {% endif %}
                        </div>
                        
                        <a href="{{ featured_news.get_absolute_url }}" class="btn btn-primary btn-lg">
                            <i class="fas fa-arrow-right"></i> To'liq o'qish
                        </a>
                    </div>
                </div>
            </div>
        {% if featured_news.image %}</div>{% else %}</div>{% endif %}
    </div>
</section>
{% endif %}

<!-- Statistika -->
<section class="stats-section py-4 rounded mb-5">
    <div class="container">
        <div class="row text-center">
            <div class="col-md-4">
                <div class="d-flex align-items-center justify-content-center">
                    <i class="fas fa-newspaper fa-2x me-3"></i>
                    <div>
                        <h3 class="mb-0">{{ stats.total_news|default:0 }}</h3>
                        <small>Jami yangiliklar</small>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="d-flex align-items-center justify-content-center">
                    <i class="fas fa-list fa-2x me-3"></i>
                    <div>
                        <h3 class="mb-0">{{ stats.total_categories|default:0 }}</h3>
                        <small>Kategoriyalar</small>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="d-flex align-items-center justify-content-center">
                    <i class="fas fa-eye fa-2x me-3"></i>
                    <div>
                        <h3 class="mb-0">{{ stats.total_views|default:0|floatformat:0 }}</h3>
                        <small>Jami ko'rishlar</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Kategoriyalar bo'yicha yangiliklar -->
{% for category in categories_with_news %}
<section class="category-section">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="section-title mb-0">
            {% if category.icon %}
                <i class="fas fa-{{ category.icon }} text-{{ category.color }}"></i>
            {% endif %}
            {{ category.name }}
            <small class="text-muted ms-2">({{ category.published_count }} ta yangilik)</small>
        </h2>
        <a href="{{ category.get_absolute_url }}" class="btn btn-outline-{{ category.color }}">
            Barchasini ko'rish <i class="fas fa-arrow-right"></i>
        </a>
    </div>
    
    <div class="row g-4">
        {% for news in category.latest_news %}
        <div class="col-lg-4 col-md-6">
            <div class="card news-card h-100 border-0 shadow-sm">
                {% if news.image %}
                <div class="overflow-hidden">
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" 
                         style="height: 200px; object-fit: cover;">
                </div>
                {% endif %}
                
                <div class="card-body d-flex flex-column">
                    <span class="badge bg-{{ category.color }} badge-category mb-2 align-self-start">
                        {{ category.name }}
                    </span>
                    
                    <h5 class="card-title">
                        <a href="{{ news.get_absolute_url }}" class="text-decoration-none text-dark">
                            {{ news.title|truncatechars:70 }}
                        </a>
                    </h5>
                    
                    <p class="card-text text-muted flex-grow-1 small">
                        {{ news.get_summary|truncatechars:120 }}
                    </p>
                    
                    <div class="d-flex justify-content-between align-items-center mt-auto pt-2 border-top">
                        <small class="text-muted">
                            <i class="fas fa-user"></i> 
                            {{ news.author.get_full_name|default:news.author.username|truncatechars:20 }}
                        </small>
                        <small class="text-muted">
                            {{ news.created_at|timesince }} oldin
                        </small>
                    </div>
                    
                    {% if news.views_count > 0 %}
                    <div class="mt-1">
                        <small class="text-muted">
                            <i class="fas fa-eye"></i> {{ news.views_count }} ko'rishlar
                        </small>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i>
                {{ category.name }} kategoriyasida hozircha yangilik yo'q
            </div>
        </div>
        {% endfor %}
    </div>
</section>

{% if not forloop.last %}
<hr class="my-5">
{% endif %}
{% empty %}
<div class="alert alert-warning text-center py-5">
    <i class="fas fa-exclamation-triangle fa-3x mb-3 text-warning"></i>
    <h4>Yangilik topilmadi</h4>
    <p class="mb-0">Hozircha hech qanday yangilik nashr etilmagan.</p>
</div>
{% endfor %}

<!-- Sidebar content -->
{% if popular_news or latest_news %}
<section class="sidebar-section mt-5">
    <div class="row">
        <!-- Mashhur yangiliklar -->
        {% if popular_news %}
        <div class="col-lg-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-fire"></i> Mashhur yangiliklar
                    </h5>
                    
                    <!-- Period selection -->
                    <div class="btn-group btn-group-sm mt-2" role="group">
                        <input type="radio" class="btn-check" name="popular-period" id="popular-day" value="day">
                        <label class="btn btn-outline-light" for="popular-day">Kun</label>
                        
                        <input type="radio" class="btn-check" name="popular-period" id="popular-week" value="week" checked>
                        <label class="btn btn-outline-light" for="popular-week">Hafta</label>
                        
                        <input type="radio" class="btn-check" name="popular-period" id="popular-month" value="month">
                        <label class="btn btn-outline-light" for="popular-month">Oy</label>
                    </div>
                </div>
                <div id="popular-news-container" class="list-group list-group-flush custom-scrollbar" style="max-height: 400px; overflow-y: auto;">
                    {% for news in popular_news|slice:":5" %}
                    <a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action border-0">
                        <div class="d-flex">
                            <div class="me-3">
                                <span class="badge bg-primary rounded-pill">{{ forloop.counter }}</span>
                            </div>
                            {% if news.image %}
                            <div class="me-3">
                                <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                                     class="rounded" style="width: 50px; height: 50px; object-fit: cover;">
                            </div>
                            {% endif %}
                            <div class="flex-grow-1">
                                <h6 class="mb-1">{{ news.title|truncatechars:55 }}</h6>
                                <small class="text-muted">
                                    {{ news.category.name }} • {{ news.views_count }} ko'rishlar
                                </small>
                            </div>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Eng yangi yangiliklar -->
        {% if latest_news %}
        <div class="col-lg-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-clock"></i> Eng yangi yangiliklar
                    </h5>
                </div>
                <div class="list-group list-group-flush custom-scrollbar" style="max-height: 400px; overflow-y: auto;">
                    {% for news in latest_news|slice:":6" %}
                    <a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action border-0">
                        <div class="d-flex">
                            {% if news.image %}
                            <div class="me-3">
                                <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                                     class="rounded" style="width: 50px; height: 50px; object-fit: cover;">
                            </div>
                            {% endif %}
                            <div class="flex-grow-1">
                                <h6 class="mb-1">{{ news.title|truncatechars:55 }}</h6>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">{{ news.category.name }}</small>
                                    <small class="text-muted">{{ news.created_at|timesince }} oldin</small>
                                </div>
                            </div>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</section>
{% endif %}

<!-- Back to top button -->
<button type="button" class="btn btn-primary position-fixed bottom-0 end-0 m-4" 
        id="backToTopBtn" style="display: none; z-index: 1000;" onclick="scrollToTop()">
    <i class="fas fa-arrow-up"></i>
</button>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Back to top button
    const backToTopBtn = document.getElementById('backToTopBtn');
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 100) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    // Popular news period change
    const periodRadios = document.querySelectorAll('input[name="popular-period"]');
    const popularContainer = document.getElementById('popular-news-container');
    
    periodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                loadPopularNews(this.value);
            }
        });
    });
    
    function loadPopularNews(period) {
        // Loading spinner ko'rsatish
        popularContainer.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"></div></div>';
        
        // AJAX so'rov
        fetch(`{% url 'news:popular_news_ajax' %}?period=${period}&limit=5`)
            .then(response => response.text())
            .then(html => {
                popularContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                popularContainer.innerHTML = '<div class="alert alert-danger m-3">Xatolik yuz berdi</div>';
            });
    }
    
    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Smooth card animations
    const cards = document.querySelectorAll('.news-card');
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        cardObserver.observe(card);
    });
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Live time update
function updateLiveTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('uz-UZ', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    const timeElements = document.querySelectorAll('.live-time');
    timeElements.forEach(el => {
        el.textContent = timeString;
    });
}

// Update time every second
setInterval(updateLiveTime, 1000);
</script>
{% endblock %}
```

## 8-bosqich: Include template'lar

```html
<!-- templates/includes/news_card.html -->
<div class="card news-card h-100 border-0 shadow-sm">
    {% if news.image %}
    <div class="overflow-hidden">
        <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" 
             style="height: 200px; object-fit: cover;" loading="lazy">
    </div>
    {% endif %}
    
    <div class="card-body d-flex flex-column">
        <span class="badge bg-{{ news.category.color }} badge-category mb-2 align-self-start">
            {% if news.category.icon %}
                <i class="fas fa-{{ news.category.icon }}"></i>
            {% endif %}
            {{ news.category.name }}
        </span>
        
        <h5 class="card-title">
            <a href="{{ news.get_absolute_url }}" class="text-decoration-none text-dark">
                {{ news.title|truncatechars:70 }}
            </a>
        </h5>
        
        <p class="card-text text-muted flex-grow-1 small">
            {{ news.get_summary|truncatechars:120 }}
        </p>
        
        <div class="card-footer bg-transparent px-0 border-0 mt-auto">
            <div class="d-flex justify-content-between align-items-center text-muted small">
                <span>
                    <i class="fas fa-user"></i> 
                    {{ news.author.get_full_name|default:news.author.username|truncatechars:20 }}
                </span>
                <span>
                    <i class="fas fa-clock"></i>
                    {{ news.created_at|timesince }} oldin
                </span>
            </div>
            
            {% if news.views_count > 0 %}
            <div class="mt-1">
                <small class="text-muted">
                    <i class="fas fa-eye"></i> {{ news.views_count|floatformat:0 }} ko'rishlar
                </small>
            </div>
            {% endif %}
        </div>
    </div>
</div>

<!-- templates/includes/popular_news_list.html -->
{% for news in news_list %}
<a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action border-0">
    <div class="d-flex">
        <div class="me-3">
            <span class="badge bg-primary rounded-pill">{{ forloop.counter }}</span>
        </div>
        {% if news.image %}
        <div class="me-3">
            <img src="{{ news.image.url }}" alt="{{ news.title }}" 
                 class="rounded" style="width: 50px; height: 50px; object-fit: cover;">
        </div>
        {% endif %}
        <div class="flex-grow-1">
            <h6 class="mb-1">{{ news.title|truncatechars:55 }}</h6>
            <small class="text-muted">
                {{ news.category.name }} • 
                <i class="fas fa-eye"></i> {{ news.views_count|floatformat:0 }} • 
                {{ news.created_at|timesince }} oldin
            </small>
        </div>
    </div>
</a>
{% empty %}
<div class="list-group-item text-center text-muted">
    <i class="fas fa-info-circle"></i>
    Bu davrda mashhur yangilik yo'q
</div>
{% endfor %}
```

## 9-bosqich: Management commands

```python
# management/commands/generate_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from news.models import Category, News
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Sample data yaratish'
    
    def add_arguments(self, parser):
        parser.add_argument('--categories', type=int, default=6)
        parser.add_argument('--news', type=int, default=50)
    
    def handle(self, *args, **options):
        # Admin user yaratish
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Admin user yaratildi: admin/admin123')
        
        # Kategoriyalar yaratish
        categories_data = [
            {'name': 'Texnologiya', 'icon': 'laptop', 'color': 'primary'},
            {'name': 'Sport', 'icon': 'futbol', 'color': 'success'},
            {'name': 'Siyosat', 'icon': 'landmark', 'color': 'danger'},
            {'name': 'Iqtisod', 'icon': 'chart-line', 'color': 'warning'},
            {'name': 'Madaniyat', 'icon': 'theater-masks', 'color': 'info'},
            {'name': 'Ilm-fan', 'icon': 'microscope', 'color': 'secondary'},
        ]
        
        for cat_data in categories_data[:options['categories']]:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_featured': True,
                    'order': random.randint(1, 10)
                }
            )
            if created:
                self.stdout.write(f'Kategoriya yaratildi: {category.name}')
        
        # Yangiliklar yaratish
        admin_user = User.objects.get(username='admin')
        categories = list(Category.objects.all())
        
        for i in range(options['news']):
            title = f"Yangilik #{i+1}: {random.choice(['Yangi', 'So\'nggi', 'Muhim'])} voqea"
            
            news = News.objects.create(
                title=title,
                content=f"Bu {title} haqida batafsil ma'lumot. " * random.randint(10, 50),
                summary=f"Bu {title} qisqacha mazmuni.",
                author=admin_user,
                category=random.choice(categories),
                published=True,
                is_featured=(i == 0),  # Birinchi yangilik featured
                views_count=random.randint(10, 1000)
            )
            
            if i % 10 == 0:
                self.stdout.write(f'{i+1} ta yangilik yaratildi...')
        
        self.stdout.write(
            self.style.SUCCESS(f'Jami {options["news"]} ta yangilik yaratildi!')
        )
```

## Topshiriqlar

### 1. Asosiy topshiriq
Bosh sahifaga quyidagilarni qo'shing:
- Weather widget (havo ma'lumotlari)
- Currency rates (valyuta kurslari)
- Breaking news ticker (tezkor yangiliklar)

### 2. Qo'shimcha topshiriq
- Infinite scroll qo'shing
- Dark mode toggle yarating
- Social media sharing buttons

### 3. Murakkab topshiriq
- Redis bilan caching amalga oshiring
- Elasticsearch bilan qidiruv tizimi
- WebSocket bilan real-time yangiliklar

## Best Practices

1. **Database optimallashtirish:**
   ```python
   # select_related va prefetch_related dan foydalaning
   News.objects.select_related('category', 'author').prefetch_related('tags')
   ```

2. **Caching strategiyasi:**
   ```python
   # View-level caching
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 15)  # 15 daqiqa
   def home_view(request):
       pass
   ```

3. **Image optimization:**
   ```python
   # Pillow bilan image processing
   from PIL import Image
   
   def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       if self.image:
           img = Image.open(self.image.path)
           if img.width > 800:
               img.thumbnail((800, 600))
               img.save(self.image.path)
   ```

4. **SEO optimization:**
   ```html
   <!-- Meta tags -->
   <meta name="description" content="{{ news.get_summary }}">
   <meta property="og:title" content="{{ news.title }}">
   <meta property="og:description" content="{{ news.get_summary }}">
   <meta property="og:image" content="{{ news.image.url }}">
   ```

## Xulosa

Bu amaliyotda siz o'rgandingiz:

1. **Complex queryset'lar** - Prefetch va select_related
2. **Custom manager'lar** - kod qayta ishlatish
3. **Template optimization** - chiroyli va tez yuklash
4. **Caching strategiyasi** - performance yaxshilash
5. **AJAX integration** - dinamik kontent
6. **Responsive design** - mobile-first yondashuv

Keyingi darsda Context manager va get_context_data metodlarini chuqurroq o'rganamiz va 2-qismda performance'ni yanada yaxshilaymiz.