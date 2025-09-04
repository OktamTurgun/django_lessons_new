# Dars 17: Template va static fayllar - Amaliyot

Ushbu amaliyot darsida biz yangiliklar loyihamizga to'liq template tizimi va static fayllar qo'shamiz.

## Loyiha tuzilishi
Amaliyot boshida loyihamiz quyidagi tuzilishga ega bo'lishi kerak:

```
newssite/
├── newssite/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── news/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── manage.py
```

## Bosqich 1: Template sozlamalarini o'rnatish

### 1.1 Template papkasini yaratish
Loyiha ildiz qismida `templates` papkasini yarating:

```bash
mkdir templates
mkdir templates/includes
mkdir templates/news
```

### 1.2 Settings.py ni sozlash

```python
# newssite/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Template sozlamalari
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Asosiy templates papkasi
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.auth.context_processors.messages',
            ],
        },
    },
]

# Static fayllar sozlamalari  
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Production uchun

# Media fayllar
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Bosqich 2: Static fayllar tuzilishini yaratish

### 2.1 Static papkalarini yaratish

```bash
mkdir static
mkdir static/css
mkdir static/js  
mkdir static/images
mkdir static/fonts
```

### 2.2 Asosiy CSS faylini yaratish
`static/css/style.css` faylini yarating:

```css
/* static/css/style.css */

/* Reset va asosiy stillari */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

/* Header stillari */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: white;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background 0.3s ease;
}

.nav-menu a:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Main content */
main {
    margin: 2rem 0;
    min-height: calc(100vh - 200px);
}

/* Card stillari */
.card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.card-title {
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
}

.card-title a {
    color: inherit;
    text-decoration: none;
}

.card-title a:hover {
    color: #3498db;
}

.card-meta {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.card-content {
    color: #555;
    line-height: 1.6;
}

/* Button stillari */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn:hover {
    background: #2980b9;
}

.btn-primary {
    background: #3498db;
}

.btn-success {
    background: #2ecc71;
}

.btn-danger {
    background: #e74c3c;
}

/* Grid system */
.row {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -15px;
}

.col {
    flex: 1;
    padding: 0 15px;
}

.col-md-6 {
    flex: 0 0 50%;
    max-width: 50%;
    padding: 0 15px;
}

.col-md-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
    padding: 0 15px;
}

.col-md-8 {
    flex: 0 0 66.666667%;
    max-width: 66.666667%;
    padding: 0 15px;
}

/* Footer stillari */
footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    .nav-menu {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .row {
        flex-direction: column;
    }
    
    .col-md-6,
    .col-md-4,
    .col-md-8 {
        flex: 1 1 100%;
        max-width: 100%;
    }
}

/* Utility classes */
.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.mb-2 {
    margin-bottom: 1rem;
}

.mb-3 {
    margin-bottom: 1.5rem;
}

.mt-2 {
    margin-top: 1rem;
}

.mt-3 {
    margin-top: 1.5rem;
}
```

### 2.3 JavaScript fayli yaratish
`static/js/main.js` faylini yarating:

```javascript
// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth scrolling
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    valid = false;
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Iltimos, barcha majburiy maydonlarni to\'ldiring!');
            }
        });
    });
});
```

## Bosqich 3: Base template yaratish

### 3.1 Base template
`templates/base.html` faylini yarating:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar Sayti{% endblock %}</title>
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container">
            <div class="header-content">
                <a href="{% url 'news:index' %}" class="logo">
                    📰 Yangiliklar
                </a>
                
                <nav>
                    <ul class="nav-menu">
                        <li><a href="{% url 'news:index' %}">Bosh sahifa</a></li>
                        <li><a href="{% url 'news:category_list' %}">Kategoriyalar</a></li>
                        <li><a href="#">Aloqa</a></li>
                    </ul>
                </nav>
                
                <!-- Mobile menu toggle -->
                <button class="mobile-toggle" style="display: none;">☰</button>
            </div>
        </div>
    </header>

    <!-- Main content -->
    <main>
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 Yangiliklar Sayti. Barcha huquqlar himoyalangan.</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 3.2 Include fayllar yaratish
`templates/includes/breadcrumb.html`:

```html
<!-- templates/includes/breadcrumb.html -->
<nav class="breadcrumb" style="margin-bottom: 2rem; padding: 1rem; background: white; border-radius: 5px;">
    <a href="{% url 'news:index' %}">Bosh sahifa</a>
    {% for crumb in breadcrumbs %}
        <span> / </span>
        {% if crumb.url %}
            <a href="{{ crumb.url }}">{{ crumb.title }}</a>
        {% else %}
            <span>{{ crumb.title }}</span>
        {% endif %}
    {% endfor %}
