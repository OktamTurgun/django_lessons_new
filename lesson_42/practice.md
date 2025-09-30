# Ruxsatnomalar - Amaliyot

Bu amaliyot mashg'ulotida biz yangiliklar sayti loyihasiga to'liq ruxsatnomalar tizimini qo'shamiz.

---

## Vazifa 1: UserPassesTestMixin qo'shish

### 1.1. NewsUpdateView'ni yangilash

`news/views.py` faylini oching va quyidagi o'zgarishlarni kiriting:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author
```

**Tushuntirish:**
- `UserPassesTestMixin` qo'shdik
- `test_func()` metodida foydalanuvchi muallif ekanligini tekshirmoqdamiz

### 1.2. NewsDeleteView'ni yangilash

```python
class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author
```

### 1.3. Tekshirish

1. Serverni ishga tushiring: `python manage.py runserver`
2. Bir foydalanuvchi bilan tizimga kiring
3. Boshqa foydalanuvchining yangiligini tahrirlashga harakat qiling
4. 403 Forbidden xato chiqishi kerak

---

## Vazifa 2: Custom Admin Panel yaratish

### 2.1. CustomAdminSite yaratish

`news/admin.py` faylini yangilang:

```python
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import News, Category

class CustomAdminSite(AdminSite):
    site_header = 'Yangiliklar Boshqaruvi'
    site_title = 'Mening Admin Panelim'
    index_title = 'Xush kelibsiz!'
    
    def has_permission(self, request):
        """
        Barcha tizimga kirgan foydalanuvchilarga ruxsat
        """
        return request.user.is_active and request.user.is_authenticated

