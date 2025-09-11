# Lesson 23: Bosh sahifani o'zgartirish. Context managerlar bilan ishlash. 2-qism

## Maqsad
Ushbu darsda biz bosh sahifamizni yanada professional ko'rinishga keltirish uchun context managerlar bilan chuqurroq ishlashni o'rganamiz. Birinchi qismda o'rgangan asoslarimizni rivojlantirib, murakkab ma'lumotlar tuzilmalarini yaratish va ularni template'larga uzatish usullarini o'rganamiz.

## Nazariy qism

### Context Manager nima?
Context manager - bu Django view'larda template'ga uzatiladigan ma'lumotlarni boshqarish uchun ishlatiladigan mexanizm. U orqali biz bir necha modeldan ma'lumotlarni yig'ib, ularni template'da ishlatish uchun tayyorlaymiz.

### Context Manager'ning afzalliklari:
- **Kod tashkiloti**: Ma'lumotlarni bir joyda boshqarish
- **Qayta ishlatish**: Bir marta yozilgan kod bir necha joyda ishlatilishi
- **Samaradorlik**: Database so'rovlarini optimallashtirish
- **Tushunarlilik**: Kodning oson o'qilishi

## Amaliy qism

### 1-bosqich: Context Manager metodini yaratish

Avval `views.py` faylimizda Home sahifasi uchun context manager yaratamiz:

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import News, Category
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class HomeView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 5
    
    def get_queryset(self):
        """Faqat published bo'lgan yangiliklarni qaytaradi"""
        return News.published.all().select_related('category', 'author')
    
    def get_context_data(self, **kwargs):
        """Context ma'lumotlarini yaratish"""
        context = super().get_context_data(**kwargs)
        
        # Kategoriyalar va ularning yangiliklar soni
        context['categories'] = self.get_categories_with_count()
        
        # So'nggi yangiliklarni olish
        context['recent_news'] = self.get_recent_news()
        
        # Eng ko'p o'qilgan yangiliklarni olish
        context['popular_news'] = self.get_popular_news()
        
        # Bu hafta qo'shilgan yangiliklarni olish
        context['weekly_news'] = self.get_weekly_news()
        
        return context
    
    def get_categories_with_count(self):
        """Har bir kategoriyada nechta yangilik borligini hisoblash"""
        return Category.objects.annotate(
            news_count=Count('news', filter=Q(news__status='published'))
        ).filter(news_count__gt=0)
    
    def get_recent_news(self, limit=5):
        """Eng so'nggi yangiliklarni olish"""
        return News.published.all()[:limit]
    
    def get_popular_news(self, limit=5):
        """Eng ko'p o'qilgan yangiliklarni olish"""
        return News.published.order_by('-views')[:limit]
    
    def get_weekly_news(self):
        """Bu hafta qo'shilgan yangiliklarni olish"""
        week_ago = timezone.now() - timedelta(days=7)
        return News.published.filter(created_date__gte=week_ago)
```

### 2-bosqich: Context Manager'ni to'liq ishlatish

Endi context manager'ni yanada kengaytiramiz:

```python
# news/views.py (davomi)
from django.core.cache import cache
from collections import defaultdict

class HomeView(ListView):
    # ... oldingi kodlar
    
    def get_context_data(self, **kwargs):
        """Kengaytirilgan context ma'lumotlari"""
        context = super().get_context_data(**kwargs)
        
        # Cache'dan ma'lumotlarni olishga harakat qilish
        cached_data = cache.get('home_page_data')
        
        if cached_data:
            context.update(cached_data)
        else:
            # Yangi ma'lumotlarni yaratish
            context_data = {
                'categories': self.get_categories_with_count(),
                'recent_news': self.get_recent_news(),
                'popular_news': self.get_popular_news(),
                'weekly_news': self.get_weekly_news(),
                'stats': self.get_site_statistics(),
                'featured_news': self.get_featured_news(),
            }
            
            # Cache'ga saqlash (15 daqiqa)
            cache.set('home_page_data', context_data, 60*15)
            context.update(context_data)
        
        return context
    
    def get_site_statistics(self):
        """Sayt statistikasi"""
        return {
            'total_news': News.objects.count(),
            'published_news': News.published.count(),
            'total_categories': Category.objects.count(),
            'this_month_news': News.published.filter(
                created_date__month=timezone.now().month
            ).count()
        }
    
    def get_featured_news(self, limit=3):
        """Tanlangan (featured) yangiliklarni olish"""
        return News.published.filter(featured=True)[:limit]
    
    def get_news_by_category(self):
        """Kategoriya bo'yicha yangiliklarni guruhlash"""
        categories = Category.objects.prefetch_related('news')
        news_by_category = defaultdict(list)
        
        for category in categories:
            published_news = category.news.filter(status='published')[:3]
            if published_news:
                news_by_category[category] = list(published_news)
        
        return dict(news_by_category)
