# 16-dars: News list va detail page

## Dars maqsadi
Ushbu darsda biz yangiliklar sayti uchun ikki muhim sahifani yaratamiz:
- **News List Page** - barcha yangiliklar ro'yxati
- **News Detail Page** - alohida yangilik haqida batafsil ma'lumot

## Nazariy qism

### List va Detail sahifalar nima?

**List sahifa** - bu ma'lumotlar bazasidagi barcha yoki filtrlangan obyektlar ro'yxatini ko'rsatadigan sahifa. Masalan, blog postlari, yangiliklar, mahsulotlar ro'yxati.

**Detail sahifa** - bu bitta obyekt haqida batafsil ma'lumot ko'rsatadigan sahifa. Masalan, bitta yangilik matnini to'liq o'qish.

### Django'da List va Detail Views

Django'da bunday sahifalarni yaratish uchun ikki xil yondashuv mavjud:

1. **Function-based Views (FBV)** - oddiy Python funksiyalari
2. **Class-based Views (CBV)** - Django'ning tayyor klasslari

Biz ikkala usulni ham o'rganamiz.

## 1-bosqich: News modelini tekshirish

Avval bizning News modelimiz qanday ko'rinishda ekanligini tekshiramiz:

```python
# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ['-created_at']
```

## 2-bosqich: URLs konfiguratsiyasi

Avval URL yo'llarini belgilaymiz:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
]
```

Asosiy URLs faylida qo'shamiz:

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 3-bosqich: Function-based Views yaratish

### News List View

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, Category

def news_list(request):
    """
    Barcha nashr etilgan yangiliklarni ko'rsatadigan view
    """
    # Faqat nashr etilgan yangiliklarni olamiz
    news_list = News.objects.filter(is_published=True)
    
    # Kategoriya bo'yicha filtrlash
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        news_list = news_list.filter(category=category)
    
    # Sahifalash (Pagination)
    paginator = Paginator(news_list, 6)  # Har sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Barcha kategoriyalarni olamiz
    categories = Category.objects.all()
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'news/list.html', context)
```

### News Detail View

```python
def news_detail(request, slug):
    """
    Bitta yangilikning batafsil sahifasi
    """
    # Slug bo'yicha yanglikni topamiz
    news = get_object_or_404(News, slug=slug, is_published=True)
    
    # Ushbu kategoriyadan boshqa yangiliklar
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/detail.html', context)
```

## 4-bosqich: Templates yaratish

### Base template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:list' %}">Yangiliklar</a>
            
            <div class="navbar-nav">
                <a class="nav-link" href="{% url 'news:list' %}">Bosh sahifa</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### News List template

