# Django Admin - Amaliy Mashg'ulot (Practice)

## Loyiha: Blog Admin Paneli Yaratish

Ushbu amaliy mashg'ulotda biz to'liq blog admin paneli yaratamiz va barcha xususiyatlarni amalda qo'llaymiz.

## 1-Bosqich: Loyihani Tayyorlash

### Yangi Django loyihasi yaratish:

```bash
# Yangi loyiha yaratish
django-admin startproject blogproject
cd blogproject

# Yangi app yaratish
python manage.py startapp blog

# Virtual environment yaratish (agar yo'q bo'lsa)
python -m venv venv
# Windows uchun:
venv\Scripts\activate
# Linux/Mac uchun:
source venv/bin/activate

# Django o'rnatish
pip install django
```

### Settings.py ni sozlash:

```python
# blogproject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Bizning appimiz
]

# O'zbek tili uchun
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_TZ = True
```

## 2-Bosqich: Blog Modellarini Yaratish

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, verbose_name="URL nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tag nomi")
    slug = models.SlugField(unique=True, verbose_name="URL nomi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Taglar"

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Nashr qilingan'),
        ('archived', 'Arxivlangan'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, verbose_name="URL nomi")
    content = models.TextField(verbose_name="Kontent")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="Qisqa matn")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Taglar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Holat")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Muhimlik")
    featured = models.BooleanField(default=False, verbose_name="Asosiy")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Yoqtirishlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Nashr qilingan vaqt")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    def short_content(self):
        return self.content[:150] + "..." if len(self.content) > 150 else self.content
    short_content.short_description = "Qisqa kontent"
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author_name = models.CharField(max_length=100, verbose_name="Muallif ismi")
    author_email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Izoh")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    
    def __str__(self):
        return f"{self.author_name} - {self.post.title[:30]}"
    
    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']

class BlogSettings(models.Model):
    site_title = models.CharField(max_length=200, verbose_name="Sayt sarlavhasi")
    site_description = models.TextField(verbose_name="Sayt tavsifi")
    posts_per_page = models.PositiveIntegerField(default=10, verbose_name="Sahifadagi postlar soni")
    allow_comments = models.BooleanField(default=True, verbose_name="Izohlarga ruxsat")
    moderate_comments = models.BooleanField(default=True, verbose_name="Izohlarni modereratsiya qilish")
    
    def __str__(self):
        return "Blog Sozlamalari"
    
    class Meta:
        verbose_name = "Blog Sozlamasi"
        verbose_name_plural = "Blog Sozlamalari"
```

## 3-Bosqich: Migration va Database

```bash
# Migrationlarni yaratish
python manage.py makemigrations blog

# Ma'lumotlar bazasini yaratish
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser
# Username: admin
# Email: admin@blog.com
# Password: admin123456
```

## 4-Bosqich: Admin.py ni To'liq Sozlash

```python
# blog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Category, Tag, Post, Comment, BlogSettings

# Admin paneli sarlavhalarini o'zgartirish
admin.site.site_header = "Blog Admin Paneli"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Blog Boshqaruv Paneli"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'post_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    list_editable = ['is_active']
    
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Sozlamalar', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        count = obj.post_set.count()
        return count
    post_count.short_description = "Postlar soni"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "Postlar soni"

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author_name', 'author_email', 'content', 'created_at']
    can_delete = True
    fields = ['author_name', 'content', 'is_approved', 'created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'status', 
        'priority', 'featured', 'views_count', 
        'likes_count', 'comment_count', 'created_at'
    ]
    list_filter = [
        'status', 'priority', 'featured', 'category', 
        'created_at', 'updated_at', 'author'
    ]
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25
    list_editable = ['status', 'priority', 'featured']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    
    inlines = [CommentInline]
    
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Kontent', {
            'fields': ('excerpt', 'content', 'tags')
        }),
        ('Sozlamalar', {
            'fields': ('status', 'priority', 'featured'),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Vaqt Ma\'lumotlari', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    radio_fields = {'status': admin.HORIZONTAL, 'priority': admin.HORIZONTAL}
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category').prefetch_related('tags')
    
    def comment_count(self, obj):
        count = obj.comments.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return count
    comment_count.short_description = "Izohlar"
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(
            request,
            f'{updated} ta post nashr qilindi.',
        )
    make_published.short_description = "Tanlangan postlarni nashr qilish"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(
            request,
            f'{updated} ta post qoralama holatiga o\'tkazildi.',
        )
    make_draft.short_description = "Tanlangan postlarni qoralama qilish"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(
            request,
            f'{updated} ta post asosiy qilib belgilandi.',
        )
    make_featured.short_description = "Tanlangan postlarni asosiy qilish"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'short_content', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['author_name', 'author_email', 'content', 'post__title']
    list_per_page = 30
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Muallif Ma\'lumotlari', {
            'fields': ('author_name', 'author_email')
        }),
        ('Izoh', {
            'fields': ('post', 'content')
        }),
        ('Modereratsiya', {
            'fields': ('is_approved',)
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Qisqa izoh"
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} ta izoh tasdiqlandi.',
        )
    approve_comments.short_description = "Tanlangan izohlarni tasdiqlash"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated} ta izohing tasdigi bekor qilindi.',
        )
    unapprove_comments.short_description = "Tanlangan izohlar tasdiqini bekor qilish"

