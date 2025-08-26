# Practice 10: Yangiliklar sayti loyihasi - Amaliy mashqlar

## Mashq maqsadi
Ushbu amaliy mashqlarda siz Django yangiliklar sayti loyihasini yaratish, model'lar bilan ishlash va admin panel sozlash ko'nikmalarini mustahkamlaysiz.

## Vazifa ro'yxati

### Asosiy vazifalar 

#### 1. Vazifa: Django loyiha yaratish va sozlash
**Maqsad:** News loyihasini yaratish va asosiy sozlamalarni qilish

**Bajarilishi kerak:**
```bash
# 1. Loyiha papkasini yarating
mkdir news_project
cd news_project

# 2. Pipenv muhitini yarating va kutubxonalarni o'rnating
pipenv install django pillow

# 3. Virtual environment ga kiring
pipenv shell

# 4. Django loyiha yaratish
django-admin startproject . .

# 5. News app yaratish
python manage.py startapp news
```

**Settings.py sozlash:**
```python
# news_project/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',  # Bu qator qo'shiladi
]

# Media files sozlamalar
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Localization
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
```

**Tekshirish:** 
- `python manage.py runserver` ishga tushishi
- Admin panelga kirish mumkin bo'lishi
- News app ro'yxatda ko'rinishi

---

#### 2. Vazifa: Category modeli yaratish
**Maqsad:** Yangiliklar kategoriyasi uchun to'liq model yaratish

**Bajarilishi kerak:**
```python
# news/models.py
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    """
    Yangiliklar kategoriyasi modeli
    Misol: Sport, Siyosat, Texnologiya
    """
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Kategoriya nomi",
        help_text="Kategoriya nomini kiriting (masalan: Sport)"
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        verbose_name="URL slug",
        help_text="URL uchun ishlatiladi (avtomatik yaratiladi)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Tavsif",
        help_text="Kategoriya haqida qisqacha ma'lumot"
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Kategoriya rangi hex formatda (#ff0000)",
        verbose_name="Rang"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol",
        help_text="Kategoriya faolmi?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']  # Nom bo'yicha tartiblash

    def __str__(self):
        """Admin panelda ko'rinadigan nom"""
        return self.name

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Kategoriya sahifasiga link"""
        return reverse('news:category_detail', kwargs={'slug': self.slug})

    def get_news_count(self):
        """Bu kategoriyaga tegishli yangiliklar soni"""
        return self.news_set.filter(is_published=True).count()
```

**Migration qilish:**
```bash
python manage.py makemigrations news
python manage.py migrate
```

**Tekshirish:** 
- Model admin panelda ko'rinishi
- Slug avtomatik yaratilishi
- Kategoriya yaratish va o'zgartirish ishlashi

---

#### 3. Vazifa: Tag modeli yaratish
**Maqsad:** Yangiliklar teglari uchun model yaratish

**Bajarilishi kerak:**
```python
# news/models.py (Category modelidan keyin qo'shing)

class Tag(models.Model):
    """
    Yangiliklar teglari modeli
    Misol: #yangi, #muhim, #so'nggi
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Teg nomi",
        help_text="Teg nomini kiriting (masalan: muhim)"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="URL slug",
        help_text="URL uchun ishlatiladi"
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
        return f"#{self.name}"  # Teg sifatida ko'rsatish

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish va kichik harfga o'tkazish"""
        if not self.slug:
            self.slug = slugify(self.name.lower())
        self.name = self.name.lower()  # Teglar kichik harfda
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Tag sahifasiga link"""
        return reverse('news:tag_detail', kwargs={'slug': self.slug})

    def get_news_count(self):
        """Bu tegga tegishli yangiliklar soni"""
        return self.news_set.filter(is_published=True).count()
```

**Migration va test:**
```bash
python manage.py makemigrations news
python manage.py migrate

# Django shell orqali test
python manage.py shell
>>> from news.models import Tag
>>> tag = Tag.objects.create(name="Muhim")
>>> print(tag)  # #muhim chiqishi kerak
```

