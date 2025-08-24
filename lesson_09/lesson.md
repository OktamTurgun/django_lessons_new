# Lesson 09: Blog loyihasi. BlogDetail. Funksiyaga asoslangan View

## Dars maqsadi
Ushbu darsda biz Django loyihasida blog postlarini batafsil ko'rsatish uchun BlogDetail view yaratishni o'rganamiz. Funksiyaga asoslangan view (Function-Based View - FBV) yordamida individual blog postlarini ko'rsatish sahifasini yaratamiz.

## O'rganadigan mavzular
- Blog detail sahifasini yaratish
- URL patterns bilan parametr uzatish
- get_object_or_404() funksiyasidan foydalanish
- Template yaratish va ma'lumotlarni ko'rsatish
- SEO uchun meta ma'lumotlar qo'shish
- Error handling (404 xatolari)

## 1. Loyiha tuzilmasi

Avval loyihamizning joriy holatini ko'rib chiqamiz:

```
myblog/
├── blog/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── blog/
│           ├── base.html
│           ├── post_list.html
│           └── post_detail.html  # Bu darsda yaratamiz
├── myblog/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## 2. Model ko'rinishi (Takrorlash)

Oldingi darslarda yaratgan Blog modelimiz:

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                      args=[self.publish.year,
                            self.publish.month, 
                            self.publish.day, 
                            self.slug])
```

## 3. BlogDetail View yaratish

### 3.1 Asosiy view funksiyasi

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post

def post_detail(request, year, month, day, slug):
    """
    Individual blog postini ko'rsatish uchun view
    
    Args:
        request: HTTP so'rov obyekti
        year: Post nashr qilingan yil
        month: Post nashr qilingan oy
        day: Post nashr qilingan kun
        slug: Post slug maydoni
    
    Returns:
        Rendered template with post data
    """
    post = get_object_or_404(
        Post,
        status='published',
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    return render(request, 'blog/post_detail.html', {'post': post})
```

### 3.2 Alternativ yondashuv - try/except bilan

```python
def post_detail_alternative(request, year, month, day, slug):
    """
    Alternative approach using try/except
    """
    try:
        post = Post.objects.get(
            status='published',
            slug=slug,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    except Post.DoesNotExist:
        raise Http404("Post topilmadi")
    
    return render(request, 'blog/post_detail.html', {'post': post})
```

**Maslahat:** `get_object_or_404()` funksiyasini ishlatish best practice hisoblanadi, chunki u kod hajmini kamaytiradi va avtomatik ravishda 404 xatoligini qaytaradi.

## 4. URL konfiguratsiyasi

### 4.1 Blog app URLs

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.post_detail, 
         name='post_detail'),
]
```

### 4.2 URL pattern tushuntirish

- `<int:year>` - To'rt xonali yil (masalan, 2024)
- `<int:month>` - Ikki xonali oy (1-12)
- `<int:day>` - Ikki xonali kun (1-31)
- `<slug:slug>` - Post slug qiymati

**Misol URL:** `blog/2024/03/15/my-first-blog-post/`

## 5. Template yaratish

### 5.1 Base template (takrorlash)

```html
<!-- blog/templates/blog/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Blog{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { border-bottom: 1px solid #ccc; margin-bottom: 20px; padding-bottom: 20px; }
        .post { margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        .post-meta { color: #666; font-size: 14px; margin-bottom: 10px; }
        .post-title { margin: 0 0 10px 0; }
        .post-content { line-height: 1.6; }
        .back-link { margin: 20px 0; }
        .back-link a { color: #007cba; text-decoration: none; }
        .back-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><a href="{% url 'blog:post_list' %}">My Blog</a></h1>
        </div>
        
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

### 5.2 Post detail template

```html
<!-- blog/templates/blog/post_detail.html -->
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }} - My Blog{% endblock %}

{% block content %}
<div class="post">
    <h1 class="post-title">{{ post.title }}</h1>
    
    <div class="post-meta">
        <strong>Muallif:</strong> {{ post.author.get_full_name|default:post.author.username }}<br>
        <strong>Nashr qilingan:</strong> {{ post.publish|date:"d F Y, H:i" }}<br>
        {% if post.updated != post.created %}
        <strong>O'zgartirilgan:</strong> {{ post.updated|date:"d F Y, H:i" }}<br>
        {% endif %}
    </div>
    
    <div class="post-content">
        {{ post.body|linebreaks }}
    </div>
    
    <div class="back-link">
        <a href="{% url 'blog:post_list' %}">← Barcha postlarga qaytish</a>
    </div>
</div>
{% endblock %}
```

## 6. Post list template-ni yangilash

Post list sahifasidan detail sahifasiga linklar qo'shamiz:

```html
<!-- blog/templates/blog/post_list.html -->
{% extends 'blog/base.html' %}

{% block title %}Barcha Postlar - My Blog{% endblock %}

{% block content %}
<h2>Blog Postlari</h2>

{% for post in posts %}
<div class="post">
    <h3 class="post-title">
        <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </h3>
    
    <div class="post-meta">
        {{ post.author.username }} - {{ post.publish|date:"d F Y" }}
    </div>
    
    <div class="post-content">
        {{ post.body|truncatewords:30|linebreaks }}
        <a href="{{ post.get_absolute_url }}">Batafsil o'qish...</a>
    </div>
</div>
{% empty %}
<p>Hozircha hech qanday post yo'q.</p>
{% endfor %}
{% endblock %}
```

## 7. Test ma'lumotlari qo'shish

Django shell orqali test ma'lumotlari qo'shamiz:

```python
# Django shell: python manage.py shell
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