@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Faqat bitta sozlama obyekti bo'lishi kerak
        return not BlogSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Sozlamani o'chirib bo'lmaydi
        return False
    
    fieldsets = (
        ('Sayt Ma\'lumotlari', {
            'fields': ('site_title', 'site_description')
        }),
        ('Ko\'rinish Sozlamalari', {
            'fields': ('posts_per_page',)
        }),
        ('Izoh Sozlamalari', {
            'fields': ('allow_comments', 'moderate_comments')
        }),
    )
```

## 5-Bosqich: URL Konfiguratsiyasi

```python
# blogproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

# blog/urls.py (yangi fayl yaratish kerak)
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    # Boshqa URLlar keyinchalik qo'shiladi
]

# blog/views.py (oddiy view yaratish)
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Blog sahifasi")
```

## 6-Bosqich: Test Ma'lumotlarini Qo'shish

Django shell orqali test ma'lumotlari qo'shing:

```bash
python manage.py shell
```

```python
# Shell ichida
from blog.models import Category, Tag, Post, Comment, BlogSettings
from django.contrib.auth.models import User

# Kategoriyalar yaratish
cat1 = Category.objects.create(
    name="Texnologiya", 
    slug="texnologiya", 
    description="Texnologik yangiliklar"
)
cat2 = Category.objects.create(
    name="Sport", 
    slug="sport", 
    description="Sport yangiliklari"
)

# Taglar yaratish
tag1 = Tag.objects.create(name="Django", slug="django")
tag2 = Tag.objects.create(name="Python", slug="python")
tag3 = Tag.objects.create(name="Web Development", slug="web-development")

# Foydalanuvchi yaratish (agar yo'q bo'lsa)
user = User.objects.get(username='admin')  # Yoki yangi user yaratish

# Postlar yaratish
post1 = Post.objects.create(
    title="Django Admin bilan ishlash",
    slug="django-admin-bilan-ishlash",
    content="Bu Django admin paneli haqida batafsil maqola...",
    excerpt="Django admin panelini o'rganish",
    author=user,
    category=cat1,
    status='published'
)
post1.tags.add(tag1, tag2)

post2 = Post.objects.create(
    title="Python dasturlash tili",
    slug="python-dasturlash-tili",
    content="Python dasturlash tili haqida...",
    excerpt="Python asoslari",
    author=user,
    category=cat1,
    status='draft'
)

# Izohlar yaratish
Comment.objects.create(
    post=post1,
    author_name="Ali Valiyev",
    author_email="ali@example.com",
    content="Ajoyib maqola! Rahmat!",
    is_approved=True
)

Comment.objects.create(
    post=post1,
    author_name="Dilnoza Karimova",
    author_email="dilnoza@example.com",
    content="Juda foydali ma'lumotlar",
    is_approved=False
)

# Blog sozlamalarini yaratish
BlogSettings.objects.create(
    site_title="Mening Blog Saytim",
    site_description="Bu yerda turli mavzularda maqolalar joylashtiriladi",
    posts_per_page=5,
    allow_comments=True,
    moderate_comments=True
)

print("Test ma'lumotlari muvaffaqiyatli qo'shildi!")
```

## 7-Bosqich: Admin Panelni Sinovdan O'tkazish

### Server ishga tushirish:

```bash
python manage.py runserver
```

### Admin panelga kirish:
1. Brauzerda `http://127.0.0.1:8000/admin/` ga o'ting
2. Username va parolni kiriting
3. Admin panelni ko'ring

### Sinovdan o'tkaziladigan imkoniyatlar:

