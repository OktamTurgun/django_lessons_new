# Dars 26: Amaliyot - URLni slug'ga o'zgartirish va get_absolute_url

## Amaliyot maqsadi
Ushbu amaliyotda siz Django loyihasida slug'lar bilan ishlashni to'liq amaliyotda qo'llaysiz va SEO-friendly URL'lar yaratishni o'rganasiz.

## 1-bosqich: Loyihani tayyorlash

### Mavjud loyihani tekshirish
```bash
# Loyiha katalogiga o'tish
cd your_news_project

# Virtual muhitni faollashtirish
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows

# Loyihani ishga tushirish
python manage.py runserver
```

### Mavjud URL'larni ko'rish
Hozirgi URL'laringiz shunday ko'rinishda:
```
http://127.0.0.1:8000/news/1/
http://127.0.0.1:8000/news/2/
http://127.0.0.1:8000/news/3/
```

Maqsad - bularni shunday qilish:
```
http://127.0.0.1:8000/news/django-bilan-web-sayt-yaratish/
http://127.0.0.1:8000/news/python-dasturlash-tili/
```

## 2-bosqich: Model'ni yangilash

### News modeliga slug maydonini qo'shish

`news/models.py` faylini oching va quyidagi o'zgarishlarni bajaring:

```python
# news/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class News(models.Model):
    title = models.CharField(max_length=250, verbose_name="Sarlavha")
    slug = models.SlugField(
        max_length=250, 
        unique=True, 
        blank=True,
        verbose_name="URL manzil"
    )
    body = models.TextField(verbose_name="Matn")
    photo = models.ImageField(
        upload_to='news/photos/', 
        blank=True, 
        null=True,
        verbose_name="Rasm"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        verbose_name="Kategoriya"
    )
    created_time = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Yaratilgan vaqt"
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqt"
    )
    status = models.BooleanField(default=True, verbose_name="Holat")
    
    def save(self, *args, **kwargs):
        # Slug avtomatik yaratish
        if not self.slug:
            # Title'dan slug yaratish
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Agar bunday slug mavjud bo'lsa, raqam qo'shamiz
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Yangilik sahifasining to'liq URL manzilini qaytaradi"""
        return reverse('news:news_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
```

### Model o'zgarishlarini tushuntirish:

1. **SlugField qo'shildi**:
   - `max_length=250`: Maksimal uzunlik
   - `unique=True`: Har bir slug noyob bo'lishi kerak
   - `blank=True`: Admin panelda bo'sh qoldirilishi mumkin

2. **save() metodini qayta yozdik**:
   - `slugify()` - Django'ning o'rnatilgan funksiyasi
   - Noyoblikni ta'minlash uchun counter ishlatildi

3. **get_absolute_url() qo'shildi**:
   - Har bir yangilik uchun to'liq URL yaratadi

## 3-bosqich: Migration yaratish va ishlatish

### Migration faylini yaratish
```bash
python manage.py makemigrations news
```

Natija:
```
Migrations for 'news':
  news/migrations/0002_news_slug.py
    - Add field slug to news
```

### Migration'ni ishlatish
```bash
python manage.py migrate
```

### Xato yuz bersa:
Agar "IntegrityError" xatosi chiqsa, avval mavjud ma'lumotlarga slug qo'shish kerak.

## 4-bosqich: Mavjud ma'lumotlarga slug qo'shish

### Django shell orqali slug qo'shish
```bash
python manage.py shell
```

Shell ichida:
```python
from news.models import News
from django.utils.text import slugify

# Barcha yangiliklar ro'yxati
news_list = News.objects.all()

# Har biriga slug qo'shish
for news in news_list:
    if not news.slug:  # Agar slug bo'sh bo'lsa
        base_slug = slugify(news.title)
        slug = base_slug
        counter = 1
        
        # Noyoblikni tekshirish
        while News.objects.filter(slug=slug).exclude(id=news.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        news.slug = slug
        news.save()
        print(f"Qo'shildi: {news.title} -> {slug}")

# Shell'dan chiqish
exit()
```