**Tekshirish:** Tag modeli admin panelda ishlashi va slug avtomatik yaratilishi.

---

#### 4. Vazifa: News modeli yaratish
**Maqsad:** To'liq yangiliklar modeli yaratish

**Bajarilishi kerak:**
```python
# news/models.py (Tag modelidan keyin qo'shing)
from django.contrib.auth.models import User
from django.utils import timezone

class News(models.Model):
    """
    Yangiliklar modeli - asosiy content
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

    # Asosiy maydonlar
    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha",
        help_text="Yangilik sarlavhasi (maksimal 200 belgi)"
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
        verbose_name="To'liq mazmun",
        help_text="Yangilik mazmuni (HTML teglar qo'llab-quvvatlanadi)"
    )
    
    # Bog'lanishlar (Relationships)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
        verbose_name="Kategoriya"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='news',
        verbose_name="Teglar",
        help_text="Bir nechta tegni tanlashingiz mumkin"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name="Muallif"
    )

    # Media fayl
    featured_image = models.ImageField(
        upload_to='news/images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Asosiy rasm (tavsiya: 1200x630px)",
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
        verbose_name="Nashr qilingan",
        help_text="Saytda ko'rsatilsinmi?"
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
        """Slug yaratish va status bo'yicha is_published yangilash"""
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Status published bo'lsa, is_published True qilish
        if self.status == 'published':
            self.is_published = True
        else:
            self.is_published = False
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Yangilik sahifasiga link"""
        return reverse('news:news_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })

    def get_summary(self):
        """Summary bo'lmasa content'dan olish"""
        if self.summary:
            return self.summary
        return self.content[:200] + "..." if len(self.content) > 200 else self.content

    def get_reading_time(self):
        """O'qish vaqtini hisoblash (daqiqa)"""
        word_count = len(self.content.split())
        reading_time = word_count / 250  # 250 so'z/daqiqa
        return max(1, round(reading_time))

    def increment_views(self):
        """Ko'rishlar sonini oshirish"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
```

**Migration:**
```bash
python manage.py makemigrations news
python manage.py migrate
```

**Tekshirish:** News modeli to'liq ishlashi va barcha maydonlar to'g'ri ko'rinishi.

---

#### 5. Vazifa: Admin panel sozlash
**Maqsad:** Professional admin interface yaratish

**Bajarilishi kerak:**
```python
# news/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Tag, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin konfiguratsiyasi"""
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
    list_editable = ['is_active']  # Ro'yxatda o'zgartirish
    
    def color_display(self, obj):
        """Rangni ko'rsatish"""
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_display.short_description = 'Rang'

    def news_count(self, obj):
        """Yangiliklar soni ko'rsatish"""
        return obj.get_news_count()
    news_count.short_description = 'Yangiliklar'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin konfiguratsiyasi"""
    list_display = ['name', 'slug', 'news_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def news_count(self, obj):
        return obj.get_news_count()
    news_count.short_description = 'Yangiliklar'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """News admin konfiguratsiyasi"""
    list_display = [
        'title',
        'category',
        'author',
        'status_display',
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
    filter_horizontal = ['tags']  # M2M uchun qulay interface
    list_editable = ['status', 'is_featured', 'priority']
    list_per_page = 20
    date_hierarchy = 'publish_date'  # Sana bo'yicha navigatsiya

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Kategoriya va teglar', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)  # Yig'ilgan holda
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
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

    def status_display(self, obj):
        """Status'ni rangli ko'rsatish"""
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_display.short_description = 'Holat'

    def save_model(self, request, obj, form, change):
        """Yangi obyekt yaratilayotganda muallifni o'rnatish"""
        if not change:  # Yangi obyekt
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Optimallashtirilgan queryset"""
        return super().get_queryset(request).select_related(
            'category', 'author'
        ).prefetch_related('tags')

# Admin site sozlamalari
admin.site.site_header = "Yangiliklar boshqaruvi"
admin.site.site_title = "News Admin"
admin.site.index_title = "Boshqaruv paneli"
```