```html
<!-- news/templates/news/list.html -->
{% extends 'base.html' %}

{% block title %}Yangiliklar ro'yxati{% endblock %}

{% block content %}
<div class="row">
    <!-- Kategoriyalar sidebar -->
    <div class="col-md-3">
        <div class="card">
            <div class="card-header">
                <h5>Kategoriyalar</h5>
            </div>
            <div class="card-body">
                <a href="{% url 'news:list' %}" 
                   class="btn btn-outline-primary btn-sm mb-2 {% if not current_category %}active{% endif %}">
                    Barchasi
                </a>
                
                {% for category in categories %}
                <a href="{% url 'news:list' %}?category={{ category.slug }}" 
                   class="btn btn-outline-primary btn-sm mb-2 d-block {% if current_category == category.slug %}active{% endif %}">
                    {{ category.name }}
                </a>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <!-- Yangiliklar ro'yxati -->
    <div class="col-md-9">
        <h2>So'nggi yangiliklar</h2>
        
        {% if news %}
        <div class="row">
            {% for item in news %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if item.image %}
                    <img src="{{ item.image.url }}" class="card-img-top" alt="{{ item.title }}" style="height: 200px; object-fit: cover;">
                    {% endif %}
                    
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ item.title }}</h5>
                        <p class="card-text">{{ item.content|truncatewords:20 }}</p>
                        
                        <div class="mt-auto">
                            <small class="text-muted">
                                {{ item.created_at|date:"d M, Y" }} | {{ item.category.name }}
                            </small>
                            <br>
                            <a href="{% url 'news:detail' item.slug %}" class="btn btn-primary btn-sm mt-2">
                                Batafsil o'qish
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        {% if news.has_other_pages %}
        <nav aria-label="Sahifalar">
            <ul class="pagination justify-content-center">
                {% if news.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ news.previous_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}">
                        Avvalgi
                    </a>
                </li>
                {% endif %}
                
                {% for num in news.paginator.page_range %}
                <li class="page-item {% if news.number == num %}active{% endif %}">
                    <a class="page-link" href="?page={{ num }}{% if current_category %}&category={{ current_category }}{% endif %}">
                        {{ num }}
                    </a>
                </li>
                {% endfor %}
                
                {% if news.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ news.next_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}">
                        Keyingi
                    </a>
                </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
        
        {% else %}
        <div class="alert alert-info">
            Hozircha yangiliklar mavjud emas.
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### News Detail template

```html
<!-- news/templates/news/detail.html -->
{% extends 'base.html' %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <!-- Yangilikning asosiy qismi -->
        <article class="mb-4">
            <h1>{{ news.title }}</h1>
            
            <div class="mb-3">
                <small class="text-muted">
                    <strong>Muallif:</strong> {{ news.author.get_full_name|default:news.author.username }} | 
                    <strong>Sana:</strong> {{ news.created_at|date:"d M, Y H:i" }} | 
                    <strong>Kategoriya:</strong> 
                    <a href="{% url 'news:list' %}?category={{ news.category.slug }}" class="text-decoration-none">
                        {{ news.category.name }}
                    </a>
                </small>
            </div>
            
            {% if news.image %}
            <img src="{{ news.image.url }}" class="img-fluid mb-3" alt="{{ news.title }}">
            {% endif %}
            
            <div class="content">
                {{ news.content|linebreaks }}
            </div>
        </article>
        
        <!-- Sahifaga qaytish tugmasi -->
        <a href="{% url 'news:list' %}" class="btn btn-secondary">
            ← Barcha yangiliklarga qaytish
        </a>
    </div>
    
    <!-- Sidebar - o'xshash yangiliklar -->
    <div class="col-md-4">
        {% if related_news %}
        <div class="card">
            <div class="card-header">
                <h5>O'xshash yangiliklar</h5>
            </div>
            <div class="card-body">
                {% for item in related_news %}
                <div class="mb-3">
                    {% if item.image %}
                    <img src="{{ item.image.url }}" class="img-thumbnail" alt="{{ item.title }}" style="width: 60px; height: 60px; object-fit: cover;">
                    {% endif %}
                    
                    <div class="d-inline-block align-top ms-2" style="width: calc(100% - 80px);">
                        <h6 class="mb-1">
                            <a href="{% url 'news:detail' item.slug %}" class="text-decoration-none">
                                {{ item.title|truncatechars:50 }}
                            </a>
                        </h6>
                        <small class="text-muted">{{ item.created_at|date:"d M, Y" }}</small>
                    </div>
                </div>
                {% if not forloop.last %}<hr>{% endif %}
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## 5-bosqich: Class-based Views bilan ishlash

Function-based views o'rniga Class-based views ishlatish ham mumkin:

```python
# news/views.py
from django.views.generic import ListView, DetailView
from .models import News, Category

class NewsListView(ListView):
    """
    Class-based view yangiliklar ro'yxati uchun
    """
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        
        # Kategoriya bo'yicha filtrlash
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context

class NewsDetailView(DetailView):
    """
    Class-based view yangilik detali uchun
    """
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O'xshash yangiliklar
        context['related_news'] = News.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:3]
        return context
```

Agar Class-based views ishlatmoqchi bo'lsangiz, URLs'ni ham o'zgartirish kerak:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]
```

## 6-bosqich: Qo'shimcha funksiyalar

### Qidiruv funksiyasi qo'shish

```python
# news/views.py
def news_list(request):
    news_list = News.objects.filter(is_published=True)
    
    # Qidiruv
    search_query = request.GET.get('q')
    if search_query:
        news_list = news_list.filter(
            title__icontains=search_query
        )
    
    # Kategoriya bo'yicha filtrlash
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        news_list = news_list.filter(category=category)
    
    # Sahifalash
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'news/list.html', context)
```

### Template'ga qidiruv qo'shish

List template'ga qidiruv formasi qo'shamiz:

```html
<!-- news/templates/news/list.html ichiga qo'shamiz -->
<div class="row mb-4">
    <div class="col-md-6">
        <form method="GET" class="d-flex">
            <input type="text" name="q" class="form-control" 
                   placeholder="Yangiliklarni qidiring..." 
                   value="{{ search_query }}">
            {% if current_category %}
            <input type="hidden" name="category" value="{{ current_category }}">
            {% endif %}
            <button type="submit" class="btn btn-primary ms-2">Qidiruv</button>
        </form>
    </div>