## 5-bosqich: URL pattern'larni yangilash

### news/urls.py faylini o'zgartirish
```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    # Eski variant:
    # path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Yangi variant - slug bilan:
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]
```

## 6-bosqich: Views'ni yangilash

### news/views.py faylini o'zgartirish
```python
# news/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import News, Category

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5  # Sahifaga 5 ta yangilik
    
    def get_queryset(self):
        return News.objects.filter(status=True).select_related('category')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    # Slug bo'yicha qidirish
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        """Faqat faol yangiliklar ko'rsatilsin"""
        return get_object_or_404(
            News.objects.select_related('category'),
            slug=self.kwargs['slug'],
            status=True
        )
```

### View o'zgarishlarini tushuntirish:

1. **slug_field**: Model'dagi slug maydon nomi
2. **slug_url_kwarg**: URL'dan keladigan parametr nomi  
3. **get_object()**: Maxsus qidiruv mantiqini qo'shdik
4. **select_related('category')**: Database so'rovlarini optimizatsiya qilish

## 7-bosqich: Template'larni yangilash

### news/news_list.html
```html
<!-- templates/news/news_list.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Yangiliklar{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <h2>So'nggi yangiliklar</h2>
            
            {% for news in news_list %}
            <div class="card mb-4">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" class="card-img-top" alt="{{ news.title }}">
                {% endif %}
                
                <div class="card-body">
                    <h5 class="card-title">
                        <!-- get_absolute_url() ishlatish -->
                        <a href="{{ news.get_absolute_url }}" class="text-decoration-none">
                            {{ news.title }}
                        </a>
                    </h5>
                    
                    <p class="card-text">
                        {{ news.body|truncatewords:25 }}
                    </p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-calendar"></i>
                            {{ news.created_time|date:"d.m.Y" }}
                        </small>
                        
                        <span class="badge bg-primary">
                            {{ news.category.name }}
                        </span>
                    </div>
                    
                    <!-- To'liq o'qish tugmasi -->
                    <div class="mt-2">
                        <a href="{{ news.get_absolute_url }}" class="btn btn-outline-primary btn-sm">
                            To'liq o'qish <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                Hozircha yangiliklar mavjud emas.
            </div>
            {% endfor %}
            
            <!-- Sahifalar bo'yicha bo'lish -->
            {% if is_paginated %}
            <nav aria-label="News pagination">
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
                        <span class="page-link">{{ page_obj.number }}</span>
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
            
        </div>
        
        <!-- Sidebar -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h6><i class="fas fa-fire"></i> So'nggi yangiliklar</h6>
                </div>
                <div class="card-body">
                    {% for recent_news in news_list|slice:":3" %}
                    <div class="d-flex mb-2">
                        <div>
                            <a href="{{ recent_news.get_absolute_url }}" class="text-decoration-none">
                                <small>{{ recent_news.title|truncatechars:40 }}</small>
                            </a>
                            <br>
                            <small class="text-muted">{{ recent_news.created_time|date:"d.m.Y" }}</small>
                        </div>
                    </div>
                    <hr>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### news/news_detail.html
```html
<!-- templates/news/news_detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <!-- Orqaga qaytish tugmasi -->
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="{% url 'home' %}">Bosh sahifa</a>
                    </li>
                    <li class="breadcrumb-item">
                        <a href="{% url 'news:news_list' %}">Yangiliklar</a>
                    </li>
                    <li class="breadcrumb-item active">{{ news.title|truncatechars:30 }}</li>
                </ol>
            </nav>
            
            <!-- Yangilik mazmuni -->
            <article class="news-article">
                <header class="mb-4">
                    <h1 class="display-5">{{ news.title }}</h1>
                    
                    <div class="d-flex justify-content-between align-items-center text-muted mb-3">
                        <div>
                            <i class="fas fa-calendar-alt"></i>
                            <time datetime="{{ news.created_time|date:'Y-m-d' }}">
                                {{ news.created_time|date:"d F Y, H:i" }}
                            </time>
                        </div>
                        
                        <span class="badge bg-primary fs-6">
                            <i class="fas fa-tag"></i>
                            {{ news.category.name }}
                        </span>
                    </div>
                </header>
                
                {% if news.photo %}
                <figure class="mb-4">
                    <img src="{{ news.photo.url }}" 
                         class="img-fluid rounded" 
                         alt="{{ news.title }}"
                         style="width: 100%; max-height: 400px; object-fit: cover;">
                </figure>
                {% endif %}
                
                <div class="news-content">
                    {{ news.body|linebreaks }}
                </div>
                
                <!-- Meta ma'lumotlar -->
                <footer class="mt-4 pt-3 border-top">
                    <div class="row">
                        <div class="col-md-6">
                            <small class="text-muted">
                                <i class="fas fa-clock"></i>
                                Oxirgi yangilanish: {{ news.updated_time|date:"d.m.Y, H:i" }}
                            </small>
                        </div>
                        <div class="col-md-6 text-end">
                            <!-- URL manzilni ko'rsatish -->
                            <small class="text-muted">
                                <i class="fas fa-link"></i>
                                <code>{{ news.slug }}</code>
                            </small>
                        </div>
                    </div>
                </footer>
            </article>
            
            <!-- Navigatsiya tugmalari -->
            <div class="d-flex justify-content-between mt-4">
                <a href="{% url 'news:news_list' %}" class="btn btn-outline-secondary">
                    <i class="fas fa-arrow-left"></i> Barcha yangiliklar
                </a>
                
                <!-- Ijtimoiy tarmoqlarda ulashish -->
                <div>
                    <a href="https://t.me/share/url?url={{ request.build_absolute_uri }}" 
                       class="btn btn-outline-info btn-sm me-2" target="_blank">
                        <i class="fab fa-telegram"></i> Telegram
                    </a>
                    <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}" 
                       class="btn btn-outline-primary btn-sm" target="_blank">
                        <i class="fab fa-facebook"></i> Facebook
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Sidebar -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h6><i class="fas fa-newspaper"></i> Boshqa yangiliklar</h6>
                </div>
                <div class="card-body">
                    <!-- Bu yerda boshqa yangiliklar ro'yxati bo'ladi -->
                    <small class="text-muted">Tez orada...</small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 8-bosqich: Admin panelni sozlash

