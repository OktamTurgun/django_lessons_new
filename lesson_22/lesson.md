# Dars 22: Bosh sahifada yangiliklarni kategoriya bo'yicha ko'rsatish (1-qism)

## Dars maqsadi
Bu darsda siz bosh sahifada yangiliklarni kategoriyalar bo'yicha guruhlab ko'rsatishning turli usullarini o'rganasiz. QuerySet'lar, annotate(), prefetch_related() kabi Django ORM'ning kuchli imkoniyatlaridan foydalanishni o'rganasiz.

## Nazariy qism

### 1. Kategoriya bo'yicha guruhlash muammosi

Odatda yangilik saytlarining bosh sahifasida yangiliklarni kategoriyalar bo'yicha ko'rsatish kerak bo'ladi:

```
TEXNOLOGIYA kategoriyasi:
- Yangilik 1
- Yangilik 2
- Yangilik 3

SPORT kategoriyasi:
- Yangilik 4
- Yangilik 5

SIYOSAT kategoriyasi:
- Yangilik 6
- Yangilik 7
- Yangilik 8
```

Buni amalga oshirishning bir nechta usullari mavjud:

### 2. Usul 1: Template'da guruhlash (yomon usul)

```python
# views.py (noto'g'ri usul)
class HomeView(ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        return News.objects.filter(published=True).select_related('category')
```

```html
<!-- Template'da guruhlash (noto'g'ri) -->
{% regroup news_list by category as grouped_news %}
{% for group in grouped_news %}
    <h3>{{ group.grouper.name }}</h3>
    {% for news in group.list %}
        <div>{{ news.title }}</div>
    {% endfor %}
{% endfor %}
```

**Nima uchun yomon:**
- Template mantiqiy ishlarni bajarmasligi kerak
- Ma'lumotlar tartibi buzilishi mumkin
- Performance muammosi

### 3. Usul 2: View'da guruhlash (yaxshi usul)

```python
# views.py (to'g'ri usul)
from django.db.models import Prefetch
from collections import defaultdict

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategoriyalar bo'yicha guruhlangan yangiliklar
        context['categorized_news'] = self.get_categorized_news()
        
        return context
    
    def get_categorized_news(self):
        """Kategoriyalar bo'yicha yangiliklarni guruhlash"""
        categorized = defaultdict(list)
        
        # Barcha yangiliklar kategoriya bilan
        news_list = News.objects.filter(published=True)\
            .select_related('category', 'author')\
            .order_by('category__name', '-created_at')
        
        # Kategoriyalar bo'yicha guruhlash
        for news in news_list:
            categorized[news.category].append(news)
        
        return dict(categorized)
```

### 4. Usul 3: Prefetch bilan optimallashtirish (eng yaxshi)

```python
# views.py (optimal usul)
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategoriyalar bilan ularning yangiliklarini olish
        categories_with_news = Category.objects.prefetch_related(
            Prefetch(
                'news_set',
                queryset=News.objects.filter(published=True)\
                    .select_related('author')\
                    .order_by('-created_at')[:5],  # Har kategoriyadan 5 ta
                to_attr='latest_news'
            )
        ).filter(
            news__published=True  # Faqat yangiliği bor kategoriyalar
        ).distinct()
        
        context['categories'] = categories_with_news
        
        return context
```

## Django ORM: Prefetch va Annotate

### 1. Prefetch nima?

Prefetch - bog'langan obyektlarni oldindan yuklash usuli. N+1 query muammosini hal qiladi.

```python
# N+1 muammo (yomon)
categories = Category.objects.all()
for category in categories:
    print(category.news_set.count())  # Har safar yangi query

# Prefetch bilan hal (yaxshi)
categories = Category.objects.prefetch_related('news_set')
for category in categories:
    print(category.news_set.count())  # Bitta query'da hammasi
```

### 2. Custom Prefetch

```python
# Maxsus Prefetch
from django.db.models import Prefetch

categories = Category.objects.prefetch_related(
    Prefetch(
        'news_set',                    # Bog'lanish nomi
        queryset=News.objects.filter(  # Custom QuerySet
            published=True
        ).select_related('author').order_by('-created_at'),
        to_attr='published_news'       # Custom atribut nomi
    )
)

# Ishlatish
for category in categories:
    for news in category.published_news:  # to_attr ishlatildi
        print(news.title)
```

### 3. Annotate bilan hisoblash