</div>
```

## 7-bosqich: SEO va Performance optimizatsiyasi

### select_related va prefetch_related ishlatish

```python
# news/views.py
def news_list(request):
    # Ma'lumotlar bazasiga kamroq so'rov yuborish uchun
    news_list = News.objects.filter(is_published=True).select_related(
        'author', 'category'
    )
    
    # Qolgan kod...

def news_detail(request, slug):
    news = get_object_or_404(
        News.objects.select_related('author', 'category'),
        slug=slug, 
        is_published=True
    )
    
    # Qolgan kod...
```

### Meta description qo'shish

```python
# news/models.py
class News(models.Model):
    # mavjud maydonlar...
    meta_description = models.CharField(max_length=160, blank=True)
    
    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.content[:160] + '...'
```

Template'da ishlatish:

```html
<!-- news/templates/news/detail.html -->
{% extends 'base.html' %}

{% block title %}{{ news.title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<!-- head qismiga qo'shamiz -->
<meta name="description" content="{{ news.get_meta_description }}">

<!-- Template davomi... -->
{% endblock %}
```

## 8-bosqich: Error handling va User Experience

### 404 sahifasini yaxshilash

```python
# news/views.py
from django.http import Http404

def news_detail(request, slug):
    try:
        news = News.objects.select_related('author', 'category').get(
            slug=slug, 
            is_published=True
        )
    except News.DoesNotExist:
        raise Http404("Yangilik topilmadi yoki nashr etilmagan")
    
    # Qolgan kod...
```

### Loading states va empty states

```html
<!-- news/templates/news/list.html -->
{% if news %}
    <!-- Yangiliklar ro'yxati -->
{% else %}
    <div class="text-center py-5">
        <h4>Yangiliklar topilmadi</h4>
        {% if search_query %}
        <p>"{{ search_query }}" bo'yicha qidiruv natijalari yo'q</p>
        <a href="{% url 'news:list' %}" class="btn btn-primary">Barchasi</a>
        {% else %}
        <p>Hozircha yangiliklar mavjud emas</p>
        {% endif %}
    </div>
{% endif %}
```

## Kod tushuntirish

### get_object_or_404 nima?

Bu Django'ning yordam funksiyasi. U obyektni topishga harakat qiladi, agar topmasa 404 xatolikni qaytaradi:

```python
# Bu ikki kod bir xil natija beradi:

# 1-usul - get_object_or_404
news = get_object_or_404(News, slug=slug)

# 2-usul - try/except
try:
    news = News.objects.get(slug=slug)
except News.DoesNotExist:
    raise Http404
```

### Pagination nima uchun kerak?

Agar minglab yangilik bo'lsa, barchasini bir sahifada ko'rsatish:
- Sahifa sekin yuklaydi
- Foydalanuvchi uchun noqulay
- Server uchun og'ir

Shuning uchun sahifalashdan foydalanamiz.

### Template'da truncatewords filtri

```django
{{ item.content|truncatewords:20 }}
```

Bu filtr matnning faqat 20 ta so'zini ko'rsatadi va oxiriga "..." qo'shadi.

## Testing qilish

Views'larni sinab ko'rish:

```python
# news/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, Category

class NewsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            content='Test content',
            author=self.user,
            category=self.category
        )
    
    def test_news_list_view(self):
        response = self.client.get(reverse('news:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')
    
    def test_news_detail_view(self):
        response = self.client.get(reverse('news:detail', kwargs={'slug': 'test-news'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')
```

## Xulosa

Ushbu darsda biz o'rgandik:

1. **Function-based Views** - oddiy Python funksiyalari sifatida views yaratish
2. **Pagination** - ko'p ma'lumotlarni sahifalarga bo'lish
3. **Filtrlash** - kategoriya bo'yicha yangiliklar filtrlash
4. **Related obyektlar** - o'xshash yangiliklar ko'rsatish
5. **SEO optimizatsiya** - meta description va title
6. **Performance** - select_related bilan optimizatsiya
7. **User Experience** - qidiruv, navigation, error handling

**Keyingi dars:**
Keyingi darsda biz template'lar va static fayllar bilan chuqurroq ishlaymiz.