### news/admin.py faylini yangilash
```python
# news/admin.py
from django.contrib import admin
from .models import Category, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time')
    list_filter = ('status', 'category', 'created_time')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # Slug avtomatik to'ldiriladi
    list_editable = ('status',)
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Kontent', {
            'fields': ('body', 'photo')
        }),
        ('Sozlamalar', {
            'fields': ('status',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Agar obyekt yaratilgan bo'lsa, slug o'zgartirishni cheklash"""
        if obj:  # Tahrirlash vaqtida
            return self.readonly_fields + ('slug',)
        return self.readonly_fields
```

### Admin sozlamalarining tushuntirish:
- **prepopulated_fields**: Title yozganda slug avtomatik to'ldiriladi
- **list_editable**: Ro'yxat sahifasida to'g'ridan-to'g'ri tahrirlash
- **fieldsets**: Admin formasini bo'limlarga ajratish
- **get_readonly_fields**: Yaratilgandan keyin slug'ni o'zgartirish mumkin emas

### Superuser yaratish (agar yo'q bo'lsa)
```bash
python manage.py createsuperuser
```

## 9-bosqich: Testlash va tekshirish

### Loyihani ishga tushirish
```bash
python manage.py runserver
```

### Admin panelga kirish
1. `http://127.0.0.1:8000/admin/` ga o'ting
2. Login va parolni kiriting
3. Yangiliklar bo'limiga o'ting
4. Yangi yangilik qo'shishda:
   - **Title** maydonini to'ldiring
   - **Slug** maydoni avtomatik to'ldirilishini kuzating
   - **Category** tanlang
   - **Body** va **Photo** qo'shing
   - **Save** tugmasini bosing