</nav>
```

`templates/includes/pagination.html`:

```html
<!-- templates/includes/pagination.html -->
{% if is_paginated %}
<div class="pagination" style="text-align: center; margin: 2rem 0;">
    {% if page_obj.has_previous %}
        <a href="?page=1" class="btn">Birinchi</a>
        <a href="?page={{ page_obj.previous_page_number }}" class="btn">Oldingi</a>
    {% endif %}
    
    <span style="margin: 0 1rem;">
        Sahifa {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
    </span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="btn">Keyingi</a>
        <a href="?page={{ page_obj.paginator.num_pages }}" class="btn">Oxirgi</a>
    {% endif %}
</div>
{% endif %}
```

## Bosqich 4: News app template'lari

### 4.1 Index template
`templates/news/index.html`:

```html
<!-- templates/news/index.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa - Yangiliklar{% endblock %}

{% block content %}
<div class="hero-section" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{% static "images/hero-bg.jpg" %}'); background-size: cover; padding: 4rem 0; text-align: center; color: white; margin-bottom: 3rem; border-radius: 10px;">
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">So'nggi Yangiliklar</h1>
    <p style="font-size: 1.2rem;">Eng muhim va dolzarb yangiliklar bilan tanishib boring</p>
</div>

<div class="row">
    <!-- Latest News -->
    <div class="col-md-8">
        <h2 style="margin-bottom: 2rem; color: #2c3e50;">So'nggi yangiliklar</h2>
        
        {% for article in latest_articles %}
        <article class="card">
            {% if article.image %}
            <div style="margin-bottom: 1rem;">
                <img src="{{ article.image.url }}" alt="{{ article.title }}" 
                     style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px;">
            </div>
            {% endif %}
            
            <h3 class="card-title">
                <a href="{% url 'news:detail' article.pk %}">{{ article.title }}</a>
            </h3>
            
            <div class="card-meta">
                <span>📅 {{ article.created_at|date:"d.m.Y H:i" }}</span>
                <span>👤 {{ article.author.first_name }} {{ article.author.last_name }}</span>
                <span>📂 <a href="{% url 'news:category_detail' article.category.pk %}">{{ article.category.name }}</a></span>
            </div>
            
            <div class="card-content">
                {{ article.content|truncatewords:50|safe }}
            </div>
            
            <div style="margin-top: 1rem;">
                <a href="{% url 'news:detail' article.pk %}" class="btn">To'liq o'qish</a>
            </div>
        </article>
        {% empty %}
        <div class="card text-center">
            <p>Hozircha yangiliklar yo'q.</p>
        </div>
        {% endfor %}
        
        {% include 'includes/pagination.html' %}
    </div>
    
    <!-- Sidebar -->
    <div class="col-md-4">
        <!-- Categories -->
        <div class="card">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">Kategoriyalar</h4>
            <ul style="list-style: none;">
                {% for category in categories %}
                <li style="margin-bottom: 0.5rem;">
                    <a href="{% url 'news:category_detail' category.pk %}" 
                       style="text-decoration: none; color: #3498db;">
                        {{ category.name }} ({{ category.article_set.count }})
                    </a>
                </li>
                {% endfor %}
            </ul>
        </div>
        
        <!-- Popular Articles -->
        <div class="card">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">Ommabop yangiliklar</h4>
            {% for article in popular_articles %}
            <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                <h5 style="margin-bottom: 0.5rem;">
                    <a href="{% url 'news:detail' article.pk %}" 
                       style="text-decoration: none; color: #2c3e50; font-size: 0.9rem;">
                        {{ article.title|truncatechars:60 }}
                    </a>
                </h5>
                <small style="color: #666;">{{ article.created_at|date:"d.m.Y" }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

### 4.2 Detail template
`templates/news/detail.html`:

```html
<!-- templates/news/detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ article.title }} - Yangiliklar{% endblock %}

{% block content %}
{% include 'includes/breadcrumb.html' with breadcrumbs=breadcrumbs %}

<div class="row">
    <div class="col-md-8">
        <article class="card">
            {% if article.image %}
            <div style="margin-bottom: 2rem;">
                <img src="{{ article.image.url }}" alt="{{ article.title }}" 
                     style="width: 100%; height: 300px; object-fit: cover; border-radius: 5px;">
            </div>
            {% endif %}
            
            <h1 style="color: #2c3e50; margin-bottom: 1rem; font-size: 2rem;">{{ article.title }}</h1>
            
            <div class="card-meta" style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #eee;">
                <span>📅 {{ article.created_at|date:"d F Y, H:i" }}</span>
                <span>👤 {{ article.author.first_name }} {{ article.author.last_name }}</span>
                <span>📂 <a href="{% url 'news:category_detail' article.category.pk %}">{{ article.category.name }}</a></span>
                {% if article.updated_at != article.created_at %}
                <span>✏️ Tahrirlangan: {{ article.updated_at|date:"d.m.Y H:i" }}</span>
                {% endif %}
            </div>
            
            <div class="card-content" style="font-size: 1.1rem; line-height: 1.8;">
                {{ article.content|safe }}
            </div>
            
            <!-- Tags -->
            {% if article.tags.all %}
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee;">
                <strong>Teglar: </strong>
                {% for tag in article.tags.all %}
                <span style="display: inline-block; background: #f8f9fa; padding: 0.25rem 0.5rem; margin: 0.25rem; border-radius: 3px; font-size: 0.9rem;">
                    #{{ tag.name }}
                </span>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Social sharing -->
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee;">
                <strong>Ulashish: </strong>
                <a href="https://t.me/share/url?url={{ request.build_absolute_uri }}&text={{ article.title }}" 
                   class="btn btn-primary" target="_blank">Telegram</a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}" 
                   class="btn" target="_blank">Facebook</a>
            </div>
        </article>
        
        <!-- Related articles -->
        {% if related_articles %}
        <div class="card">
            <h3 style="margin-bottom: 1rem; color: #2c3e50;">Ushbu mavzuda boshqa yangiliklar</h3>
            <div class="row">
                {% for related in related_articles %}
                <div class="col-md-6">
                    <div style="margin-bottom: 1rem;">
                        <h5>
                            <a href="{% url 'news:detail' related.pk %}" 
                               style="text-decoration: none; color: #2c3e50;">
                                {{ related.title|truncatechars:80 }}
                            </a>
                        </h5>
                        <small style="color: #666;">{{ related.created_at|date:"d.m.Y" }}</small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
    
    <!-- Sidebar -->
    <div class="col-md-4">
        <!-- Author info -->
        <div class="card">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">Muallif</h4>
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; background: #3498db; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 2rem;">
                    {{ article.author.first_name.0 }}{{ article.author.last_name.0 }}
                </div>
                <h5>{{ article.author.first_name }} {{ article.author.last_name }}</h5>
                <p style="color: #666; font-size: 0.9rem;">{{ article.author.email }}</p>
            </div>
        </div>
        
        <!-- Recent articles from same category -->
        <div class="card">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">{{ article.category.name }} yangiliklari</h4>
            {% for cat_article in category_articles %}
            <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                <h6>
                    <a href="{% url 'news:detail' cat_article.pk %}" 
                       style="text-decoration: none; color: #2c3e50; font-size: 0.9rem;">
                        {{ cat_article.title|truncatechars:60 }}
                    </a>
                </h6>
                <small style="color: #666;">{{ cat_article.created_at|date:"d.m.Y" }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<div style="margin-top: 2rem; text-align: center;">
    <a href="{% url 'news:index' %}" class="btn">⬅ Bosh sahifaga qaytish</a>
</div>
{% endblock %}
```

### 4.3 Category templates
`templates/news/category_list.html`:

```html
<!-- templates/news/category_list.html -->
{% extends 'base.html' %}

{% block title %}Kategoriyalar - Yangiliklar{% endblock %}

{% block content %}
<div class="text-center mb-3">
    <h1 style="color: #2c3e50;">Yangilik Kategoriyalari</h1>
    <p style="color: #666;">Qiziqtirgan mavzuni tanlang</p>
</div>

<div class="row">
    {% for category in categories %}
    <div class="col-md-4">
        <div class="card text-center">
            <h3 style="color: #3498db; margin-bottom: 1rem;">{{ category.name }}</h3>
            <p style="color: #666; margin-bottom: 1rem;">{{ category.description|truncatewords:20 }}</p>
            <p><strong>{{ category.article_set.count }} ta yangilik</strong></p>
            <a href="{% url 'news:category_detail' category.pk %}" class="btn">Ko'rish</a>
        </div>
    </div>
    {% empty %}
    <div class="col">
        <div class="card text-center">
            <p>Hozircha kategoriyalar mavjud emas.</p>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

`templates/news/category_detail.html`:

```html
<!-- templates/news/category_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ category.name }} - Kategoriya{% endblock %}