**Kategoriyalar bo'limida:**
- Yangi kategoriya qo'shish
- Kategoriyalarni tahrirlash
- Slug maydonining avtomatik to'ldirilishini tekshirish
- Faol/nofaol holatini o'zgartirish
- Kategoriyalardagi postlar sonini ko'rish

**Postlar bo'limida:**
- Yangi post yaratish
- Postlarni turli holatga o'tkazish (draft, published, archived)
- Taglarni qo'shish va o'chirish
- Inline izohlarni ko'rish va boshqarish
- Bulk actions (ommaviy amallar)ni sinash
- Filtrlar va qidiruv funksiyasini sinash

**Izohlar bo'limida:**
- Izohlarni tasdiqlash/rad etish
- Izohlarni filtrlab ko'rish
- Ommaviy tasdiqlash amalini sinash

## 8-Bosqich: Advanced Customization

### Custom Admin Dashboard yaratish:

```python
# blog/admin.py ga qo'shimcha
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class BlogAdminSite(AdminSite):
    site_header = "Blog Boshqaruv Paneli"
    site_title = "Blog Admin"
    index_title = "Dashboard"
    
    def index(self, request, extra_context=None):
        # Statistika ma'lumotlarini yig'ish
        extra_context = extra_context or {}
        
        # Postlar statistikasi
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()
        
        # Izohlar statistikasi
        total_comments = Comment.objects.count()
        pending_comments = Comment.objects.filter(is_approved=False).count()
        
        # Oxirgi 30 kun ichidagi postlar
        last_30_days = timezone.now() - timedelta(days=30)
        recent_posts = Post.objects.filter(created_at__gte=last_30_days).count()
        
        # Eng ko'p ko'rilgan postlar
        popular_posts = Post.objects.filter(status='published').order_by('-views_count')[:5]
        
        extra_context.update({
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'recent_posts': recent_posts,
            'popular_posts': popular_posts,
        })
        
        return super().index(request, extra_context)

# Custom admin site yaratish
blog_admin_site = BlogAdminSite(name='blog_admin')

# Modellarni custom admin sitega ro'yxatdan o'tkazish
blog_admin_site.register(Post, PostAdmin)
blog_admin_site.register(Category, CategoryAdmin)
blog_admin_site.register(Tag, TagAdmin)
blog_admin_site.register(Comment, CommentAdmin)
blog_admin_site.register(BlogSettings, BlogSettingsAdmin)
blog_admin_site.register(User, UserAdmin)
blog_admin_site.register(Group, GroupAdmin)
```

### Custom Admin Template yaratish:

```html
<!-- blog/templates/admin/index.html -->
{% extends "admin/index.html" %}
{% load i18n static %}

{% block content %}
<div class="row">
    <div class="col-md-3">
        <div class="card text-white bg-primary mb-3">
            <div class="card-header">Jami Postlar</div>
            <div class="card-body">
                <h4 class="card-title">{{ total_posts }}</h4>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success mb-3">
            <div class="card-header">Nashr qilingan</div>
            <div class="card-body">
                <h4 class="card-title">{{ published_posts }}</h4>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning mb-3">
            <div class="card-header">Qoralama</div>
            <div class="card-body">
                <h4 class="card-title">{{ draft_posts }}</h4>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-danger mb-3">
            <div class="card-header">Kutilayotgan izohlar</div>
            <div class="card-body">
                <h4 class="card-title">{{ pending_comments }}</h4>
            </div>
        </div>
    </div>
</div>

{% if popular_posts %}
<div class="row mt-4">
    <div class="col-12">
        <h3>Eng mashhur postlar</h3>
        <div class="list-group">
            {% for post in popular_posts %}
            <div class="list-group-item">
                <strong>{{ post.title }}</strong>
                <span class="badge badge-primary">{{ post.views_count }} ko'rildi</span>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}

{{ block.super }}
{% endblock %}
```

## 9-Bosqich: Ma'lumotlarni Import/Export

### CSV Export funksiyasi qo'shish:

```python
# blog/admin.py ga qo'shimcha import
import csv
from django.http import HttpResponse

def export_posts_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Sarlavha', 'Muallif', 'Kategoriya', 'Holat', 'Yaratilgan'])
    
    for post in queryset:
        writer.writerow([
            post.title,
            post.author.username,
            post.category.name,
            post.get_status_display(),
            post.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

export_posts_csv.short_description = "Tanlangan postlarni CSV ga export qilish"

# PostAdmin klassiga qo'shish
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ... mavjud kodlar
    actions = ['make_published', 'make_draft', 'make_featured', 'export_posts_csv']
    
    # Custom method qo'shish
    def export_posts_csv(self, request, queryset):
        return export_posts_csv(self, request, queryset)
```