### Slug avtomatik yaratilishini tekshirish
Admin panelda yangilik qo'shayotganda:
```
Title: "Django Framework bilan Web Sayt Yaratish"
Slug: "django-framework-bilan-web-sayt-yaratish" (avtomatik)
```

### URL'larni tekshirish
Endi yangilik sahifalarining URL'lari shunday ko'rinishda bo'ladi:
```
Eski: http://127.0.0.1:8000/news/1/
Yangi: http://127.0.0.1:8000/news/django-framework-bilan-web-sayt-yaratish/
```

### Template'larda havolalar
Barcha havola o'tishlarini tekshiring:
- Yangiliklar ro'yxati sahifasidagi havolalar
- Yangilik detali sahifasidagi qaytish tugmasi
- Breadcrumb navigatsiya

## 10-bosqich: SEO optimizatsiya

### Meta teglarni qo'shish
Base template'ni meta teglar uchun tayyorlang:

```html
<!-- templates/base.html ichiga qo'shish -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    
    {% block meta %}
    <meta name="description" content="O'zbekistonning eng so'nggi yangiliklari">
    <meta name="keywords" content="yangiliklar, o'zbekiston, news">
    {% endblock %}
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">
                <i class="fas fa-newspaper"></i> Yangiliklar
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="{% url 'news:news_list' %}">Barcha yangiliklar</a>
            </div>
        </div>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
        </div>
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### news_detail.html uchun SEO teglar
```html
<!-- templates/news/news_detail.html boshida -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ news.title }} - Bizning sayt{% endblock %}

{% block meta %}
<meta name="description" content="{{ news.body|truncatewords:20|striptags }}">
<meta name="keywords" content="{{ news.category.name }}, yangiliklar, {{ news.title }}">
<meta name="author" content="Bizning sayt">

<!-- Open Graph (Facebook, Telegram) -->
<meta property="og:title" content="{{ news.title }}">
<meta property="og:description" content="{{ news.body|truncatewords:20|striptags }}">
<meta property="og:url" content="{{ request.build_absolute_uri }}">
<meta property="og:type" content="article">
{% if news.photo %}
<meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{{ news.photo.url }}">
{% endif %}

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ news.title }}">
<meta name="twitter:description" content="{{ news.body|truncatewords:20|striptags }}">

<!-- Structured Data (JSON-LD) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{{ news.title }}",
  "description": "{{ news.body|truncatewords:20|striptags }}",
  "datePublished": "{{ news.created_time|date:'c' }}",
  "dateModified": "{{ news.updated_time|date:'c' }}",
  {% if news.photo %}
  "image": "{{ request.scheme }}://{{ request.get_host }}{{ news.photo.url }}",
  {% endif %}
  "author": {
    "@type": "Organization",
    "name": "Bizning sayt"
  }
}
</script>
{% endblock %}
```

## 11-bosqich: Xatoliklarni hal qilish

### Keng tarqalgan xatolar va yechimlar

#### 1. "NoReverseMatch" xatosi
**Xato mesaji**: `NoReverseMatch at /news/some-slug/`
**Sabab**: URL pattern noto'g'ri yoki mavjud emas
**Yechim**:
```python
# urls.py faylini tekshiring
urlpatterns = [
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    # name='news_detail' to'g'ri yozilganini tekshiring
]
```

#### 2. "Slug already exists" xatosi
**Sabab**: Bir xil nomli yangiliklar yaratilmoqda
**Yechim**: Model'dagi save() metodini tekshiring:
```python
def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        
        # Bu yerda self.id ni exclude qilish muhim
        while News.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        self.slug = slug
    super().save(*args, **kwargs)