{% block content %}
{% include 'includes/breadcrumb.html' with breadcrumbs=breadcrumbs %}

<div class="card mb-3">
    <h1 style="color: #2c3e50;">{{ category.name }}</h1>
    <p style="color: #666;">{{ category.description }}</p>
    <small style="color: #999;">Jami: {{ articles.count }} ta yangilik</small>
</div>

<div class="row">
    {% for article in articles %}
    <div class="col-md-6">
        <article class="card">
            {% if article.image %}
            <div style="margin-bottom: 1rem;">
                <img src="{{ article.image.url }}" alt="{{ article.title }}" 
                     style="width: 100%; height: 150px; object-fit: cover; border-radius: 5px;">
            </div>
            {% endif %}
            
            <h4 class="card-title">
                <a href="{% url 'news:detail' article.pk %}">{{ article.title|truncatechars:80 }}</a>
            </h4>
            
            <div class="card-meta">
                <span>{{ article.created_at|date:"d.m.Y" }}</span>
                <span>{{ article.author.first_name }} {{ article.author.last_name }}</span>
            </div>
            
            <div class="card-content">
                {{ article.content|truncatewords:30|striptags }}
            </div>
            
            <a href="{% url 'news:detail' article.pk %}" class="btn">Davomi</a>
        </article>
    </div>
    {% empty %}
    <div class="col">
        <div class="card text-center">
            <p>Bu kategoriyada hozircha yangiliklar yo'q.</p>
        </div>
    </div>
    {% endfor %}