**Superuser yaratish:**
```bash
python manage.py createsuperuser
# Username, email, password kiritish
```

**Tekshirish:** Admin panelda barcha model'lar professional ko'rinishi.

---

#### 6. Vazifa: URL routing sozlash
**Maqsad:** To'liq URL tizimini yaratish

**Bajarilishi kerak:**

**Asosiy URLs (news_project/urls.py):**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # Asosiy sahifa news app'ga
]

# Media fayllar uchun (development)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
```

**News app URLs (news/urls.py - yangi fayl yarating):**
```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Asosiy sahifa - yangiliklar ro'yxati
    path('', views.news_list, name='news_list'),
    
    # Yangilik detail sahifasi
    path(
        'news/<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.news_detail,
        name='news_detail'
    ),
    
    # Kategoriya sahifasi
    path(
        'category/<slug:slug>/', 
        views.category_detail, 
        name='category_detail'
    ),
    
    # Tag sahifasi
    path(
        'tag/<slug:slug>/', 
        views.tag_detail, 
        name='tag_detail'
    ),
    
    # Qidiruv sahifasi
    path('search/', views.search_news, name='search_news'),
    
    # API endpoints (kelajakda)
    # path('api/', include('news.api.urls')),
]
```

**Tekshirish:** URL'lar to'g'ri sozlangani tekshirish.

---

### Murakkab vazifalar

#### 7. Vazifa: Views yaratish
**Maqsad:** Barcha sahifalar uchun view'lar yaratish

**Bajarilishi kerak:**
```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import Http404
from .models import News, Category, Tag

def news_list(request):
    """
    Asosiy sahifa - barcha yangiliklar
    """
    # Yangiliklar ro'yxati (optimized query)
    news_list = News.objects.filter(
        is_published=True
    ).select_related('category', 'author').prefetch_related('tags')
    
    # Pagination - sahifalash
    paginator = Paginator(news_list, 12)  # 12 ta yangilik har sahifada
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Featured yangiliklar (asosiy yangiliklar)
    featured_news = News.objects.filter(
        is_published=True, 
        is_featured=True
    ).select_related('category', 'author')[:5]
    
    # Kategoriyalar
    categories = Category.objects.filter(
        is_active=True
    ).annotate(
        news_count=Count('news', filter=Q(news__is_published=True))
    )
    
    # Mashhur teglar
    popular_tags = Tag.objects.annotate(
        news_count=Count('news', filter=Q(news__is_published=True))
    ).filter(news_count__gt=0).order_by('-news_count')[:10]
    
    context = {
        'page_obj': page_obj,
        'featured_news': featured_news,
        'categories': categories,
        'popular_tags': popular_tags,
        'total_news': news_list.count(),
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, year, month, day, slug):
    """
    Yangilik detail sahifasi
    """
    # Yangilikni topish
    news = get_object_or_404(
        News.objects.select_related('category', 'author').prefetch_related('tags'),
        slug=slug,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
        is_published=True
    )
    
    # Ko'rishlar sonini oshirish
    news.increment_views()
    
    # O'xshash yangiliklar (bir xil kategoriya)
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id).select_related('category', 'author')[:4]
    
    # Oldingi va keyingi yangilik
    try:
        previous_news = News.objects.filter(
            publish_date__lt=news.publish_date,
            is_published=True
        ).select_related('category').first()
    except News.DoesNotExist:
        previous_news = None
    
    try:
        next_news = News.objects.filter(
            publish_date__gt=news.publish_date,
            is_published=True
        ).select_related('category').last()
    except News.DoesNotExist:
        next_news = None
    
    context = {
        'news': news,
        'related_news': related_news,
        'previous_news': previous_news,
        'next_news': next_news,
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
    
    # Pagination
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'total_news': news_list.count(),
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
    
    # Pagination
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'total_news': news_list.count(),
    }
    return render(request, 'news/tag_detail.html', context)