```

#### 3. "Page not found (404)" xatosi
**Tekshirish**: Database'da slug mavjudligini tekshiring
```bash
python manage.py shell
```
```python
from news.models import News

# Barcha slug'larni ko'rish
for news in News.objects.all():
    print(f"ID: {news.id}, Title: {news.title}, Slug: {news.slug}")

# Muayyan slug'ni qidirish
news = News.objects.filter(slug='your-slug-here').first()
print(news)
```

#### 4. Kirill harflar bilan muammo
**Masala**: "Yangi loyiha" → "ÿíåé-ëîéèòà" (noto'g'ri)
**Yechim**: Transliterate kutubxonasini o'rnating
```bash
pip install transliterate
```

Model'ni yangilang:
```python
from transliterate import translit, detect_language

def save(self, *args, **kwargs):
    if not self.slug:
        title = self.title
        
        # Kirill harflarini aniqlash va transliterate qilish
        try:
            if detect_language(title) == 'ru':
                title = translit(title, 'ru', reversed=True)
        except:
            pass  # Agar xato bo'lsa, asl title'ni ishlat
            
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        
        while News.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        self.slug = slug
    super().save(*args, **kwargs)
```

#### 5. Admin panelda slug ko'rinmaydi
**Yechim**: Admin class'ni to'g'ri ro'yxatdan o'tkazing
```python
# admin.py
from django.contrib import admin
from .models import News

# Bu usulni ishlatgan bo'lsangiz:
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # ...

# Yoki bu usulni:
admin.site.register(News, NewsAdmin)
```

## 12-bosqich: Test yozish va tekshirish

### Test faylini yaratish
`news/tests.py` faylini yarating:

```python
# news/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, News

class NewsModelTest(TestCase):
    def setUp(self):
        """Test uchun dastlabki ma'lumotlar"""
        self.category = Category.objects.create(name="Technology")
        self.news = News.objects.create(
            title="Django Framework",
            body="Django haqida ma'lumot",
            category=self.category,
            status=True
        )
    
    def test_slug_generation(self):
        """Slug avtomatik yaratilishini tekshirish"""
        self.assertEqual(self.news.slug, "django-framework")
    
    def test_get_absolute_url(self):
        """get_absolute_url metodini tekshirish"""
        expected_url = reverse('news:news_detail', kwargs={'slug': self.news.slug})
        self.assertEqual(self.news.get_absolute_url(), expected_url)
    
    def test_unique_slug(self):
        """Noyob slug yaratilishini tekshirish"""
        news2 = News.objects.create(
            title="Django Framework",  # Bir xil title
            body="Boshqa ma'lumot",
            category=self.category
        )
        self.assertNotEqual(self.news.slug, news2.slug)
        self.assertEqual(news2.slug, "django-framework-1")
    
    def test_string_representation(self):
        """__str__ metodini tekshirish"""
        self.assertEqual(str(self.news), "Django Framework")