</div>

{% include 'includes/pagination.html' %}

<div style="margin-top: 2rem; text-center;">
    <a href="{% url 'news:category_list' %}" class="btn">⬅ Barcha kategoriyalar</a>
</div>
{% endblock %}
```

## Bosqich 5: View'larni yangilash

### 5.1 Updated views.py
`news/views.py` faylini yangilang:

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Article, Category

def index(request):
    """Bosh sahifa view'i"""
    # So'nggi yangiliklar
    articles_list = Article.objects.select_related('author', 'category').order_by('-created_at')
    paginator = Paginator(articles_list, 5)  # Har sahifada 5 ta yangilik
    page_number = request.GET.get('page')
    latest_articles = paginator.get_page(page_number)
    
    # Kategoriyalar
    categories = Category.objects.annotate(
        article_count=Count('article')
    ).filter(article_count__gt=0)
    
    # Ommabop yangiliklar (oxirgi 10 ta)
    popular_articles = Article.objects.select_related('author', 'category').order_by('-created_at')[:10]
    
    context = {
        'latest_articles': latest_articles,
        'categories': categories,
        'popular_articles': popular_articles,
    }
    return render(request, 'news/index.html', context)

def detail(request, pk):
    """Yangilik batafsil ko'rish"""
    article = get_object_or_404(Article.objects.select_related('author', 'category'), pk=pk)
    
    # O'xshash yangiliklar
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(pk=article.pk).order_by('-created_at')[:4]
    
    # Kategoriya yangiliklari
    category_articles = Article.objects.filter(
        category=article.category
    ).exclude(pk=article.pk).order_by('-created_at')[:5]
    
    # Breadcrumb
    breadcrumbs = [
        {'title': article.category.name, 'url': f'/news/category/{article.category.pk}/'},
        {'title': article.title[:50] + '...' if len(article.title) > 50 else article.title, 'url': None}
    ]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'category_articles': category_articles,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'news/detail.html', context)

def category_list(request):
    """Kategoriyalar ro'yxati"""
    categories = Category.objects.annotate(
        article_count=Count('article')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'news/category_list.html', context)

def category_detail(request, pk):
    """Kategoriya bo'yicha yangiliklar"""
    category = get_object_or_404(Category, pk=pk)
    
    articles_list = Article.objects.filter(
        category=category
    ).select_related('author').order_by('-created_at')
    
    paginator = Paginator(articles_list, 6)  # Har sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    # Breadcrumb
    breadcrumbs = [
        {'title': 'Kategoriyalar', 'url': '/news/categories/'},
        {'title': category.name, 'url': None}
    ]
    
    context = {
        'category': category,
        'articles': articles,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'news/category_detail.html', context)
```