def search_news(request):
    """
    Yangiliklar qidiruvi
    """
    query = request.GET.get('q', '').strip()
    results = []
    total_results = 0
    
    if query and len(query) >= 3:  # Kamida 3 belgi
        results = News.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query),
            is_published=True
        ).select_related('category', 'author').distinct()
        
        total_results = results.count()
        
        # Pagination
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': total_results,
    }
    return render(request, 'news/search_results.html', context)
```

**Tekshirish:** Barcha view'lar ishlashi va ma'lumotlar to'g'ri uzatilishi.

---

#### 8. Vazifa: Dastlabki ma'lumotlar yaratish
**Maqsad:** Test ma'lumotlari bilan to'ldirish

**Bajarilishi kerak:**
```python
# Django shell: python manage.py shell

# 1. Kategoriyalar yaratish
from news.models import Category, Tag, News
from django.contrib.auth.models import User

categories_data = [
    {
        'name': 'Siyosat', 
        'description': 'Siyosiy yangiliklar va voqealar', 
        'color': '#dc3545'
    },
    {
        'name': 'Sport', 
        'description': 'Sport yangiliklar va natijalar', 
        'color': '#28a745'
    },
    {
        'name': 'Texnologiya', 
        'description': 'IT va texnologiya yangiliklar', 
        'color': '#007bff'
    },
    {
        'name': 'Iqtisodiyot', 
        'description': 'Moliya va biznes yangiliklar', 
        'color': '#ffc107'
    },
    {
        'name': 'Madaniyat', 
        'description': 'San\'at va madaniyat yangiliklar', 
        'color': '#6f42c1'
    },
    {
        'name': 'Ta\'lim', 
        'description': 'Ta\'lim sohasidagi yangiliklar', 
        'color': '#fd7e14'
    }
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"Kategoriya yaratildi: {category.name}")

# 2. Teglar yaratish
tags_data = [
    'yangi', 'muhim', 'so\'nggi', 'mashhur', 'tez', 'eksklyuziv',
    'rasmiy', 'tahlil', 'sport', 'futbol', 'dasturlash', 'sun\'iy-aql',
    'biznes', 'startap', 'innovatsiya', 'fan', 'tadqiqot', 'sog\'liq'
]

for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        print(f"Teg yaratildi: {tag.name}")

# 3. Test yangiliklar yaratish
user = User.objects.first()  # Admin user
if not user:
    user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

