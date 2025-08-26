# Lesson 10: Yangiliklar sayti loyihasi bilan tanishish

## Dars maqsadi
Ushbu darsda biz Django yordamida professional yangiliklar sayti loyihasi yaratishni boshlaymiz. Loyiha arxitekturasi, ma'lumotlar bazasi dizayni va asosiy funksionallik bilan tanishamiz.

## O'rganadigan mavzular
- Yangiliklar sayti loyihasi arxitekturasi
- Model yaratish va ma'lumotlar bazasi dizayni
- Category va Tag modellari
- News model bilan bog'lanishlar
- Admin panel sozlash
- Initial data migration
- Media fayllar bilan ishlash

## 1. Loyiha tuzilmasi va rejalash

### 1.1 Loyiha xususiyatlari

Bizning yangiliklar sayti quyidagi funksiyalarga ega bo'ladi:

- **Yangiliklar ko'rish:** Barcha yangiliklar ro'yxati
- **Kategoriyalar:** Yangiliklar kategoriyalar bo'yicha guruhlash
- **Teglar:** Yangiliklar teglar orqali filtrlash
- **Qidiruv:** Yangiliklar ichida qidiruv
- **Admin panel:** Yangiliklar boshqaruvi
- **Media:** Rasmlar va fayllar yuklash

### 1.2 Loyiha tuzilmasi

```
news_project/
├── news_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   └── templates/
│       └── news/
├── media/
│   ├── images/
│   └── uploads/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   └── includes/
└── manage.py
```

## 2. Django loyihasini yaratish

### 2.1 Virtual environment va loyiha yaratish

```bash
# Virtual environment yaratish
python -m venv news_env

# Virtual environment faollashtirish (Windows)
news_env\Scripts\activate

# Virtual environment faollashtirish (macOS/Linux)
source news_env/bin/activate

# Django o'rnatish
pip install django pillow

# Loyiha yaratish
django-admin startproject news_project
cd news_project

# News app yaratish
python manage.py startapp news
```

### 2.2 Settings.py sozlash

```python
# news_project/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',  # News app qo'shish
]

# Internationalization
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

## 3. Model yaratish

### 3.1 Category modeli

```python
# news/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    """
    Yangiliklar kategoriyasi modeli
    """
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Kategoriya nomi"
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        verbose_name="URL slug"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Tavsif"
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Kategoriya rangi (hex format)",
        verbose_name="Rang"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})

    def get_news_count(self):
        """Bu kategoriyaga tegishli yangiliklar soni"""
        return self.news_set.filter(is_published=True).count()
```

### 3.2 Tag modeli

```python
class Tag(models.Model):
    """
    Yangiliklar teglari modeli
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Teg nomi"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="URL slug"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:tag_detail', kwargs={'slug': self.slug})

    def get_news_count(self):
        """Bu tegga tegishli yangiliklar soni"""
        return self.news_set.filter(is_published=True).count()