## Bosqich 6: URL'larni yangilash

### 6.1 News app URLs
`news/urls.py` faylini yangilang:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.detail, name='detail'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]
```

### 6.2 Main URLs
`newssite/urls.py` faylini yangilang:

```python
# newssite/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # Bosh sahifa uchun
    path('news/', include('news.urls')),  # /news/ prefiksi bilan ham
]

# Media fayllar uchun (development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
```

## Bosqich 7: Media fayllar uchun sozlamalar

### 7.1 Media papkasini yaratish

```bash
mkdir media
mkdir media/news
mkdir media/news/images
```

### 7.2 Model'ni yangilash
Agar hali qilmagan bo'lsangiz, `news/models.py` da image field qo'shing:

```python
# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('news:category_detail', args=[self.pk])

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    image = models.ImageField(upload_to='news/images/', blank=True, null=True, verbose_name="Rasm")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")
    is_published = models.BooleanField(default=True, verbose_name="Nashr etilgan")

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:detail', args=[self.pk])
```

## Bosqich 8: Django admin ni sozlash

### 8.1 Admin.py ni yangilash
`news/admin.py` faylini yangilang:

```python
# news/admin.py
from django.contrib import admin
from .models import Category, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'content', 'image')
        }),
        ('Kategoriya va Muallif', {
            'fields': ('category', 'author')
        }),
        ('Holatlar', {
            'fields': ('is_published',)
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratilganda
            obj.author = request.user
        super().save_model(request, obj, form, change)
```

## Bosqich 9: Qo'shimcha funksiyalar

### 9.1 Custom template tags
`news/templatetags/` papkasini yarating va `news_extras.py` fayli qo'shing:

```python
# news/templatetags/news_extras.py
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()

@register.filter
def truncate_words_html(value, arg):
    """HTML taglarni saqlab qolgan holda so'zlarni qisqartirish"""
    from django.utils.text import Truncator
    truncator = Truncator(value)
    return truncator.words(int(arg), html=True)

@register.simple_tag
def relative_time(datetime_obj):
    """Nisbiy vaqtni ko'rsatish"""
    from django.utils.timezone import now
    from datetime import timedelta
    
    diff = now() - datetime_obj
    
    if diff.days > 7:
        return datetime_obj.strftime("%d.%m.%Y")
    elif diff.days > 0:
        return f"{diff.days} kun oldin"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} soat oldin"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} daqiqa oldin"
    else:
        return "Hozirgina"

@register.inclusion_tag('includes/article_card.html')
def article_card(article, show_category=True):
    """Yangilik kartasi uchun template tag"""
    return {
        'article': article,
        'show_category': show_category,
    }
```

### 9.2 Article card template
`templates/includes/article_card.html` yarating:

```html
<!-- templates/includes/article_card.html -->
{% load news_extras %}

<article class="card">
    {% if article.image %}
    <div style="margin-bottom: 1rem;">
        <img src="{{ article.image.url }}" alt="{{ article.title }}" 
             style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px;">
    </div>
    {% endif %}
    
    <h3 class="card-title">
        <a href="{{ article.get_absolute_url }}">{{ article.title }}</a>
    </h3>
    
    <div class="card-meta">
        <span>📅 {% relative_time article.created_at %}</span>
        <span>👤 {{ article.author.first_name }} {{ article.author.last_name }}</span>
        {% if show_category %}
        <span>📂 <a href="{{ article.category.get_absolute_url }}">{{ article.category.name }}</a></span>
        {% endif %}
    </div>
    
    <div class="card-content">
        {{ article.content|truncate_words_html:30 }}
    </div>
    
    <div style="margin-top: 1rem;">
        <a href="{{ article.get_absolute_url }}" class="btn">To'liq o'qish</a>
    </div>
</article>
```

## Bosqich 10: Migratsiya va test

### 10.1 Migratsiyalarni bajarish

```bash
# Yangi migratsiya yaratish (agar model o'zgartirgan bo'lsangiz)
python manage.py makemigrations

# Migratsiyalarni bajarish
python manage.py migrate

# Static fayllarni yig'ish (production uchun)
python manage.py collectstatic
```

### 10.2 Superuser yaratish

```bash
python manage.py createsuperuser
```

### 10.3 Test ma'lumotlari qo'shish

Django shell orqali:

```python
# Shell ochish
python manage.py shell

# Test ma'lumotlari
from news.models import Category, Article
from django.contrib.auth.models import User

# Kategoriyalar yaratish
sport = Category.objects.create(
    name="Sport", 
    description="Sport yangiliklari va voqealari"
)

texnologiya = Category.objects.create(
    name="Texnologiya", 
    description="IT va texnologiya sohasidagi yangiliklar"
)

siyosat = Category.objects.create(
    name="Siyosat", 
    description="Siyosiy yangiliklar va tahlillar"
)

# User yaratish (agar yo'q bo'lsa)
user = User.objects.first()  # yoki User.objects.create_user(...)

# Yangiliklar yaratish
Article.objects.create(
    title="Yangi texnologiya haqida",
    content="Bu yerda yangilik matni bo'ladi...",
    author=user,
    category=texnologiya
)

# Yana bir nechta yangilik qo'shish...
```

### 10.4 Serverni ishga tushirish

```bash
python manage.py runserver
```

## Xulosa

Ushbu darsda biz:

1. **Template tizimini sozladik** - base template, includes, va app-specific template'lar
2. **Static fayllar tizimini yaratdik** - CSS, JavaScript, images
3. **Responsive dizayn** yaratdik - mobile-friendly interface
4. **To'liq funksional yangiliklar sayti** yaratdik
5. **Admin paneli** ni sozladik
6. **Custom template tags** yaratdik
7. **Pagination** qo'shdik
8. **Breadcrumb navigation** qo'shdik

**Keyingi darsda**: Forms, Search, va User Authentication qo'shamiz.

**Vazifa**: 
1. Qo'shimcha kategoriya va yangiliklar qo'shing
2. Ranglar va dizaynni o'zingizga moslashtiring  
3. Qo'shimcha static fayllar (font, icons) qo'shing
4. Mobile ko'rinishni sinab ko'ring