# Custom admin site instance yaratamiz
custom_admin_site = CustomAdminSite(name='custom_admin')
```

### 2.2. News modelini ro'yxatdan o'tkazish

```python
@admin.register(News, site=custom_admin_site)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'publish_time']
    list_filter = ['status', 'category', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    
    def save_model(self, request, obj, form, change):
        """
        Yangi yangilik yaratilganda avtomatik author qo'shish
        """
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """
        Har bir foydalanuvchi faqat o'z yangiliklarini ko'radi
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def has_change_permission(self, request, obj=None):
        """
        Faqat o'z yangiligini tahrirlash mumkin
        """
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """
        Faqat o'z yangiligini o'chirish mumkin
        """
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser
```

### 2.3. Category modelini ro'yxatdan o'tkazish

```python
@admin.register(Category, site=custom_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def has_add_permission(self, request):
        """
        Faqat superuser kategoriya qo'shishi mumkin
        """
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """
        Faqat superuser kategoriya o'chirishi mumkin
        """
        return request.user.is_superuser
```

### 2.4. URL'ni sozlash

`config/urls.py` faylini yangilang:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.admin import custom_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),  # Django standart admin
    path('my-admin/', custom_admin_site.urls),  # Custom admin
    path('', include('pages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 2.5. Tekshirish

1. Oddiy foydalanuvchi bilan tizimga kiring
2. `http://127.0.0.1:8000/my-admin/` manzilga o'ting
3. Faqat o'z yangiliklaringizni ko'rishingiz kerak
4. Yangilik qo'shing va tekshiring

---

## Vazifa 3: Dekoratorli ruxsatnomalar (Function-Based Views)

### 3.1. Custom dekorator yaratish

`news/decorators.py` faylini yarating:

```python
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from functools import wraps

def author_required(model):
    """
    Foydalanuvchi obyekt muallifi ekanligini tekshiradi
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # pk yoki slug olish
            pk = kwargs.get('pk')
            slug = kwargs.get('slug')
            
            # Obyektni topish
            if pk:
                obj = get_object_or_404(model, pk=pk)
            elif slug:
                obj = get_object_or_404(model, slug=slug)
            else:
                return HttpResponseForbidden("Noto'g'ri parametr!")
            
            # Tekshirish
            if request.user != obj.author and not request.user.is_superuser:
                return HttpResponseForbidden(
                    "Sizda bu amalni bajarish huquqi yo'q!"
                )
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
```

### 3.2. Function-based view'lar yaratish

`news/views.py` faylida yangi view'lar qo'shing:

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import News
from .forms import NewsForm
from .decorators import author_required

@login_required
def news_create_fbv(request):
    """
    Function-based view orqali yangilik yaratish
    """
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', slug=news.slug)
    else:
        form = NewsForm()
    
    context = {
        'form': form,
        'title': 'Yangilik qo\'shish'
    }
    return render(request, 'news/create.html', context)

@login_required
@author_required(News)
def news_update_fbv(request, slug):
    """
    Function-based view orqali yangilikni tahrirlash
    """
    news = get_object_or_404(News, slug=slug)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', slug=news.slug)
    else:
        form = NewsForm(instance=news)
    
    context = {
        'form': form,
        'news': news,
        'title': 'Yangilikni tahrirlash'
    }
    return render(request, 'news/update.html', context)

@login_required
@author_required(News)
def news_delete_fbv(request, slug):
    """
    Function-based view orqali yangilikni o'chirish
    """
    news = get_object_or_404(News, slug=slug)
    
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    
    context = {
        'news': news,
        'title': 'Yangilikni o\'chirish'
    }
    return render(request, 'news/delete.html', context)
```

### 3.3. URL'larni qo'shish

`news/urls.py` faylida:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Class-based views
    path('', views.NewsListView.as_view(), name='news_list'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('<slug:slug>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('<slug:slug>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    
    # Function-based views (test uchun)
    path('fbv/create/', views.news_create_fbv, name='news_create_fbv'),
    path('fbv/<slug:slug>/update/', views.news_update_fbv, name='news_update_fbv'),
    path('fbv/<slug:slug>/delete/', views.news_delete_fbv, name='news_delete_fbv'),
]
```

---

## Vazifa 4: Custom Mixin yaratish

### 4.1. AuthorRequiredMixin yaratish

`news/mixins.py` faylini yarating:

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Foydalanuvchi obyekt muallifi ekanligini tekshiradi
    """
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user == obj.author or user.is_superuser
    
    def handle_no_permission(self):
        """
        Ruxsat bo'lmasa, xabar ko'rsatish va bosh sahifaga yo'naltirish
        """
        messages.error(
            self.request,
            "Sizda bu amalni bajarish huquqi yo'q!"
        )
        return redirect('news_list')

class AuthorOrStaffRequiredMixin(UserPassesTestMixin):
    """
    Muallif yoki staff foydalanuvchi ekanligini tekshiradi
    """
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user == obj.author or user.is_staff or user.is_superuser
```

### 4.2. Mixin'lardan foydalanish

`news/views.py` faylida:

```python
from .mixins import AuthorRequiredMixin, AuthorOrStaffRequiredMixin

class NewsUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'news/update.html'

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
```

---

## Vazifa 5: Template'da ruxsatlarni ko'rsatish

### 5.1. news_detail.html'ni yangilash

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-8">
            <article>
                <h1>{{ news.title }}</h1>
                
                {% if news.image %}
                <img src="{{ news.image.url }}" class="img-fluid mb-3" alt="{{ news.title }}">
                {% endif %}
                
                <div class="mb-3">
                    <small class="text-muted">
                        <i class="fas fa-user"></i> {{ news.author.username }} |
                        <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d F, Y" }} |
                        <i class="fas fa-tag"></i> {{ news.category.name }}
                    </small>
                </div>
                
                <div class="news-body">
                    {{ news.body|linebreaks }}
                </div>
                
                <!-- Ruxsatlar bo'yicha tugmalar -->
                {% if user.is_authenticated %}
                    {% if user == news.author or user.is_superuser %}
                    <div class="mt-4">
                        <a href="{% url 'news_update' news.slug %}" class="btn btn-warning">
                            <i class="fas fa-edit"></i> Tahrirlash
                        </a>
                        <a href="{% url 'news_delete' news.slug %}" class="btn btn-danger">
                            <i class="fas fa-trash"></i> O'chirish
                        </a>
                    </div>
                    {% endif %}
                {% else %}
                    <div class="alert alert-info mt-4">
                        Tahrirlash uchun <a href="{% url 'login' %}">tizimga kiring</a>
                    </div>
                {% endif %}
            </article>
        </div>
        
        <div class="col-lg-4">
            <!-- Sidebar -->
        </div>
    </div>
</div>
{% endblock %}
```

### 5.2. news_list.html'ni yangilash

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Yangiliklar</h1>
                
                {% if user.is_authenticated %}
                <a href="{% url 'news_create' %}" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Yangilik qo'shish
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <div class="row">
        {% for news in news_list %}
        <div class="col-md-6 mb-4">
            <div class="card">
                {% if news.image %}
                <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}">
                {% endif %}
                
                <div class="card-body">
                    <h5 class="card-title">{{ news.title }}</h5>
                    <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            {{ news.author.username }} | {{ news.publish_time|date:"d.m.Y" }}
                        </small>
                        
                        <div>
                            <a href="{% url 'news_detail' news.slug %}" class="btn btn-sm btn-primary">
                                O'qish
                            </a>
                            
                            {% if user == news.author or user.is_superuser %}
                            <a href="{% url 'news_update' news.slug %}" class="btn btn-sm btn-warning">
                                <i class="fas fa-edit"></i>
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <p class="text-center">Hozircha yangiliklar yo'q</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

---

## Vazifa 6: Xato xabarlarini ko'rsatish

### 6.1. messages.py yaratish

`news/messages.py` faylini yarating:

```python
from django.contrib import messages

def success_message(request, message):
    """Success xabar"""
    messages.success(request, message)

def error_message(request, message):
    """Error xabar"""
    messages.error(request, message)

def warning_message(request, message):
    """Warning xabar"""
    messages.warning(request, message)

def info_message(request, message):
    """Info xabar"""
    messages.info(request, message)
```

### 6.2. View'larga xabarlar qo'shish

```python
from django.contrib import messages

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'news/create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Yangilik muvaffaqiyatli yaratildi!")
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'news/update.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Yangilik muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Yangilik muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)
```

### 6.3. base.html'ga xabarlar qo'shish

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    
    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    {% block content %}
    {% endblock %}
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## Vazifa 7: Testlar yozish

### 7.1. tests.py yaratish

`news/tests.py` faylini yarating:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import News, Category

class NewsPermissionTests(TestCase):
    
    def setUp(self):
        """Test uchun ma'lumotlar yaratish"""
        self.client = Client()
        
        # Foydalanuvchilar yaratish
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Kategoriya yaratish
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Yangilik yaratish
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            body='Test body content',
            category=self.category,
            author=self.user1,
            status='published'
        )
    
    def test_anonymous_user_redirected_to_login(self):
        """Anonim foydalanuvchi login sahifasiga yo'naltiriladi"""
        response = self.client.get(
            reverse('news_update', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_author_can_update_own_news(self):
        """Muallif o'z yangiligini tahrirlashi mumkin"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(
            reverse('news_update', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_non_author_cannot_update_news(self):
        """Boshqa foydalanuvchi yangilikni tahrirlolmaydi"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(
            reverse('news_update', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 403)
    
    def test_superuser_can_update_any_news(self):
        """Superuser har qanday yangilikni tahrirlashi mumkin"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(
            reverse('news_update', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_author_can_delete_own_news(self):
        """Muallif o'z yangiligini o'chirishi mumkin"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(
            reverse('news_delete', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(News.objects.filter(slug='test-news').exists())
    
    def test_non_author_cannot_delete_news(self):
        """Boshqa foydalanuvchi yangilikni o'chira olmaydi"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.post(
            reverse('news_delete', kwargs={'slug': self.news.slug})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(News.objects.filter(slug='test-news').exists())
```

### 7.2. Testlarni ishga tushirish

```bash
# Barcha testlarni ishga tushirish
python manage.py test

# Faqat news ilovasining testlari
python manage.py test news

# Faqat bitta test klassi
python manage.py test news.tests.NewsPermissionTests

# Faqat bitta test metodi
python manage.py test news.tests.NewsPermissionTests.test_author_can_update_own_news

# Verbose rejim
python manage.py test --verbosity=2
```

---

## Vazifa 8: 403 va 404 sahifalarini sozlash

### 8.1. Custom 403 sahifa yaratish

`templates/403.html` faylini yarating:

```html
{% extends 'base.html' %}

{% block title %}403 - Ruxsat yo'q{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <h1 class="display-1">403</h1>
            <h2>Ruxsat yo'q</h2>
            <p class="lead">Sizda bu sahifaga kirish huquqi yo'q.</p>
            <p>Agar bu xato deb hisoblasangiz, administrator bilan bog'laning.</p>
            <a href="{% url 'home' %}" class="btn btn-primary">Bosh sahifa</a>
            <a href="javascript:history.back()" class="btn btn-secondary">Orqaga</a>
        </div>
    </div>
</div>
{% endblock %}
```

### 8.2. Custom 404 sahifa yaratish

`templates/404.html` faylini yarating:

```html
{% extends 'base.html' %}

{% block title %}404 - Sahifa topilmadi{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <h1 class="display-1">404</h1>
            <h2>Sahifa topilmadi</h2>
            <p class="lead">Kechirasiz, siz qidirayotgan sahifa mavjud emas.</p>
            <a href="{% url 'home' %}" class="btn btn-primary">Bosh sahifa</a>
            <a href="{% url 'news_list' %}" class="btn btn-secondary">Yangiliklar</a>
        </div>
    </div>
</div>
{% endblock %}
```

### 8.3. settings.py'da sozlash

```python
# DEBUG = False bo'lganda ishlaydi
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Template sozlamalari
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
            ],
        },
    },
]
```

### 8.4. Handler'larni sozlash

`config/urls.py` faylida:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom error handlers
handler403 = 'django.views.defaults.permission_denied'
handler404 = 'django.views.defaults.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-admin/', custom_admin_site.urls),
    path('', include('pages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Vazifa 9: Logging sozlash

### 9.1. settings.py'da logging sozlash

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'news': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 9.2. logs papkasini yaratish

```bash
mkdir logs
touch logs/.gitkeep
```

### 9.3. .gitignore'ga qo'shish

```
# Logs
logs/*.log
```

### 9.4. View'larda logging ishlatish

```python
import logging

logger = logging.getLogger('news')

class NewsUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        has_permission = self.request.user == news.author or self.request.user.is_superuser
        
        if not has_permission:
            logger.warning(
                f"Unauthorized update attempt - User: {self.request.user.username}, "
                f"News ID: {news.pk}, News Title: {news.title}"
            )
        
        return has_permission
    
    def form_valid(self, form):
        logger.info(
            f"News updated - User: {self.request.user.username}, "
            f"News ID: {self.object.pk}, News Title: {self.object.title}"
        )
        messages.success(self.request, "Yangilik muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
    
    def delete(self, request, *args, **kwargs):
        news = self.get_object()
        logger.warning(
            f"News deleted - User: {request.user.username}, "
            f"News ID: {news.pk}, News Title: {news.title}"
        )
        messages.success(request, "Yangilik muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)
```

---

## Vazifa 10: Qo'shimcha xususiyatlar

### 10.1. Yangilikni publish/unpublish qilish

`news/views.py`ga qo'shing:

```python
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def toggle_publish(request, slug):
    """
    Yangilikni publish/unpublish qilish
    """
    news = get_object_or_404(News, slug=slug)
    
    # Ruxsat tekshiruvi
    if request.user != news.author and not request.user.is_superuser:
        return JsonResponse({
            'success': False,
            'message': 'Ruxsat yo\'q'
        }, status=403)
    
    # Status o'zgartirish
    if news.status == 'published':
        news.status = 'draft'
        message = 'Yangilik qoralama holatiga o\'tkazildi'
    else:
        news.status = 'published'
        message = 'Yangilik nashr etildi'
    
    news.save()
    
    logger.info(
        f"News status changed - User: {request.user.username}, "
        f"News: {news.title}, New status: {news.status}"
    )
    
    return JsonResponse({
        'success': True,
        'message': message,
        'status': news.status
    })
```

### 10.2. URL qo'shish

```python
path('<slug:slug>/toggle-publish/', views.toggle_publish, name='toggle_publish'),
```

### 10.3. Template'ga AJAX qo'shish

```html
<button class="btn btn-info" onclick="togglePublish('{{ news.slug }}')">
    {% if news.status == 'published' %}
        Qoralama holatiga o'tkazish
    {% else %}
        Nashr etish
    {% endif %}
</button>

<script>
function togglePublish(slug) {
    if (!confirm('Statusni o\'zgartirmoqchimisiz?')) return;
    
    fetch(`/news/${slug}/toggle-publish/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Xatolik yuz berdi');
    });
}
</script>
```

---

## Vazifa 11: Qo'shimcha ruxsatlar

### 11.1. Staff uchun maxsus view

```python
from django.contrib.auth.decorators import user_passes_test