# Test yangiliklar ma'lumotlari
news_data = [
    {
        'title': 'Python dasturlashda yangi imkoniyatlar',
        'summary': 'Python 3.12 versiyasida qo\'shilgan yangi funksiyalar va optimizatsiyalar haqida batafsil ma\'lumot.',
        'content': '''
        Python dasturlash tilining 3.12 versiyasi chiqdi va u bilan birga ko'plab yangi imkoniyatlar keldi.
        
        **Asosiy yangiliklar:**
        - Tezlik 15% ga oshdi
        - Yangi sintaksis qo'shildi
        - Xotira iste'moli kamaytirildi
        - Type hints yaxshilandi
        
        Bu yangiliklar Python dasturchilar jamoasi uchun katta yutuq hisoblanadi.
        ''',
        'category': 'Texnologiya',
        'tags': ['yangi', 'dasturlash', 'muhim'],
        'is_featured': True
    },
    {
        'title': 'Futbol Jahon Chempionati yangiliklari',
        'summary': 'Futbol bo\'yicha so\'nggi natijalar va kelgusi o\'yinlar jadvali.',
        'content': '''
        Futbol Jahon Chempionatida hayajonli o'yinlar davom etmoqda.
        
        **So'nggi natijalar:**
        - Argentina vs Braziliya: 2-1
        - Ispaniya vs Italiya: 1-0
        - Germaniya vs Fransiya: 3-2
        
        Keyingi bosqichda qiziq o'yinlar kutilmoqda.
        ''',
        'category': 'Sport',
        'tags': ['sport', 'futbol', 'so\'nggi'],
        'is_featured': True
    },
    {
        'title': 'Sun\'iy aql sohasida yangi kashfiyot',
        'summary': 'ChatGPT-dan ham kuchli yangi AI model yaratildi.',
        'content': '''
        Sun'iy aql sohasida navbatdagi katta qadam tashlandi.
        
        **Yangi model imkoniyatlari:**
        - Tez javob berish
        - Ko'p tilda gaplashish
        - Murakkab masalalarni yechish
        - Kreativ yozish
        
        Bu texnologiya kelajakda ko'p sohalarda qo'llanilishi kutilmoqda.
        ''',
        'category': 'Texnologiya',
        'tags': ['sun\'iy-aql', 'innovatsiya', 'fan'],
        'is_featured': False
    },
    {
        'title': 'Startup kompaniyalar uchun yangi dastur',
        'summary': 'Hukumat startup'lar uchun moliyaviy yordam dasturini e'lon qildi.',
        'content': '''
        Hukumat tomonidan startup kompaniyalar uchun keng ko'lamli yordam dasturi e'lon qilindi.
        
        **Dastur shartlari:**
        - 100 ming dollarcha grant
        - Bepul maslahat xizmatlari
        - Ofis joyi taqdim etish
        - Mentorlik dasturi
        
        Ariza berish jarayoni kelgusi hafta boshlanadi.
        ''',
        'category': 'Iqtisodiyot',
        'tags': ['biznes', 'startap', 'yangi'],
        'is_featured': False
    },
    {
        'title': 'Ta\'limda raqamli texnologiyalar',
        'summary': 'Maktablarda yangi texnologiyalar joriy etilmoqda.',
        'content': '''
        Ta'lim tizimida raqamli transformatsiya davom etmoqda.
        
        **Joriy etiladigan texnologiyalar:**
        - Interaktiv doskalar
        - VR/AR texnologiyalari
        - Online ta'lim platformalari
        - AI yordamchilari
        
        Bu o'zgarishlar ta'lim sifatini sezilarli darajada oshirishi kutilmoqda.
        ''',
        'category': 'Ta\'lim',
        'tags': ['ta\'lim', 'texnologiya', 'innovatsiya'],
        'is_featured': False
    }
]

# Yangiliklar yaratish
for news_item in news_data:
    # Kategoriyani topish
    try:
        category = Category.objects.get(name=news_item['category'])
    except Category.DoesNotExist:
        category = None
    
    # Yangilik yaratish
    news = News.objects.create(
        title=news_item['title'],
        summary=news_item['summary'],
        content=news_item['content'],
        category=category,
        author=user,
        status='published',
        is_featured=news_item['is_featured']
    )
    
    # Teglarni qo'shish
    for tag_name in news_item['tags']:
        try:
            tag = Tag.objects.get(name=tag_name)
            news.tags.add(tag)
        except Tag.DoesNotExist:
            pass
    
    print(f"Yangilik yaratildi: {news.title}")

print(f"\nJami yaratildi:")
print(f"- Kategoriyalar: {Category.objects.count()}")
print(f"- Teglar: {Tag.objects.count()}")
print(f"- Yangiliklar: {News.objects.count()}")
```

**Manual test qilish:**
```bash
# 1. Server ishga tushirish
python manage.py runserver

# 2. Admin panelga kirish
# http://127.0.0.1:8000/admin/

# 3. Ma'lumotlarni tekshirish
# - Categories bo'limini ochish
# - News bo'limini ochish
# - Yangi yangilik qo'shib ko'rish
```

**Tekshirish:** Ma'lumotlar bazasi test ma'lumotlari bilan to'ldirilgan va admin panelda ko'rinadi.

---

#### 9. Vazifa: Media fayllar bilan ishlash
**Maqsad:** Rasm yuklash va ko'rsatishni sozlash

**Bajarilishi kerak:**

**1. Media papkalarini yaratish:**
```bash
# Loyiha papkasida
mkdir media
mkdir media/news
mkdir media/news/images
```

**2. Settings.py da media sozlamalari:**
```python
# news_project/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Media fayllar sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Rasm yuklash uchun cheklovlar
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
```

**3. URL konfiguratsiyasi (development):**
```python
# news_project/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]