# User yaratish (agar yo'q bo'lsa)
user = User.objects.create_user('testuser', 'test@example.com', 'password')

# Test postlar yaratish
post1 = Post.objects.create(
    title='Birinchi blog post',
    slug='birinchi-blog-post',
    author=user,
    body='Bu birinchi blog postimning mazmuni. Bu yerda turli mavzular haqida yozaman.',
    status='published'
)

post2 = Post.objects.create(
    title='Django haqida',
    slug='django-haqida',
    author=user,
    body='Django - bu Python dasturlash tilida yozilgan web framework. U web ilovalar yaratishni osonlashtiradi.',
    status='published'
)
```

## 8. SEO va meta ma'lumotlar

SEO uchun meta ma'lumotlarni qo'shamiz:

```html
<!-- blog/templates/blog/post_detail.html - yangilangan versiya -->
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }} - My Blog{% endblock %}

{% block content %}
<!-- Meta tags for SEO -->
<meta name="description" content="{{ post.body|truncatewords:20|striptags }}">
<meta name="author" content="{{ post.author.get_full_name|default:post.author.username }}">
<meta property="og:title" content="{{ post.title }}">
<meta property="og:description" content="{{ post.body|truncatewords:20|striptags }}">
<meta property="og:type" content="article">

<div class="post">
    <h1 class="post-title">{{ post.title }}</h1>
    
    <div class="post-meta">
        <strong>Muallif:</strong> {{ post.author.get_full_name|default:post.author.username }}<br>
        <strong>Nashr qilingan:</strong> {{ post.publish|date:"d F Y, H:i" }}<br>
        {% if post.updated != post.created %}
        <strong>O'zgartirilgan:</strong> {{ post.updated|date:"d F Y, H:i" }}<br>
        {% endif %}
    </div>
    
    <div class="post-content">
        {{ post.body|linebreaks }}
    </div>
    
    <div class="back-link">
        <a href="{% url 'blog:post_list' %}">← Barcha postlarga qaytish</a>
    </div>
</div>
{% endblock %}
```

## 9. Error handling va xavfsizlik

### 9.1 404 sahifasini sozlash

```html
<!-- templates/404.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sahifa topilmadi - 404</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .error-container { max-width: 500px; margin: 0 auto; }
        .error-code { font-size: 72px; color: #ccc; margin: 0; }
        .error-message { font-size: 24px; margin: 20px 0; }
        .back-link { margin-top: 30px; }
        .back-link a { color: #007cba; text-decoration: none; padding: 10px 20px; border: 1px solid #007cba; }
        .back-link a:hover { background-color: #007cba; color: white; }
    </style>
</head>
<body>
    <div class="error-container">
        <h1 class="error-code">404</h1>
        <h2 class="error-message">Sahifa topilmadi</h2>
        <p>Kechirasiz, siz qidirayotgan sahifa mavjud emas.</p>
        <div class="back-link">
            <a href="{% url 'blog:post_list' %}">Bosh sahifaga qaytish</a>
        </div>
    </div>
</body>
</html>
```

### 9.2 Settings.py da debug rejimini o'chirish

```python
# myblog/settings.py
DEBUG = False  # Production uchun
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

## 10. Best Practices va Maslahatlar

### 10.1 View optimizatsiyasi

```python
# Optimized view with select_related
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post.objects.select_related('author'),
        status='published',
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    return render(request, 'blog/post_detail.html', {'post': post})
```

### 10.2 Template filterlari

```python
# blog/templatetags/blog_tags.py (yangi fayl yarating)
from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
```

Template da ishlatish:

```html
{% load blog_tags %}

<div class="post-content">
    {{ post.body|markdown }}
</div>
```

### 10.3 URL nomi konventsiyalari

```python
# blog/urls.py - URL nomlarini aniq qiling
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.post_detail, 
         name='post_detail'),
    # Kelajakda qo'shilishi mumkin
    path('category/<slug:category_slug>/', views.post_by_category, name='post_by_category'),
    path('tag/<slug:tag_slug>/', views.post_by_tag, name='post_by_tag'),
]
```

## 11. Testing

### 11.1 Unit testlar yozish

```python
# blog/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post

class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Bu test post matni.',
            status='published'
        )
    
    def test_post_detail_view_success(self):
        url = reverse('blog:post_detail', args=[
            self.post.publish.year,
            self.post.publish.month,
            self.post.publish.day,
            self.post.slug
        ])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
    
    def test_post_detail_view_404(self):
        url = reverse('blog:post_detail', args=[2024, 1, 1, 'mavjud-emas'])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
```

### 11.2 Testlarni ishga tushirish

```bash
python manage.py test blog
```

## 12. Xulosa

Ushbu darsda biz:

1. **BlogDetail view yaratdik** - Individual blog postlarini ko'rsatish uchun
2. **URL routing o'rnatdik** - Parametrlar bilan ishlashni o'rgandik
3. **Template yaratdik** - SEO-friendly va user-friendly dizayn bilan
4. **Error handling qo'shdik** - 404 xatolarini boshqarish uchun
5. **Best practices'larni qo'lladik** - Optimizatsiya va xavfsizlik uchun
6. **Testing yozdik** - Kodning ishonchliligini ta'minlash uchun

### Keyingi qadamlar:
- Comments tizimini qo'shish
- Postlarni kategoriyalar bo'yicha filtrlash
- Search funksiyasini qo'shish
- Admin panel orqali postlarni boshqarish

### Foydali linklar:
- [Django Views Documentation](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Django URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)