def is_staff_user(user):
    """Staff yoki superuser ekanligini tekshirish"""
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_user)
def staff_dashboard(request):
    """
    Staff foydalanuvchilar uchun dashboard
    """
    # Statistika
    total_news = News.objects.count()
    published_news = News.objects.filter(status='published').count()
    draft_news = News.objects.filter(status='draft').count()
    
    # Oxirgi yangiliklar
    recent_news = News.objects.order_by('-publish_time')[:10]
    
    # Muallif bo'yicha statistika
    from django.db.models import Count
    authors_stats = User.objects.annotate(
        news_count=Count('news')
    ).filter(news_count__gt=0).order_by('-news_count')
    
    context = {
        'total_news': total_news,
        'published_news': published_news,
        'draft_news': draft_news,
        'recent_news': recent_news,
        'authors_stats': authors_stats,
    }
    
    return render(request, 'news/staff_dashboard.html', context)
```

### 11.2. Dashboard template

`templates/news/staff_dashboard.html`:

```html
{% extends 'base.html' %}

{% block title %}Staff Dashboard{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Staff Dashboard</h1>
    
    <!-- Statistika kartalar -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5 class="card-title">Jami yangiliklar</h5>
                    <h2>{{ total_news }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5 class="card-title">Nashr etilgan</h5>
                    <h2>{{ published_news }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <h5 class="card-title">Qoralama</h5>
                    <h2>{{ draft_news }}</h2>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Oxirgi yangiliklar -->
    <div class="card mb-4">
        <div class="card-header">
            <h5>Oxirgi yangiliklar</h5>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Sarlavha</th>
                        <th>Muallif</th>
                        <th>Status</th>
                        <th>Sana</th>
                        <th>Amallar</th>
                    </tr>
                </thead>
                <tbody>
                    {% for news in recent_news %}
                    <tr>
                        <td>{{ news.title }}</td>
                        <td>{{ news.author.username }}</td>
                        <td>
                            <span class="badge bg-{% if news.status == 'published' %}success{% else %}warning{% endif %}">
                                {{ news.get_status_display }}
                            </span>
                        </td>
                        <td>{{ news.publish_time|date:"d.m.Y H:i" }}</td>
                        <td>
                            <a href="{% url 'news_detail' news.slug %}" class="btn btn-sm btn-info">Ko'rish</a>
                            <a href="{% url 'news_update' news.slug %}" class="btn btn-sm btn-warning">Tahrirlash</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Muallif statistikasi -->
    <div class="card">
        <div class="card-header">
            <h5>Muallif statistikasi</h5>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Muallif</th>
                        <th>Yangiliklar soni</th>
                    </tr>
                </thead>
                <tbody>
                    {% for author in authors_stats %}
                    <tr>
                        <td>{{ author.username }}</td>
                        <td>{{ author.news_count }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Yakuniy tekshirish ro'yxati

Barcha vazifalarni bajarib bo'lgandan keyin quyidagilarni tekshiring:

### ✅ UserPassesTestMixin
- [ ] NewsUpdateView'da ishlamoqda
- [ ] NewsDeleteView'da ishlamoqda
- [ ] Faqat muallif tahrirlashi va o'chirishi mumkin
- [ ] Superuser barcha yangiliklar bilan ishlashi mumkin

### ✅ Custom Admin Panel
- [ ] `/my-admin/` manzili ochilmoqda
- [ ] Barcha tizimga kirgan foydalanuvchilar kirishlari mumkin
- [ ] Har kim faqat o'z yangiliklarini ko'rmoqda
- [ ] Yangilik qo'shishda avtomatik author qo'shilmoqda

### ✅ Dekoratorlar
- [ ] `@login_required` ishlamoqda
- [ ] `@author_required` custom dekorator ishlayapti
- [ ] Function-based view'lar to'g'ri ishlayapti

### ✅ Custom Mixin'lar
- [ ] AuthorRequiredMixin yaratilgan
- [ ] View'larda ishlatilgan
- [ ] Xato xabarlari ko'rsatilmoqda

### ✅ Template'lar
- [ ] Tugmalar faqat ruxsat bo'lganida ko'rsatilmoqda
- [ ] Xabarlar (messages) to'g'ri ishlayapti
- [ ] 403 va 404 sahifalar ishlayapti

### ✅ Testlar
- [ ] Barcha testlar yozilgan
- [ ] `python manage.py test` buyrug'i muvaffaqiyatli
- [ ] Coverage 80% dan yuqori

### ✅ Logging
- [ ] Logging sozlangan
- [ ] Log fayllar yaratilmoqda
- [ ] Warning va error'lar yozilmoqda

### ✅ Xavfsizlik
- [ ] CSRF himoyasi ishlayapti
- [ ] SQL Injection'dan himoyalangan
- [ ] XSS'dan himoyalangan
- [ ] Parollar hash qilingan

---

## Qo'shimcha topshiriqlar (Ixtiyoriy)

### 1. Email bildirishnomalar
Yangilik tahrirlanganda yoki o'chirilganda admin'ga email yuborish.

### 2. Activity log
Barcha amallarni bazaga yozib borish (kim, qachon, nima qilgan).

### 3. Bulk actions
Admin panelda bir nechta yangilikni birdan tahrirlash yoki o'chirish.

### 4. Export funksiyasi
Yangiliklarni CSV yoki Excel formatda yuklab olish.

### 5. API yaratish
Django REST Framework bilan API endpoint'lar yaratish va ruxsatnomalarni sozlash.

---

## Xulosa

Ushbu amaliyot darsida biz:

1. **UserPassesTestMixin** bilan Class-based view'larda ruxsatlarni boshqardik
2. **Custom Admin Panel** yaratdik va barcha foydalanuvchilar uchun ochdik
3. **Dekoratorlar** bilan Function-based view'larda ruxsatlarni boshqardik
4. **Custom Mixin va Dekorator** yaratdik
5. **Template'larda** ruxsatlarni ko'rsatdik
6. **Xato sahifalari** (403, 404) yaratdik
7. **Logging** sozladik
8. **Testlar** yozdik
9. **Xavfsizlik** bo'yicha ko'rsatmalarni bajardik

Keyingi darsda biz Django'da izohlar tizimini yaratamiz!

---

## Foydali havolalar

- [Django Authentication System](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django Admin Site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django Logging](https://docs.djangoproject.com/en/stable/topics/logging/)