# Development rejimida media fayllar
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
```

**4. Model'da rasm maydonini sozlash:**
```python
# news/models.py (News modelida allaqachon bor)
featured_image = models.ImageField(
    upload_to='news/images/%Y/%m/%d/',  # Sana bo'yicha papkalar
    blank=True,
    null=True,
    help_text="Asosiy rasm (tavsiya: 1200x630px)",
    verbose_name="Asosiy rasm"
)

def get_image_url(self):
    """Rasm URL'ini olish"""
    if self.featured_image:
        return self.featured_image.url
    return '/static/images/default-news.jpg'  # Default rasm
```

**5. Admin panelda rasm preview:**
```python
# news/admin.py (NewsAdmin klassiga qo'shing)
from django.utils.html import format_html

class NewsAdmin(admin.ModelAdmin):
    # ... mavjud kodlar
    
    readonly_fields = ['image_preview']  # Faqat ko'rish uchun
    
    def image_preview(self, obj):
        """Admin panelda rasm preview"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.featured_image.url
            )
        return "Rasm yuklanmagan"
    image_preview.short_description = 'Rasm ko\'rinishi'
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_preview'),
            'classes': ('collapse',)
        }),
        # ... qolgan fieldsets
    )
```

**6. Test rasm yuklash:**
```python
# Django shell orqali
from news.models import News
from django.core.files import File
from django.contrib.auth.models import User

# Birinchi yangilikni olish
news = News.objects.first()
if news:
    print(f"Yangilik: {news.title}")
    print(f"Rasm: {news.get_image_url()}")
```

**Tekshirish:** Admin panelda yangilik yaratishda rasm yuklash ishlashi.

---

#### 10. Vazifa: Advanced model methods
**Maqsad:** Model'larga qo'shimcha funksiyalar qo'shish

**Bajarilishi kerak:**

**1. News modeliga qo'shimcha methodlar:**
```python
# news/models.py (News klassiga qo'shing)

class News(models.Model):
    # ... mavjud fieldlar
    
    def get_related_news(self, count=5):
        """O'xshash yangiliklar"""
        return News.objects.filter(
            category=self.category,
            is_published=True
        ).exclude(id=self.id)[:count]
    
    def get_previous_news(self):
        """Oldingi yangilik"""
        return News.objects.filter(
            publish_date__lt=self.publish_date,
            is_published=True
        ).order_by('-publish_date').first()
    
    def get_next_news(self):
        """Keyingi yangilik"""
        return News.objects.filter(
            publish_date__gt=self.publish_date,
            is_published=True
        ).order_by('publish_date').first()
    
    @property
    def is_recent(self):
        """So'nggi 7 kun ichida yaratilganmi?"""
        from django.utils import timezone
        from datetime import timedelta
        
        return (timezone.now() - self.publish_date) <= timedelta(days=7)
    
    @property
    def reading_time_text(self):
        """O'qish vaqtini matn ko'rinishida"""
        time = self.get_reading_time()
        return f"{time} daqiqa o'qish"
    
    def get_excerpt(self, words=30):
        """Ma'lum so'z miqdori bilan qisqacha"""
        content_words = self.content.split()
        if len(content_words) <= words:
            return self.content
        return ' '.join(content_words[:words]) + '...'
    
    def get_word_count(self):
        """So'zlar soni"""
        return len(self.content.split())
    
    @classmethod
    def get_featured(cls, count=5):
        """Featured yangiliklar (class method)"""
        return cls.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-publish_date')[:count]
    
    @classmethod 
    def get_popular(cls, count=10):
        """Mashhur yangiliklar (ko'rishlar bo'yicha)"""
        return cls.objects.filter(
            is_published=True
        ).order_by('-views_count')[:count]
```

**2. Category modeliga qo'shimcha methodlar:**
```python
# news/models.py (Category klassiga qo'shing)