```python
from django.db.models import Count

# Har kategoriyada nechta yangilik borligini hisoblash
categories = Category.objects.annotate(
    news_count=Count('news', filter=models.Q(news__published=True))
).filter(news_count__gt=0)

# Template'da ishlatish
for category in categories:
    print(f"{category.name}: {category.news_count} ta yangilik")
```

## Amaliy misollar

### 1. Asosiy model strukturasi

```python
# models.py
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Rang kodi
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon
    is_featured = models.BooleanField(default=False)  # Asosiy kategoriya
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_published_news_count(self):
        """Nashr etilgan yangiliklar soni"""
        return self.news_set.filter(published=True).count()

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    summary = models.TextField(max_length=300, blank=True)  # Qisqacha
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/%Y/%m/', blank=True)
    published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)  # Asosiy yangilik
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_summary(self):
        """Qisqacha matn yaratish"""
        if self.summary:
            return self.summary
        return self.content[:200] + '...' if len(self.content) > 200 else self.content
```

### 2. Manager va QuerySet'lar

```python
# managers.py
from django.db import models

class NewsQuerySet(models.QuerySet):
    def published(self):
        """Nashr etilgan yangiliklar"""
        return self.filter(published=True)
    
    def featured(self):
        """Asosiy yangiliklar"""
        return self.filter(is_featured=True)
    
    def by_category(self, category):
        """Kategoriya bo'yicha"""
        return self.filter(category=category)
    
    def with_relations(self):
        """Bog'langan obyektlar bilan"""
        return self.select_related('category', 'author')
    
    def latest_first(self):
        """Eng yangilar birinchi"""
        return self.order_by('-created_at')

class NewsManager(models.Manager):
    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured(self):
        return self.get_queryset().published().featured()
    
    def by_category(self, category):
        return self.get_queryset().published().by_category(category)

# models.py da qo'shish
class News(models.Model):
    # ... maydonlar
    
    objects = NewsManager()  # Custom manager
    
    # ... qolgan metodlar
```

### 3. View'da kategoriyalar bilan ishlash

```python
# views.py
from django.views.generic import TemplateView
from django.db.models import Count, Prefetch, Q
from .models import Category, News

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Asosiy yangilik (Hero section)
        context['featured_news'] = News.objects.featured().with_relations().first()
        
        # 2. Kategoriyalar va ularning yangiliklarini olish
        context['categories_with_news'] = self.get_categories_with_news()
        
        # 3. Eng ko'p o'qilgan yangiliklar
        context['popular_news'] = News.objects.published()\
            .with_relations()\
            .order_by('-views_count')[:5]
        
        # 4. Eng yangi yangiliklar
        context['latest_news'] = News.objects.published()\
            .with_relations()\
            .latest_first()[:10]
        
        return context
    
    def get_categories_with_news(self):
        """Yangiliklarni kategoriyalar bo'yicha guruhlash"""
        return Category.objects.filter(
            is_featured=True  # Faqat asosiy kategoriyalar
        ).prefetch_related(
            Prefetch(
                'news_set',
                queryset=News.objects.published()\
                    .with_relations()\
                    .latest_first()[:6],  # Har kategoriyadan 6 ta
                to_attr='latest_news'
            )
        ).annotate(
            published_count=Count(
                'news',
                filter=Q(news__published=True)
            )
        ).filter(published_count__gt=0)  # Faqat yangiliği borlar
```

### 4. Template'da ko'rsatish