## 10-Bosqich: Xavfsizlik Sozlamalari

### Admin paneli xavfsizligini kuchaytirish:

```python
# blogproject/settings.py ga qo'shimcha
import os

# Admin paneli uchun maxsus URL
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')

# Session xavfsizligi
SESSION_COOKIE_SECURE = True  # HTTPS da ishlatish uchun
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# Admin panelga kirish uchun IP cheklash (ixtiyoriy)
ALLOWED_ADMIN_IPS = ['127.0.0.1', '::1']  # Faqat local access
```

### Custom Login Required Decorator:

```python
# blog/decorators.py (yangi fayl)
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.conf import settings

def admin_ip_restriction(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        if hasattr(settings, 'ALLOWED_ADMIN_IPS'):
            if ip not in settings.ALLOWED_ADMIN_IPS:
                raise PermissionDenied("Access denied from this IP")
        return view_func(request, *args, **kwargs)
    return wrapper
```

## 11-Bosqich: Performance Monitoring

### Admin paneli performance ni kuzatish:

```python
# blog/admin.py ga qo'shimcha
from django.db import connection
from django.contrib.admin.views.main import ChangeList

class OptimizedChangeList(ChangeList):
    def get_results(self, request):
        # Query larni sanash
        query_count_before = len(connection.queries)
        result = super().get_results(request)
        query_count_after = len(connection.queries)
        
        print(f"Admin changelist queries: {query_count_after - query_count_before}")
        return result

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ... mavjud kodlar
    
    def get_changelist(self, request, **kwargs):
        return OptimizedChangeList
```

## Xulosa va Sinov

### Yaratilgan Admin Panel Imkoniyatlari:

1. **To'liq Blog Boshqaruvi:**
   - Postlarni CRUD operatsiyalari
   - Kategoriya va tag boshqaruvi
   - Izohlarni modereratsiya qilish
   - Sayt sozlamalari

2. **Advanced Xususiyatlar:**
   - Custom admin actions
   - Inline editing
   - Filtrlar va qidiruv
   - Bulk operations
   - CSV export

3. **Foydalanuvchi Do'stona Interfeys:**
   - O'zbek tilidagi nomlar
   - Tushunarli fieldset guruhlari
   - Visual indicators
   - Responsive design

4. **Performance Optimizatsiyasi:**
   - Select_related va prefetch_related
   - Optimizatsiya qilingan querylar
   - Query monitoring

### Keyingi Qadamlar:

1. Real ma'lumotlar bilan sinov o'tkazing
2. Foydalanuvchi huquqlarini sozlang
3. Backup strategiyasini ishlab chiqing
4. Monitoring va logging qo'shing

## Best Practices

### 1. Ma'lumotlar Xavfsizligi:
```python
# Muhim ma'lumotlarni readonly qilish
readonly_fields = ['created_at', 'updated_at', 'views_count']

# Foydalanuvchi huquqlarini tekshirish
def has_change_permission(self, request, obj=None):
    if obj and obj.author != request.user:
        return request.user.is_superuser
    return True
```

### 2. Performance:
```python
# Har doim select_related/prefetch_related ishlatish
def get_queryset(self, request):
    return super().get_queryset(request).select_related('author', 'category')

# List_per_page ni optimal qilib sozlash
list_per_page = 25  # Juda katta qiymat qo'ymaslik
```

### 3. Foydalanuvchi Tajribasi:
```python
# Tushunarli field nomlarini ishlatish
verbose_name = "Foydalanuvchi nomi"
verbose_name_plural = "Foydalanuvchilar"

# Foydali help_text qo'shish
help_text = "Bu maydon majburiy emas"
```

### 4. Validatsiya:
```python
# Model va form darajasida validatsiya
def clean(self):
    if self.status == 'published' and not self.published_at:
        self.published_at = timezone.now()
    return super().clean()
```

### 5. Logging:
```python
import logging
logger = logging.getLogger(__name__)

def save_model(self, request, obj, form, change):
    if change:
        logger.info(f"Post '{obj.title}' updated by {request.user.username}")
    else:
        logger.info(f"New post '{obj.title}' created by {request.user.username}")
    super().save_model(request, obj, form, change)
```

**E'tibor bering:** Admin panelni production muhitida ishlatishdan oldin barcha xavfsizlik choralarini ko'ring va test qiling!