class Category(models.Model):
    # ... mavjud fieldlar
    
    def get_latest_news(self, count=5):
        """Eng so'nggi yangiliklar"""
        return self.news.filter(
            is_published=True
        ).order_by('-publish_date')[:count]
    
    def get_popular_news(self, count=5):
        """Mashhur yangiliklar"""
        return self.news.filter(
            is_published=True
        ).order_by('-views_count')[:count]
    
    @property
    def total_views(self):
        """Kategoriya bo'yicha jami ko'rishlar"""
        from django.db.models import Sum
        return self.news.filter(
            is_published=True
        ).aggregate(
            total=Sum('views_count')
        )['total'] or 0
```

**3. Tag modeliga qo'shimcha methodlar:**
```python
# news/models.py (Tag klassiga qo'shing)

class Tag(models.Model):
    # ... mavjud fieldlar
    
    def get_latest_news(self, count=5):
        """Eng so'nggi yangiliklar"""
        return self.news.filter(
            is_published=True
        ).order_by('-publish_date')[:count]
    
    @classmethod
    def get_popular_tags(cls, count=10):
        """Mashhur teglar"""
        from django.db.models import Count
        return cls.objects.annotate(
            news_count=Count('news', filter=Q(news__is_published=True))
        ).filter(news_count__gt=0).order_by('-news_count')[:count]
```

**4. Custom Managers yaratish:**
```python
# news/models.py (tepasiga qo'shing)

class PublishedManager(models.Manager):
    """Faqat nashr qilingan yangiliklar uchun manager"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class FeaturedManager(models.Manager):
    """Featured yangiliklar uchun manager"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True, is_featured=True)

class News(models.Model):
    # ... mavjud fieldlar
    
    # Custom managers
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Faqat published
    featured = FeaturedManager()  # Faqat featured
    
    # ... qolgan kod

# Foydalanish:
# News.published.all()  # Faqat published yangiliklar
# News.featured.all()   # Faqat featured yangiliklar
# News.objects.all()    # Barcha yangiliklar
```

**5. Test qilish:**
```python
# Django shell: python manage.py shell
from news.models import News, Category, Tag

# Method'larni test qilish
news = News.objects.first()
if news:
    print(f"Reading time: {news.reading_time_text}")
    print(f"Is recent: {news.is_recent}")
    print(f"Word count: {news.get_word_count()}")
    print(f"Excerpt: {news.get_excerpt(20)}")
    
    # Related news
    related = news.get_related_news(3)
    print(f"Related news count: {related.count()}")

# Custom managers
featured_news = News.featured.all()
print(f"Featured news count: {featured_news.count()}")

published_news = News.published.all()
print(f"Published news count: {published_news.count()}")
```

**Tekshirish:** Barcha yangi method'lar to'g'ri ishlashi.

---

#### 11. Bonus: Custom Admin Actions
**Maqsad:** Admin panelda bulk operations qo'shish

**Bajarilishi kerak:**
```python
# news/admin.py ga qo'shing

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # ... mavjud kodlar
    
    actions = [
        'make_published',
        'make_draft', 
        'make_featured',
        'remove_featured',
        'reset_views'
    ]
    
    def make_published(self, request, queryset):
        """Tanlanganlarni publish qilish"""
        updated = queryset.update(status='published', is_published=True)
        self.message_user(
            request,
            f'{updated} ta yangilik nashr qilindi.'
        )
    make_published.short_description = "Tanlangan yangiliklarni nashr qilish"
    
    def make_draft(self, request, queryset):
        """Tanlanganlarni draft qilish"""
        updated = queryset.update(status='draft', is_published=False)
        self.message_user(
            request,
            f'{updated} ta yangilik qoralama qilindi.'
        )
    make_draft.short_description = "Tanlangan yangiliklarni qoralama qilish"
    
    def make_featured(self, request, queryset):
        """Tanlanganlarni featured qilish"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} ta yangilik asosiy qilindi.'
        )
    make_featured.short_description = "Asosiy yangilik qilish"
    
    def remove_featured(self, request, queryset):
        """Featured'dan olib tashlash"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{updated} ta yangilik asosiydan olib tashlandi.'
        )
    remove_featured.short_description = "Asosiydan olib tashlash"
    
    def reset_views(self, request, queryset):
        """Ko'rishlar sonini 0 ga tushirish"""
        updated = queryset.update(views_count=0)
        self.message_user(
            request,
            f'{updated} ta yangilik ko\'rishlar soni nolandi.'
        )
    reset_views.short_description = "Ko'rishlar sonini nolash"