```

### 3.3 News modeli

```python
class News(models.Model):
    """
    Yangiliklar modeli
    """
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Nashr qilingan'),
        ('archived', 'Arxivlangan'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Past'),
        ('normal', 'Oddiy'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha"
    )
    slug = models.SlugField(
        max_length=200,
        unique_for_date='publish_date',
        verbose_name="URL slug"
    )
    summary = models.TextField(
        max_length=500,
        help_text="Qisqacha mazmun (maksimal 500 belgi)",
        verbose_name="Qisqacha"
    )
    content = models.TextField(
        verbose_name="To'liq mazmun"
    )
    
    # Bog'lanishlar
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news',
        verbose_name="Kategoriya"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='news',
        verbose_name="Teglar"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name="Muallif"
    )

    # Media
    featured_image = models.ImageField(
        upload_to='news/images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Asosiy rasm (tavsiya etiladi: 1200x630px)",
        verbose_name="Asosiy rasm"
    )
    
    # Status va holatlar
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Holat"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name="Muhimlik darajasi"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Nashr qilingan"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Asosiy sahifada ko'rsatish",
        verbose_name="Asosiy yangilik"
    )

    # Sanalar
    publish_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Nashr sanasi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )

    # Statistika
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Ko'rishlar soni"
    )

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-publish_date', '-created_at']
        indexes = [
            models.Index(fields=['-publish_date']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Agar status 'published' bo'lsa, is_published True qilish
        if self.status == 'published':
            self.is_published = True
        else:
            self.is_published = False
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })

    def get_summary(self):
        """Summary mavjud bo'lmasa, content'dan olinadi"""
        if self.summary:
            return self.summary
        return self.content[:200] + "..." if len(self.content) > 200 else self.content

    def get_reading_time(self):
        """O'qish vaqtini hisoblash (daqiqalarda)"""
        word_count = len(self.content.split())
        reading_time = word_count / 250  # 250 so'z/daqiqa
        return max(1, round(reading_time))

    def increment_views(self):
        """Ko'rishlar sonini oshirish"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
```

## 4. Admin panel sozlash

### 4.1 Admin.py konfiguratsiyasi

```python
# news/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Tag, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'slug', 
        'color_display', 
        'news_count', 
        'is_active', 
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Rang'

    def news_count(self, obj):
        return obj.get_news_count()
    news_count.short_description = 'Yangiliklar soni'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _news_count=Count('news', distinct=True)
        )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'news_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def news_count(self, obj):
        return obj.get_news_count()
    news_count.short_description = 'Yangiliklar soni'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'author',
        'status',
        'priority',
        'is_featured',
        'views_count',
        'publish_date'
    ]
    list_filter = [
        'status',
        'category',
        'priority',
        'is_featured',
        'publish_date',
        'created_at'
    ]
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_editable = ['status', 'is_featured', 'priority']
    list_per_page = 20

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Kategoriya va teglar', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Nashr parametrlari', {
            'fields': (
                'author',
                'status',
                'priority',
                'is_featured',
                'publish_date'
            )
        }),
        ('Statistika', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratilayotgan bo'lsa
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'category', 'author'
        ).prefetch_related('tags')
```

## 5. URL konfiguratsiyasi

### 5.1 Asosiy URLs

```python
# news_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]

# Media fayllar uchun (development rejimida)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
```

### 5.2 News app URLs

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Asosiy sahifa
    path('', views.news_list, name='news_list'),
    
    # Yangilik detail
    path(
        '<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.news_detail,
        name='news_detail'
    ),
    
    # Kategoriya
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Tag
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    
    # Qidiruv
    path('search/', views.search_news, name='search_news'),
]
```

## 6. Dastlabki Views

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import News, Category, Tag

def news_list(request):
    """
    Barcha yangiliklar ro'yxati
    """
    news_list = News.objects.filter(
        is_published=True
    ).select_related('category', 'author').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(news_list, 10)  # 10 ta yangilik har sahifada
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Featured yangiliklar
    featured_news = News.objects.filter(
        is_published=True, 
        is_featured=True
    )[:5]
    
    # Kategoriyalar
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'featured_news': featured_news,
        'categories': categories,
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, year, month, day, slug):
    """
    Yangilik detail sahifasi
    """
    news = get_object_or_404(
        News,
        slug=slug,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
        is_published=True
    )
    
    # Ko'rishlar sonini oshirish
    news.increment_views()
    
    # O'xshash yangiliklar
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:5]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/news_detail.html', context)

def category_detail(request, slug):
    """
    Kategoriya bo'yicha yangiliklar
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    news_list = News.objects.filter(
        category=category,
        is_published=True
    ).select_related('author').prefetch_related('tags')
    
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'news/category_detail.html', context)

def tag_detail(request, slug):
    """
    Tag bo'yicha yangiliklar
    """
    tag = get_object_or_404(Tag, slug=slug)
    
    news_list = News.objects.filter(
        tags=tag,
        is_published=True
    ).select_related('category', 'author')
    
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'news/tag_detail.html', context)