class NewsViewTest(TestCase):
    def setUp(self):
        """Test uchun dastlabki ma'lumotlar"""
        self.client = Client()
        self.category = Category.objects.create(name="Technology")
        self.news = News.objects.create(
            title="Test News",
            body="Test content for news article",
            category=self.category,
            status=True
        )
    
    def test_news_list_view(self):
        """Yangiliklar ro'yxati sahifasini tekshirish"""
        response = self.client.get(reverse('news:news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        self.assertIn(self.news, response.context['news_list'])
    
    def test_news_detail_view(self):
        """Yangilik sahifasini tekshirish"""
        response = self.client.get(
            reverse('news:news_detail', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        self.assertContains(response, self.news.body)
        self.assertEqual(response.context['news'], self.news)
    
    def test_inactive_news_not_shown(self):
        """Faol bo'lmagan yangilik ko'rsatilmasligini tekshirish"""
        self.news.status = False
        self.news.save()
        
        # List view'da ko'rsatilmasligi kerak
        response = self.client.get(reverse('news:news_list'))
        self.assertNotContains(response, self.news.title)
        
        # Detail view 404 qaytarishi kerak
        response = self.client.get(
            reverse('news:news_detail', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_nonexistent_slug_returns_404(self):
        """Mavjud bo'lmagan slug uchun 404 qaytarish"""
        response = self.client.get(
            reverse('news:news_detail', kwargs={'slug': 'mavjud-emas'})
        )
        self.assertEqual(response.status_code, 404)

class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sports")
    
    def test_category_str(self):
        """Category __str__ metodini tekshirish"""
        self.assertEqual(str(self.category), "Sports")
```

### Testlarni ishga tushirish
```bash
# Barcha testlar
python manage.py test news

# Muayyan test klassi
python manage.py test news.tests.NewsModelTest

# Muayyan test metodi
python manage.py test news.tests.NewsModelTest.test_slug_generation

# Coverage bilan (qo'shimcha kutubxona kerak)
pip install coverage
coverage run --source='.' manage.py test news
coverage report
```

### Test natijalarini ko'rish
```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.045s

OK
Destroying test database for alias 'default'...
```

## 13-bosqich: Qo'shimcha funksiyalar

### URL pattern'ga qo'shimcha validatsiya
```python
# news/urls.py
from django.urls import path, re_path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    
    # Regex bilan slug pattern'ni cheklash (ixtiyoriy)
    re_path(
        r'^(?P<slug>[-\w]+)/, 
        views.NewsDetailView.as_view(), 
        name='news_detail'
    ),
    
    # Yoki oddiy slug pattern
    # path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]
```

### Sitemap qo'shish (SEO uchun)
```python
# news/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import News

class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return News.objects.filter(status=True)
    
    def lastmod(self, obj):
        return obj.updated_time
    
    def location(self, obj):
        return obj.get_absolute_url()
```

Main urls.py ga qo'shish:
```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from news.sitemaps import NewsSitemap

sitemaps = {
    'news': NewsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
```

### RSS Feed qo'shish
```python
# news/feeds.py
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import News

class LatestNewsFeed(Feed):
    title = "So'nggi yangiliklar"
    link = reverse_lazy('news:news_list')
    description = "Saytning eng so'nggi yangiliklari"
    
    def items(self):
        return News.objects.filter(status=True)[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.body[:200]
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.created_time
```

URLs'ga qo'shish:
```python
# news/urls.py
from .feeds import LatestNewsFeed

urlpatterns = [
    # ...
    path('feed/', LatestNewsFeed(), name='news_feed'),
]
```

## 14-bosqich: Performance optimizatsiya

### Database query optimizatsiya
```python
# views.py
class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5
    
    def get_queryset(self):
        return News.objects.filter(status=True)\
                          .select_related('category')\
                          .only('title', 'slug', 'body', 'photo', 'created_time', 'category__name')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        return get_object_or_404(
            News.objects.select_related('category'),
            slug=self.kwargs['slug'],
            status=True
        )
```

### Caching qo'shish
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Cache table yaratish
# python manage.py createcachetable
```

View'larda cache ishlatish:
```python
# views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 daqiqa
class NewsDetailView(DetailView):
    # ...
```

## Yakuniy natija va tekshirish

### ✅ Bajarilgan ishlarni tekshirish ro'yxati:

1. **Model o'zgarishlari**:
   - [x] Slug maydoni qo'shildi
   - [x] save() metodi yozildi
   - [x] get_absolute_url() metodi qo'shildi

2. **Database**:
   - [x] Migration yaratildi va ishlatildi
   - [x] Mavjud ma'lumotlarga slug qo'shildi

3. **URLs va Views**:
   - [x] URL pattern slug bilan yangilandi
   - [x] DetailView slug bilan ishlash uchun sozlandi

4. **Templates**:
   - [x] get_absolute_url() ishlatildi
   - [x] SEO meta teglar qo'shildi
   - [x] Breadcrumb navigatsiya qo'shildi

5. **Admin panel**:
   - [x] prepopulated_fields sozlandi
   - [x] Fieldsets tashkil qilindi
   - [x] List display optimallashtirildi

6. **Testing**:
   - [x] Testlar yozildi va o'tkazildi
   - [x] Barcha testlar muvaffaqiyatli

7. **Qo'shimcha funksiyalar**:
   - [x] SEO optimizatsiya
   - [x] Performance tuning
   - [x] Error handling

### 📊 Oxirgi tekshirish:

**URL'larni tekshiring**:
```
✅ Eski: /news/1/ → Yangi: /news/django-framework/
✅ Admin panelda "View on site" tugmasi ishlaydi
✅ Template'lardagi barcha havolalar to'g'ri
✅ 404 sahifa noto'g'ri slug uchun ko'rsatiladi
```

**SEO tekshiruvi**:
```
✅ Meta description mavjud
✅ Open Graph teglar qo'shildi  
✅ URL manzili SEO-friendly
✅ Structured data qo'shildi
✅ Sitemap va RSS feed (ixtiyoriy)
```

**Performance tekshiruvi**:
```
✅ Database queries optimallashtirildi
✅ select_related() ishlatildi
✅ only() bilan maydonlar cheklandi
✅ Caching qo'shildi (ixtiyoriy)
```

### 🎉 Muvaffaqiyat!

Agar barcha tekshiruvlar muvaffaqiyatli bo'lsa, sizda endi professional darajadagi slug tizimi bor! 

## Bu darsdan o'rgangan bilimlaringiz:

### 🎯 Asosiy bilimlar:
- **Slug nima va nima uchun kerak**
- **SEO-friendly URL'lar yaratish**
- **Django model metodlari** (save, get_absolute_url)
- **URL pattern'lar bilan ishlash**
- **Template'larda URL'larni to'g'ri ishlatish**

### 🛠️ Texnik ko'nikmalar:
- **slugify() funksiyasi**
- **Migration'lar bilan ishlash**  
- **Admin panel sozlash**
- **Test yozish va debugging**
- **Performance optimizatsiya**

### 📈 Professional skills:
- **SEO optimizatsiya**
- **Error handling**
- **Code organization**
- **Best practices**
- **Documentation**

## Maslahatlar va Best Practices

### 🔥 Muhim maslahatlar:

1. **Har doim slug noyob bo'lishini ta'minlang**
2. **get_absolute_url() metodini doim ishlating**
3. **Template'larda URL'larni qo'lda yozmasdan get_absolute_url() ishlating**
4. **Kirill harflar uchun transliterate ishlatting**
5. **Slug uzunligini cheklang (max 50-70 belgi)**
6. **Test yozishni unutmang**
7. **Migration'larni ehtiyotkorlik bilan bajaring**

### ⚡ Performance tips:

1. **select_related()** ishlatib database so'rovlarini kamaytiring
2. **get_object_or_404()** ishlatib xavfsizlikni ta'minlang
3. **Slug'larga index qo'shing** (Django avtomatik qo'shadi)
4. **Cache ishlatib sahifalar tezligini oshiring**

### 🔒 Xavfsizlik maslahalari:

1. **Slug validation qo'shing**
2. **XSS himoyasini unutmang**
3. **Status field orqali content'ni boshqaring**
4. **404 sahifalarini to'g'ri sozlang**

## Keyingi qadamlar

1. **Kategoriya bo'yicha slug**: Kategoriyalar uchun ham slug qo'shish
2. **Breadcrumb navigation**: To'liq navigatsiya tizimi
3. **Related posts**: O'xshash yangiliklar ko'rsatish
4. **Search functionality**: Qidiruv tizimini qo'shish
5. **Comments system**: Izohlar tizimi
6. **Social sharing**: Ijtimoiy tarmoqlarda ulashish

**Keyingi dars**: Yangiliklar sayti sahifasini yaratishni o'rganamiz!