```

---

#### 12. Bonus: Database Optimization
**Maqsad:** Database query'larni optimizatsiya qilish

**Bajarilishi kerak:**
```python
# news/models.py ga qo'shing

class OptimizedNewsQuerySet(models.QuerySet):
    """Optimizatsiya qilingan QuerySet"""
    
    def published(self):
        return self.filter(is_published=True)
    
    def featured(self):
        return self.filter(is_featured=True)
    
    def by_category(self, category):
        return self.filter(category=category)
    
    def recent(self, days=7):
        from django.utils import timezone
        from datetime import timedelta
        date_from = timezone.now() - timedelta(days=days)
        return self.filter(publish_date__gte=date_from)
    
    def with_related(self):
        """Related obyektlar bilan"""
        return self.select_related('category', 'author').prefetch_related('tags')
    
    def popular(self):
        """Mashhur yangiliklar (ko'rishlar bo'yicha)"""
        return self.order_by('-views_count')
    
    def search(self, query):
        """Qidiruv"""
        from django.db.models import Q
        return self.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        )

class News(models.Model):
    # ... mavjud fieldlar
    
    objects = OptimizedNewsQuerySet.as_manager()
    
    # ... qolgan kod

# Foydalanish:
# News.objects.published().featured().with_related()
# News.objects.recent(30).popular()[:10]
# News.objects.search('python').published()
```

---

### Asosiy funksionallik:
- [ ] Django loyiha yaratilgan va sozlangan
- [ ] Category modeli to'liq ishlaydi
- [ ] Tag modeli to'liq ishlaydi  
- [ ] News modeli barcha maydonlar bilan
- [ ] Admin panel professional ko'rinishda
- [ ] URL routing to'g'ri sozlangan

### Views va ma'lumotlar:
- [ ] Barcha view'lar to'g'ri ishlaydi
- [ ] Pagination qo'shilgan
- [ ] Test ma'lumotlari yaratilgan
- [ ] Media files yuklash ishlaydi
- [ ] Advanced model methods qo'shilgan

### Bonus:
- [ ] Admin actions ishlaydi
- [ ] Query optimization qo'shilgan
- [ ] Custom managers yaratilgan


### Loyiha struktura:
```
news_project/
├── news_project/
│   ├── settings.py     # Sozlamalar
│   ├── urls.py         # Asosiy URLs  
├── news/
│   ├── models.py       # Barcha modellar
│   ├── admin.py        # Admin konfiguratsiya
│   ├── views.py        # Barcha view'lar
│   ├── urls.py         # News app URLs
├── media/              # Media fayllar
└── db.sqlite3          # Ma'lumotlar bazasi
```

## O'rnatish va ishga tushirish

```bash
# 1. Repository clone qilish
git clone <repo-url>
cd news_project

# 2. Virtual environment
python -m venv news_env
news_env\Scripts\activate  # Windows
# source news_env/bin/activate  # macOS/Linux

# 3. Dependencies o'rnatish  
pip install -r requirements.txt

# 4. Database setup
python manage.py migrate
python manage.py createsuperuser

# 5. Test data yuklash
python manage.py shell
# Shell'da yuqoridagi test data kodni ishga tushiring

# 6. Server ishga tushirish
python manage.py runserver
```
 
**Umumiy xatolar:**
- Migration muammolari - `python manage.py migrate --run-syncdb`
- Media fayllar ko'rsatilmaslik - URL konfiguratsiya tekshirish
- Admin panelda model ko'rinmaslik - admin.py da registration tekshirish