def search_news(request):
    """
    Yangiliklar qidiruvi
    """
    query = request.GET.get('q')
    results = []
    
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query),
            is_published=True
        ).select_related('category', 'author')
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'news/search_results.html', context)
```

## 7. Migration va dastlabki ma'lumotlar

### 7.1 Migration yaratish va qo'llash

```bash
# Migration fayllarini yaratish
python manage.py makemigrations news

# Migration qo'llash
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser
```

### 7.2 Dastlabki ma'lumotlar (Django shell orqali)

```python
# python manage.py shell
from django.contrib.auth.models import User
from news.models import Category, Tag, News
from django.utils import timezone

# Kategoriyalar yaratish
categories_data = [
    {'name': 'Siyosat', 'description': 'Siyosiy yangiliklar', 'color': '#dc3545'},
    {'name': 'Sport', 'description': 'Sport yangiliklar', 'color': '#28a745'},
    {'name': 'Texnologiya', 'description': 'IT yangiliklar', 'color': '#007bff'},
    {'name': 'Iqtisodiyot', 'description': 'Moliya yangiliklar', 'color': '#ffc107'},
    {'name': 'Madaniyat', 'description': 'San\'at va madaniyat', 'color': '#6f42c1'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"Kategoriya yaratildi: {category.name}")

# Teglar yaratish
tags_data = ['yangi', 'muhim', 'so\'nggi', 'mashhur', 'tez', 'eksklyuziv']
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        print(f"Teg yaratildi: {tag.name}")

# Test yangilik yaratish
user = User.objects.first()  # Birinchi userni olish
sport_category = Category.objects.get(name='Sport')

test_news = News.objects.create(
    title='Futbol bo\'yicha yangi rekord',
    summary='Bugungi o\'yinda yangi rekord o\'rnatildi',
    content='Bu yerda to\'liq yangilik matni bo\'ladi...',
    category=sport_category,
    author=user,
    status='published',
    is_featured=True
)

print(f"Test yangilik yaratildi: {test_news.title}")
```

## 8. Best Practices va tavsiyalar

### 8.1 Model optimizatsiyasi

```python
# Effective queryset'lar
# Yomon:
for news in News.objects.all():
    print(news.category.name)  # N+1 problem

# Yaxshi:
for news in News.objects.select_related('category'):
    print(news.category.name)
```

### 8.2 Slug generatsiyasi

```python
# Custom slug generator
from django.utils.text import slugify
import string
import random

def generate_unique_slug(model_class, title):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug
```

### 8.3 Xavfsizlik choralari

```python
# settings.py da qo'shimcha sozlamalar
# File upload restrictions
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
```

## 9. Keyingi qadamlar

### 9.1 Loyihani ishga tushirish

```bash
# Development server
python manage.py runserver

# Admin panelga kirish
# http://127.0.0.1:8000/admin/

# Asosiy sahifa
# http://127.0.0.1:8000/
```

### 9.2 Kelajakda qo'shilishi mumkin

1. **Template'lar yaratish** (keyingi darsda)
2. **Static fayllar sozlash**
3. **Search funksiyasini yaxshilash**
4. **Caching qo'shish**
5. **API yaratish**
6. **User authentication**
7. **Comment tizimi**
8. **Newsletter**
9. **RSS feeds**
10. **Social media integration**

## 10. Xulosa

Ushbu darsda biz:

1. **Yangiliklar sayti loyihasi**ni boshladik
2. **Professional model'lar** yaratdik (Category, Tag, News)
3. **Admin panel**ni sozladik
4. **URL routing** qildik
5. **Dastlabki view'lar** yozdik
6. **Ma'lumotlar bazasi** tuzilmasini yaratdik

### Keyingi darsda:
- Template'lar yaratish
- Frontend dizayni
- Responsive layout
- Bootstrap integratsiyasi

### Foydali linklar:
- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Pillow Library](https://pillow.readthedocs.io/)