```html
<!-- home.html -->
{% extends 'base.html' %}

{% block content %}
<!-- Hero Section - Asosiy yangilik -->
{% if featured_news %}
<section class="hero-section mb-5">
    <div class="card bg-dark text-white">
        {% if featured_news.image %}
        <img src="{{ featured_news.image.url }}" class="card-img" alt="{{ featured_news.title }}">
        <div class="card-img-overlay d-flex align-items-end">
        {% else %}
        <div class="card-body">
        {% endif %}
            <div class="container">
                <span class="badge bg-{{ featured_news.category.color }} mb-2">
                    {{ featured_news.category.name }}
                </span>
                <h1 class="card-title display-4">{{ featured_news.title }}</h1>
                <p class="card-text lead">{{ featured_news.get_summary }}</p>
                <a href="{{ featured_news.get_absolute_url }}" class="btn btn-primary btn-lg">
                    Batafsil o'qish
                </a>
            </div>
        {% if featured_news.image %}</div>{% else %}</div>{% endif %}
    </div>
</section>
{% endif %}

<!-- Kategoriyalar bo'yicha yangiliklar -->
{% for category in categories_with_news %}
<section class="category-section mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="section-title">
            {% if category.icon %}
                <i class="fas fa-{{ category.icon }} text-{{ category.color }}"></i>
            {% endif %}
            {{ category.name }}
            <small class="text-muted">({{ category.published_count }} ta)</small>
        </h2>
        <a href="{% url 'category_detail' category.slug %}" class="btn btn-outline-primary">
            Barchasini ko'rish <i class="fas fa-arrow-right"></i>
        </a>
    </div>
    
    <div class="row">
        {% for news in category.latest_news %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                {% if news.image %}
                <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}" style="height: 200px; object-fit: cover;">
                {% endif %}
                
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">
                        <a href="{{ news.get_absolute_url }}" class="text-decoration-none">
                            {{ news.title|truncatechars:60 }}
                        </a>
                    </h5>
                    
                    <p class="card-text text-muted flex-grow-1">
                        {{ news.get_summary|truncatechars:100 }}
                    </p>
                    
                    <div class="card-footer bg-transparent px-0 py-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                <i class="fas fa-user"></i> {{ news.author.get_full_name|default:news.author.username }}
                            </small>
                            <small class="text-muted">
                                <i class="fas fa-clock"></i> {{ news.created_at|date:"d.m.Y" }}
                            </small>
                        </div>
                        
                        {% if news.views_count > 0 %}
                        <small class="text-muted">
                            <i class="fas fa-eye"></i> {{ news.views_count }} ta ko'rishlar
                        </small>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info">
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
<div class="alert alert-warning text-center">
    <h4><i class="fas fa-exclamation-triangle"></i> Yangilik topilmadi</h4>
    <p>Hozircha hech qanday yangilik nashr etilmagan.</p>
</div>
{% endfor %}

<!-- Sidebar ma'lumotlari -->
<aside class="mt-5">
    <div class="row">
        <!-- Mashhur yangiliklar -->
        {% if popular_news %}
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-fire text-danger"></i> Mashhur yangiliklar</h5>
                </div>
                <div class="list-group list-group-flush">
                    {% for news in popular_news %}
                    <a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between">
                            <div class="flex-grow-1">
                                <h6 class="mb-1">{{ news.title|truncatechars:50 }}</h6>
                                <small class="text-muted">{{ news.category.name }}</small>
                            </div>
                            <span class="badge bg-primary">{{ news.views_count }}</span>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Eng yangi yangiliklar -->
        {% if latest_news %}
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-clock text-success"></i> Eng yangi</h5>
                </div>
                <div class="list-group list-group-flush">
                    {% for news in latest_news|slice:":5" %}
                    <a href="{{ news.get_absolute_url }}" class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between">
                            <div class="flex-grow-1">
                                <h6 class="mb-1">{{ news.title|truncatechars:50 }}</h6>
                                <small class="text-muted">{{ news.category.name }}</small>
                            </div>
                            <small class="text-muted">{{ news.created_at|timesince }}</small>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</aside>
{% endblock %}
```

## Performance optimallashtirish

### 1. Database Query'larni kamaytirish

```python
# Yomon: N+1 problem
categories = Category.objects.all()
for category in categories:
    news_list = category.news_set.filter(published=True)[:5]  # Har safar query

# Yaxshi: Prefetch bilan
categories = Category.objects.prefetch_related(
    Prefetch('news_set', queryset=News.objects.published()[:5])
)
```

### 2. Select_related vs Prefetch_related

```python
# ForeignKey uchun select_related
News.objects.select_related('category', 'author')  # JOIN qiladi

# ManyToMany va Reverse FK uchun prefetch_related  
Category.objects.prefetch_related('news_set')  # Alohida query
```

### 3. Caching strategiyasi

```python
from django.core.cache import cache

def get_categories_with_news(self):
    cache_key = 'home_categories_news'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        cached_data = Category.objects.filter(is_featured=True).prefetch_related(
            Prefetch('news_set', queryset=News.objects.published()[:6])
        )
        cache.set(cache_key, cached_data, 300)  # 5 daqiqa cache
    
    return cached_data
```

## Xulosa

Bu darsda o'rgandingiz:

1. **Kategoriya bo'yicha guruhlash** - to'g'ri va noto'g'ri usullar
2. **Django ORM optimizatsiyasi** - Prefetch va select_related
3. **Custom Manager'lar** - kod qayta ishlatish
4. **Template strukturasi** - chiroyli ko'rinish
5. **Performance** - query'larni optimallashtirish

**Keyingi darsda:**
Context manager va get_context_data metodlarini chuqurroq o'rganamiz va sahifa performance'ini yaxshilaymiz.