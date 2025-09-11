# Practice 23: Context manager bilan bosh sahifa yaratish - Amaliyot

## Amaliy mashqlar

### Mashq 1: Asosiy Context Manager yaratish

**Maqsad**: Bosh sahifa uchun asosiy context manager yaratish

**Bosqichma-bosqich:**

1. **Views.py faylini yangilash:**
```python
# news/views.py
from django.views.generic import ListView
from .models import News, Category
from django.db.models import Count, Q

class HomeView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_queryset(self):
        """Faqat published yangiliklarni qaytarish"""
        return News.published.all().select_related('category', 'author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Kategoriyalar ro'yxati
        context['categories'] = Category.objects.annotate(
            news_count=Count('news', filter=Q(news__status='published'))
        )
        
        # 2. So'nggi 5 ta yangilik
        context['recent_news'] = News.published.all()[:5]
        
        return context
```

2. **Template yaratish:**
```html
<!-- news/templates/news/index.html -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <h2>So'nggi yangilikar</h2>
            {% for news_item in news %}
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="{{ news_item.get_absolute_url }}">{{ news_item.title }}</a>
                        </h5>
                        <p class="card-text">{{ news_item.body|truncatewords:25 }}</p>
                        <small class="text-muted">
                            {{ news_item.category.name }} | {{ news_item.publish|date:"d.m.Y" }}
                        </small>
                    </div>
                </div>
            {% endfor %}
        </div>
        
        <div class="col-md-4">
            <h4>Kategoriyalar</h4>
            <ul class="list-group">
                {% for category in categories %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        {{ category.name }}
                        <span class="badge badge-primary badge-pill">{{ category.news_count }}</span>
                    </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}
```

3. **URL sozlash:**
```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
```

### Mashq 2: Featured yangiliklarni qo'shish

**Maqsad**: Bosh sahifada featured yangiliklarni ko'rsatish

**Bosqichlar:**

1. **Model'ga featured maydon qo'shish:**
```python
# news/models.py
class News(models.Model):
    # ... mavjud maydonlar
    featured = models.BooleanField(default=False, verbose_name="Tanlangan")
    
    class Meta:
        ordering = ('-publish',)
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangilikar"
```

2. **Migration yaratish va bajarish:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Views.py'ni kengaytirish:**
```python
# news/views.py (kengaytirish)
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Featured yangilikar
    context['featured_news'] = News.published.filter(featured=True)[:3]
    
    # Kategoriyalar
    context['categories'] = Category.objects.annotate(
        news_count=Count('news', filter=Q(news__status='published'))
    )
    
    # Eng mashhur yangilikar
    context['popular_news'] = News.published.order_by('-views')[:5]
    
    return context
```

4. **Template'ni yangilash:**
```html
<!-- Template'ga featured section qo'shish -->
{% if featured_news %}
<div class="featured-section mb-4">
    <h3>Tanlangan yangilikar</h3>
    <div class="row">
        {% for news in featured_news %}
        <div class="col-md-4">
            <div class="card">
                {% if news.image %}
                    <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}">
                {% endif %}
                <div class="card-body">
                    <h6 class="card-title">
                        <a href="{{ news.get_absolute_url }}">{{ news.title|truncatechars:40 }}</a>
                    </h6>
                    <small class="text-muted">{{ news.publish|date:"d.m.Y" }}</small>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}
```

### Mashq 3: Cache sistemasini qo'shish

**Maqsad**: Performance yaxshilash uchun cache ishlatish

**Bosqichlar:**

1. **Settings.py'da cache sozlash:**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 daqiqa
    }
}
```

2. **Views'da cache qo'llash:**
```python
# news/views.py
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class HomeView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cache'dan ma'lumot olish
        sidebar_data = cache.get('sidebar_data')
        
        if not sidebar_data:
            sidebar_data = {
                'categories': Category.objects.annotate(
                    news_count=Count('news', filter=Q(news__status='published'))
                ),
                'popular_news': News.published.order_by('-views')[:5],
                'featured_news': News.published.filter(featured=True)[:3],
            }
            # 15 daqiqa cache'lash
            cache.set('sidebar_data', sidebar_data, 60*15)
        
        context.update(sidebar_data)
        return context
```

3. **Cache'ni tozalash funksiyasini yaratish:**
```python
# news/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import News, Category

@receiver([post_save, post_delete], sender=News)
@receiver([post_save, post_delete], sender=Category)
def clear_cache(sender, **kwargs):
    """Yangilik yoki kategoriya o'zgarganda cache'ni tozalash"""
    cache.delete('sidebar_data')