```

### 3-bosqich: Models.py'ni yangilash

Featured yangiliklarni qo'llab-quvvatlash uchun modelimizni yangilaymiz:

```python
# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='news/%Y/%m/%d/')
    publish = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)  # Yangi maydon
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
```

### 4-bosqich: Template'ni yangilash

Endi index.html template'ni yangilaymiz:

```html
<!-- news/templates/news/index.html -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <!-- Asosiy kontent -->
        <div class="col-lg-8">
            <!-- Featured yangiliklarni ko'rsatish -->
            {% if featured_news %}
            <div class="featured-news mb-4">
                <h3 class="mb-3">Tanlangan yangilikar</h3>
                <div class="row">
                    {% for news in featured_news %}
                    <div class="col-md-4">
                        <div class="card mb-3">
                            {% if news.image %}
                                <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}">
                            {% endif %}
                            <div class="card-body">
                                <h6 class="card-title">
                                    <a href="{{ news.get_absolute_url }}">{{ news.title|truncatechars:50 }}</a>
                                </h6>
                                <small class="text-muted">{{ news.publish|date:"d.m.Y" }}</small>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Asosiy yangiliklarni ko'rsatish -->
            <h3>So'nggi yangilikar</h3>
            {% for news_item in news %}
                <div class="card mb-4">
                    <div class="row no-gutters">
                        {% if news_item.image %}
                        <div class="col-md-4">
                            <img src="{{ news_item.image.url }}" class="card-img" alt="{{ news_item.title }}">
                        </div>
                        {% endif %}
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">
                                    <a href="{{ news_item.get_absolute_url }}">{{ news_item.title }}</a>
                                </h5>
                                <p class="card-text">{{ news_item.body|truncatewords:30 }}</p>
                                <p class="card-text">
                                    <small class="text-muted">
                                        {{ news_item.author.username }} | {{ news_item.publish|date:"d.m.Y" }} | 
                                        <i class="fa fa-eye"></i> {{ news_item.views }}
                                    </small>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
            
            <!-- Pagination -->
            {% if is_paginated %}
                <nav aria-label="Page navigation">
                    <ul class="pagination justify-content-center">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">&laquo; Oldingi</a>
                            </li>
                        {% endif %}
                        
                        <li class="page-item active">
                            <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
                        </li>
                        
                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi &raquo;</a>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
        
        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Kategoriyalar -->
            <div class="card mb-4">
                <div class="card-header">Kategoriyalar</div>
                <div class="list-group list-group-flush">
                    {% for category in categories %}
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            {{ category.name }}
                            <span class="badge badge-primary badge-pill">{{ category.news_count }}</span>
                        </a>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Mashhur yangilikar -->
            {% if popular_news %}
            <div class="card mb-4">
                <div class="card-header">Eng ko'p o'qilgan</div>
                <div class="list-group list-group-flush">
                    {% for news in popular_news %}
                        <a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action">
                            <h6 class="mb-1">{{ news.title|truncatechars:40 }}</h6>
                            <small class="text-muted">
                                <i class="fa fa-eye"></i> {{ news.views }} | {{ news.publish|date:"d.m.Y" }}
                            </small>
                        </a>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Sayt statistikasi -->
            {% if stats %}
            <div class="card mb-4">
                <div class="card-header">Statistika</div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li><strong>Jami yangilikar:</strong> {{ stats.total_news }}</li>
                        <li><strong>Nashr etilgan:</strong> {{ stats.published_news }}</li>
                        <li><strong>Kategoriyalar:</strong> {{ stats.total_categories }}</li>
                        <li><strong>Bu oy:</strong> {{ stats.this_month_news }}</li>
                    </ul>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### 5-bosqich: URL va Migration

URLs.py faylini yangilaymiz:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]
```

Featured maydon uchun migration yaratish:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6-bosqich: Admin panelni yangilash

Featured yangiliklarni admin panelda boshqarish:

```python
# news/admin.py
from django.contrib import admin
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'featured', 'publish']
    list_filter = ['status', 'featured', 'category', 'publish']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured']
    ordering = ['-publish']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Kontent', {
            'fields': ('body', 'image')
        }),
        ('Sozlamalar', {
            'fields': ('status', 'featured'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']
    search_fields = ['name']
```

## Xatoliklarni hal qilish

### Keng uchraydigan xatoliklar:

1. **Template not found**: Template yo'llarini to'g'ri belgilanganini tekshiring
2. **Context key error**: Template'da context kalitlarini to'g'ri ishlatganingizni tekshiring
3. **Database query error**: Model maydonlarining mavjudligini tekshiring

### Debug uchun maslahatlar:

```python
# Debug uchun context'ni tekshirish
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Context ma'lumotlarini ko'rish uchun
    print("Context keys:", context.keys())
    return context
```

## Best Practice va Tavsiyalar

### 1. Performance Optimization
- **Select_related** va **prefetch_related** ishlatish
- Cache'dan foydalanish
- Database so'rovlar sonini kamaytirish

### 2. Code Organization
- Context metodlarini alohida yozish
- Naming convention'ga amal qilish
- Dokumentatsiya yozish

### 3. Security
- User ma'lumotlarini filterlash
- XSS'dan himoyalanish
- CSRF token ishlatish

### 4. Cache Strategiyasi
```python
# Cache kalitlarini to'g'ri nomlash
CACHE_KEYS = {
    'HOME_DATA': 'home_page_data',
    'CATEGORIES': 'categories_list',
    'POPULAR_NEWS': 'popular_news_list'
}

# Cache timeout'larni belgilash
CACHE_TIMEOUTS = {
    'SHORT': 60 * 5,   # 5 daqiqa
    'MEDIUM': 60 * 15, # 15 daqiqa
    'LONG': 60 * 60    # 1 soat
}
```

## Xulosa

Ushbu darsda biz context manager'lar yordamida bosh sahifani professional darajaga keltirdik. Biz o'rganganlar:

- Context manager metodlarini yaratish
- Ma'lumotlarni cache'lash
- Template'larda murakkab ma'lumotlar bilan ishlash
- Database so'rovlarini optimallashtirishCustom manager va QuerySet'lar yaratish

**Keyingi darsda:**
Keyingi darsda biz context_processor va template tag'lari bilan ishlashni o'rganamiz.

## Qo'shimcha materiallar

- Django QuerySet API
- Template Context Processors
- Caching framework
- Performance optimization