```

### Mashq 4: Statistika ko'rsatish

**Maqsad**: Sayt statistikasini ko'rsatish

**Bosqichlar:**

1. **Statistics metodini yaratish:**
```python
# news/views.py
from django.utils import timezone
from datetime import timedelta

def get_site_statistics(self):
    """Sayt statistikasi"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    return {
        'total_news': News.objects.count(),
        'published_news': News.published.count(),
        'weekly_news': News.published.filter(
            publish__date__gte=week_ago
        ).count(),
        'monthly_news': News.published.filter(
            publish__date__gte=month_ago
        ).count(),
        'total_categories': Category.objects.count(),
    }

# get_context_data metodiga qo'shish
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # ... mavjud kodlar
    context['stats'] = self.get_site_statistics()
    
    return context
```

2. **Template'da statistikani ko'rsatish:**
```html
<!-- Sidebar'ga qo'shish -->
{% if stats %}
<div class="card mb-4">
    <div class="card-header">
        <h5>Sayt statistikasi</h5>
    </div>
    <div class="card-body">
        <ul class="list-unstyled">
            <li><strong>Jami yangilikar:</strong> {{ stats.total_news }}</li>
            <li><strong>Nashr etilgan:</strong> {{ stats.published_news }}</li>
            <li><strong>Bu hafta:</strong> {{ stats.weekly_news }}</li>
            <li><strong>Bu oy:</strong> {{ stats.monthly_news }}</li>
            <li><strong>Kategoriyalar:</strong> {{ stats.total_categories }}</li>
        </ul>
    </div>
</div>
{% endif %}
```

### Mashq 5: Qidiruv funksiyasini qo'shish

**Maqsad**: Bosh sahifada qidiruv imkoniyatini yaratish

**Bosqichlar:**

1. **Search mixin yaratish:**
```python
# news/mixins.py
from django.db.models import Q

class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(body__icontains=query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
```

2. **HomeView'ga mixin qo'shish:**
```python
# news/views.py
from .mixins import SearchMixin

class HomeView(SearchMixin, ListView):
    # ... mavjud kodlar
```

3. **Qidiruv formasi:**
```html
<!-- Template'da qidiruv formasi -->
<div class="search-section mb-4">
    <form method="get" class="form-inline justify-content-center">
        <input type="text" name="q" value="{{ query }}" 
               class="form-control mr-2" placeholder="Yangiliklarni qidiring...">
        <button type="submit" class="btn btn-primary">Qidirish</button>
    </form>
    {% if query %}
        <p class="mt-2">Qidiruv natijalari: "{{ query }}"</p>
    {% endif %}
</div>
```

## Test qilish

Har bir mashqni bajargandan so'ng quyidagilarni tekshiring:

### 1. Funktsionallik testi
```bash
# Server ishga tushirish
python manage.py runserver

# Browser'da tekshirish:
# - http://127.0.0.1:8000/ - bosh sahifa
# - Featured yangilikar ko'rinishi
# - Kategoriyalar ro'yxati
# - Statistika ma'lumotlari
# - Qidiruv funksiyasi
```

### 2. Debug rejimda tekshirish
```python
# settings.py'da
DEBUG = True

# Django Debug Toolbar o'rnatish (ixtiyoriy)
pip install django-debug-toolbar
```

### 3. Database so'rovlarini tekshirish
```python
# views.py'ga debug qo'shish
import logging
logger = logging.getLogger(__name__)

def get_context_data(self, **kwargs):
    from django.db import connection
    
    context = super().get_context_data(**kwargs)
    
    # Database so'rovlar sonini tekshirish
    queries_count = len(connection.queries)
    logger.info(f"Database queries count: {queries_count}")
    
    return context
```

## Muammolarni hal qilish

### Keng uchraydigan xatoliklar va yechimlar:

#### 1. Template Not Found
```python
# Sabab: Template yo'li noto'g'ri
# Yechim: settings.py'da TEMPLATES sozlamalarini tekshirish

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        # ...
    },
]
```

#### 2. Context variable ishlamayapti
```python
# Template'da debug qilish
{% load static %}
{% comment %}
Debug uchun context'ni ko'rish:
{{ categories|length }} - kategoriyalar soni
{{ featured_news|length }} - featured yangilikar soni
{% endcomment %}

<!-- Mavjudligini tekshirish -->
{% if categories %}
    <p>Kategoriyalar mavjud</p>
{% else %}
    <p>Kategoriyalar topilmadi</p>
{% endif %}
```

#### 3. Performance muammolari
```python
# N+1 problem hal qilish
def get_queryset(self):
    return News.published.select_related(
        'category', 'author'
    ).prefetch_related('tags')

# Cache ishlatish
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(ListView):
    # ...
```

## Kengaytirish imkoniyatlari

### 1. Ajax bilan dynamic content
```javascript
// static/js/home.js
function loadMoreNews(page) {
    fetch(`/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            // Content'ni yangilash
            document.getElementById('news-container').innerHTML += data.html;
        });
}
```

### 2. Real-time updates
```python
# WebSocket yoki SSE (Server-Sent Events) ishlatish
# channels kutubxonasi bilan
pip install channels
```

### 3. API endpoint yaratish
```python
# news/api_views.py
from django.http import JsonResponse
from django.core.serializers import serialize

class HomeAPIView(HomeView):
    def get(self, request, *args, **kwargs):
        if request.headers.get('Accept') == 'application/json':
            context = self.get_context_data()
            
            data = {
                'news': [
                    {
                        'title': news.title,
                        'url': news.get_absolute_url(),
                        'publish': news.publish.isoformat(),
                    }
                    for news in context['news']
                ],
                'categories': [
                    {
                        'name': cat.name,
                        'count': cat.news_count
                    }
                    for cat in context['categories']
                ]
            }
            
            return JsonResponse(data)
        
        return super().get(request, *args, **kwargs)
```

## Vazifalar

### Asosiy vazifa (5 ball)
1. Context manager yaratish
2. Featured yangiliklarni qo'shish
3. Basic template yaratish
4. Kategoriyalar ro'yxatini ko'rsatish

### Qo'shimcha vazifa (3 ball)
1. Cache sistemasini qo'llash
2. Statistika ko'rsatish
3. Qidiruv funksiyasini qo'shish

### Mukammal vazifa (2 ball)
1. Performance optimizatsiya
2. Ajax funksiyalarni qo'shish
3. API endpoint yaratish
4. Unit testlar yozish

## Unit testlar yozish

```python
# news/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import News, Category

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(name='Test Category')
        
        # Test news yaratish
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            author=self.user,
            body='Test body content',
            status='published',
            category=self.category,
            featured=True
        )
    
    def test_home_view_status_code(self):
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_context_data(self):
        response = self.client.get(reverse('news:home'))
        
        # Context'da kerakli ma'lumotlar borligini tekshirish
        self.assertContains(response, 'Test News')
        self.assertIn('categories', response.context)
        self.assertIn('featured_news', response.context)
    
    def test_featured_news_display(self):
        response = self.client.get(reverse('news:home'))
        featured_news = response.context['featured_news']
        
        self.assertEqual(len(featured_news), 1)
        self.assertEqual(featured_news[0].title, 'Test News')
    
    def test_search_functionality(self):
        response = self.client.get(reverse('news:home'), {'q': 'Test'})
        self.assertContains(response, 'Test News')
        
        response = self.client.get(reverse('news:home'), {'q': 'NonExistent'})
        self.assertNotContains(response, 'Test News')
```

## Performance monitoring

```python
# news/middleware.py
import time
import logging

logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        if duration > 1.0:  # 1 soniyadan ko'p
            logger.warning(
                f"Slow request: {request.path} took {duration:.2f}s"
            )
        
        return response
```

## Best Practices

### 1. Kod tashkiloti
- Har bir metod bitta vazifani bajarishi kerak
- Nomlarni tushunarli qo'yish
- Docstring yozish

### 2. Database optimizatsiya
- `select_related()` va `prefetch_related()` ishlatish
- Index'lar qo'yish
- Database connection pool ishlatish

### 3. Security
```python
# XSS'dan himoyalanish
from django.utils.html import escape

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # User input'ini escape qilish
    query = self.request.GET.get('q', '')
    context['query'] = escape(query)
    
    return context
```

### 4. Error handling
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    try:
        context['featured_news'] = News.published.filter(featured=True)[:3]
    except Exception as e:
        logger.error(f"Featured news error: {e}")
        context['featured_news'] = []
    
    return context
```

## Xulosa

Ushbu amaliy darsda siz quyidagilarni o'rgandingiz:

1. **Context manager** yaratish va ishlatish
2. **Featured content** tizimini qo'llash  
3. **Cache** sistemasi bilan ishlash
4. **Performance** optimizatsiya usullari
5. **Testing** va **debugging** texnikalari

Endi siz professional darajada Django bosh sahifasini yarata olasiz va uni samarali boshqara olasiz.

## Keyingi qadamlar

- Context processors bilan ishlashni o'rganing
- Template tags yaratishni o'rganing
- SEO optimizatsiya qilishni o'rganing
- Performance monitoring qo'shishni o'rganing