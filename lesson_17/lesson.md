# Dars 17: Template va static fayllar bilan ishlash

## Kirish

Django web frameworkida template va static fayllar web ilovaning vizual qismini tashkil etadi. Template'lar HTML sahifalarni dinamik tarzda yaratish uchun ishlatiladi, static fayllar esa CSS, JavaScript va rasm kabi o'zgarmas resurslarni saqlaydi.

## 1. Template'lar nima?

Template - bu HTML kodi ichida Django template tilini ishlatib, dinamik ma'lumotlarni ko'rsatish uchun mo'ljallangan fayllar.

### Template'ning asosiy qismlari:
- **HTML markup** - sahifaning tuzilishi
- **Template teglar** - `{% %}` belgilar ichida
- **Template o'zgaruvchilar** - `{{ }}` belgilar ichida  
- **Template filtrlari** - ma'lumotlarni formatlash uchun

```html
<!-- Oddiy template misoli -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Xush kelibsiz, {{ user.username }}!</h1>
    
    {% if articles %}
        <ul>
        {% for article in articles %}
            <li>{{ article.title|title }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Maqolalar topilmadi.</p>
    {% endif %}
</body>
</html>
```

## 2. Template'larni sozlash

### 2.1 TEMPLATES sozlamasi

`settings.py` faylida template'lar konfiguratsiyasi:

```python
# settings.py
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Asosiy templates papkasi
        ],
        'APP_DIRS': True,  # Har bir app ichidagi templates ni topish
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
```

### 2.2 Template papkalarini tuzish

```
myproject/
│
├── myproject/
│   ├── settings.py
│   └── ...
│
├── templates/          # Asosiy template papkasi
│   ├── base.html      # Asosiy shablon
│   ├── includes/      # Qism template'lar
│   └── news/         # News app template'lari
│       ├── list.html
│       └── detail.html
│
└── news/              # News app
    ├── templates/     # App ichidagi template'lar
    │   └── news/     # Namespace uchun
    └── views.py
```

## 3. Template meros olish (Inheritance)

### 3.1 Base template yaratish

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    
    <!-- Static fayllarni ulash -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header qismi -->
    <header>
        <nav>
            <a href="{% url 'home' %}">Bosh sahifa</a>
            <a href="{% url 'news:list' %}">Yangiliklar</a>
            <a href="{% url 'contact' %}">Aloqa</a>
        </nav>
    </header>
    
    <!-- Asosiy kontent -->
    <main>
        {% block content %}
        <!-- Bu qism boshqa template'larda to'ldiriladi -->
        {% endblock %}
    </main>
    
    <!-- Footer qismi -->
    <footer>
        <p>&copy; 2024 Yangiliklar sayti</p>
    </footer>
    
    <!-- JavaScript fayllar -->
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 3.2 Base template'dan foydalanish

```html
<!-- templates/news/list.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Yangiliklar ro'yxati{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/news.css' %}">
{% endblock %}

{% block content %}
    <div class="news-container">
        <h1>Eng so'ngi yangiliklar</h1>
        
        {% for article in articles %}
            <div class="news-item">
                <h2>
                    <a href="{% url 'news:detail' article.slug %}">
                        {{ article.title }}
                    </a>
                </h2>
                <p class="meta">
                    <span>{{ article.publish_date|date:"d.m.Y" }}</span>
                    <span>{{ article.category.name }}</span>
                </p>
                <p>{{ article.body|truncatewords:30 }}</p>
            </div>
        {% empty %}
            <p>Hozircha yangiliklar yo'q.</p>
        {% endfor %}
    </div>
{% endblock %}
```

## 4. Template teglar va filtrlar

### 4.1 Asosiy template teglar

```html
<!-- Shartli operatorlar -->
{% if condition %}
    <p>Shart bajarildi</p>
{% elif other_condition %}
    <p>Boshqa shart</p>
{% else %}
    <p>Hech bir shart bajarilmadi</p>
{% endif %}

<!-- Sikl operatorlari -->
{% for item in items %}
    <li>{{ item.name }} - {{ forloop.counter }}</li>
{% empty %}
    <li>Ro'yxat bo'sh</li>
{% endfor %}

<!-- URL yaratish -->
<a href="{% url 'news:detail' article.pk %}">Batafsil</a>
<a href="{% url 'news:category' category.slug %}">{{ category.name }}</a>

<!-- Static fayllar -->
{% load static %}
<img src="{% static 'images/logo.png' %}" alt="Logo">

<!-- Boshqa template'ni qo'shish -->
{% include 'includes/sidebar.html' %}
```

### 4.2 Ko'p ishlatiladigan filtrlar

```html
<!-- Ma'tnni formatlash -->
{{ article.title|title }}           <!-- Har so'z bosh harf bilan -->
{{ article.body|truncatewords:20 }}  <!-- 20 so'zga qisqartirish -->
{{ content|linebreaks }}            <!-- Qator o'tishlarni <br> ga aylantirish -->

<!-- Sanani formatlash -->
{{ article.date|date:"d.m.Y" }}     <!-- 25.12.2024 -->
{{ article.date|timesince }}        <!-- "2 soat oldin" -->

<!-- Sonlar bilan ishlash -->
{{ price|floatformat:2 }}           <!-- 10 chaqirigichgacha -->
{{ count|default:"0" }}             <!-- Agar bo'sh bo'lsa 0 -->

<!-- Ro'yxatlar -->
{{ items|length }}                  <!-- Elementlar soni -->
{{ items|first }}                   <!-- Birinchi element -->
{{ items|last }}                    <!-- Oxirgi element -->
```

## 5. Static fayllar bilan ishlash

### 5.1 Static fayllarni sozlash

```python
# settings.py
import os

# Static fayllar sozlamalari
STATIC_URL = '/static/'

# Development uchun
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Asosiy static papka
]

# Production uchun
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic buyrug'i uchun

# Media fayllar (foydalanuvchi yuklagan)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 5.2 Static fayllar tuzilishi

```
myproject/
├── static/
│   ├── css/
│   │   ├── style.css      # Asosiy stillar
│   │   ├── bootstrap.css  # CSS freymvork
│   │   └── news.css       # News ilovasi stillari
│   ├── js/
│   │   ├── main.js        # Asosiy JavaScript
│   │   ├── jquery.js      # Kutubxona
│   │   └── news.js        # News ilovasi JS kodi
│   ├── images/
│   │   ├── logo.png
│   │   ├── bg.jpg
│   │   └── icons/
│   └── fonts/
│       └── custom-font.woff2
└── news/
    └── static/           # App ichidagi static fayllar
        └── news/
            ├── css/
            └── js/
```

### 5.3 Template'da static fayllarni ishlatish

```html
{% load static %}

<!-- CSS fayllar -->
<link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- JavaScript fayllar -->
<script src="{% static 'js/jquery.js' %}"></script>
<script src="{% static 'js/main.js' %}"></script>

<!-- Rasmlar -->
<img src="{% static 'images/logo.png' %}" alt="Logo" class="logo">

<!-- Background image CSS orqali -->
<div class="hero-section" style="background-image: url('{% static 'images/bg.jpg' %}');"></div>
```

## 6. Include template'lar

### 6.1 Sidebar yaratish

```html
<!-- templates/includes/sidebar.html -->
<aside class="sidebar">
    <div class="widget">
        <h3>So'ngi yangiliklar</h3>
        <ul>
            {% for article in latest_news %}
                <li>
                    <a href="{% url 'news:detail' article.slug %}">
                        {{ article.title|truncatechars:50 }}
                    </a>
                    <small>{{ article.publish_date|date:"d.m" }}</small>
                </li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="widget">
        <h3>Kategoriyalar</h3>
        <ul>
            {% for category in categories %}
                <li>
                    <a href="{% url 'news:category' category.slug %}">
                        {{ category.name }} ({{ category.news_count }})
                    </a>
                </li>
            {% endfor %}
        </ul>
    </div>
</aside>
```

### 6.2 Include'ni ishlatish

```html
<!-- templates/news/list.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <!-- Asosiy kontent -->
            {% for article in articles %}
                <article>{{ article.title }}</article>
            {% endfor %}
        </div>
        
        <div class="col-md-4">
            <!-- Sidebar qo'shish -->
            {% include 'includes/sidebar.html' %}
        </div>
    </div>
</div>
{% endblock %}
```

## 7. View'larda template'lar bilan ishlash

### 7.1 Function-based view

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def news_list(request):
    """Yangiliklar ro'yxati"""
    articles = Article.objects.filter(status='published').order_by('-publish_date')
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'title': 'Eng so\'ngi yangiliklar',
    }
    
    return render(request, 'news/list.html', context)

def news_detail(request, slug):
    """Yangilik batafsil"""
    article = get_object_or_404(Article, slug=slug, status='published')
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(id=article.id)[:5]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'title': article.title,
    }
    
    return render(request, 'news/detail.html', context)
```

### 7.2 Class-based view

```python
# news/views.py
from django.views.generic import ListView, DetailView
from .models import Article

class NewsListView(ListView):
    model = Article
    template_name = 'news/list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(status='published').order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eng so\'ngi yangiliklar'
        context['categories'] = Category.objects.all()
        return context

class NewsDetailView(DetailView):
    model = Article
    template_name = 'news/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['related_articles'] = Article.objects.filter(
            category=article.category
        ).exclude(id=article.id)[:5]
        return context
```

## 8. Custom template teglar va filtrlar

### 8.1 Custom filtr yaratish

```python
# news/templatetags/news_extras.py
from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter
def markdown_to_html(text):
    """Markdown matnini HTML ga aylantirish"""
    return mark_safe(markdown.markdown(text))

@register.filter
def reading_time(text):
    """O'qish vaqtini hisoblash"""
    word_count = len(text.split())
    reading_time_minutes = word_count // 200  # 200 so'z/daqiqa
    return max(1, reading_time_minutes)
```

### 8.2 Custom teg yaratish

```python
# news/templatetags/news_extras.py

@register.simple_tag
def get_popular_articles(count=5):
    """Mashhur maqolalarni olish"""
    from news.models import Article
    return Article.objects.filter(status='published').order_by('-views')[:count]

@register.inclusion_tag('includes/popular_articles.html')
def show_popular_articles(count=5):
    """Mashhur maqolalarni ko'rsatish"""
    articles = Article.objects.filter(status='published').order_by('-views')[:count]
    return {'articles': articles}
```

### 8.3 Template'da custom teglarni ishlatish

```html
<!-- news/list.html -->
{% extends 'base.html' %}
{% load news_extras %}

{% block content %}
    <div class="content">
        {% for article in articles %}
            <article>
                <h2>{{ article.title }}</h2>
                <p class="meta">
                    O'qish vaqti: {{ article.body|reading_time }} daqiqa
                </p>
                <div class="content">
                    {{ article.body|markdown_to_html }}
                </div>
            </article>
        {% endfor %}
    </div>
    
    <aside>
        <!-- Custom teg ishlatish -->
        {% show_popular_articles 3 %}
        
        <!-- Yoki simple_tag -->
        {% get_popular_articles 5 as popular %}
        {% for article in popular %}
            <li>{{ article.title }}</li>
        {% endfor %}
    </aside>
{% endblock %}
```

## 9. CSS va JavaScript bilan ishlash

### 9.1 CSS faylni tuzish

```css
/* static/css/style.css */

/* Asosiy stillari */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

/* Header stillari */
header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
}

nav {
    display: flex;
    justify-content: space-around;
    max-width: 1200px;
    margin: 0 auto;
}

nav a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background 0.3s;
}

nav a:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Yangiliklar stillari */
.news-container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.news-item {
    border-bottom: 1px solid #eee;
    padding: 2rem 0;
}

.news-item h2 {
    margin-bottom: 0.5rem;
}

.news-item h2 a {
    color: #2c3e50;
    text-decoration: none;
}

.news-item h2 a:hover {
    color: #3498db;
}

.meta {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.meta span {
    margin-right: 1rem;
}

/* Responsive dizayn */
@media (max-width: 768px) {
    nav {
        flex-direction: column;
        text-align: center;
    }
    
    .news-container {
        padding: 0 0.5rem;
    }
}
```

### 9.2 JavaScript funksionalligi

```javascript
// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Yuqoriga chiqish tugmasi
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '↑';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        display: none;
        z-index: 1000;
    `;
    document.body.appendChild(backToTop);
    
    // Scroll hodisasini kuzatish
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });
    
    // Yuqoriga chiqish funksiyasi
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Rasmlarni lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});
```

## 10. Template xavfsizligi

### 10.1 XSS hujumlardan himoya

```html
<!-- Xavfli: HTML teglar ijro etiladi -->
{{ user_input }}

<!-- Xavfsiz: HTML teglar escape qilinadi -->
{{ user_input|escape }}

<!-- Agar HTML kerak bo'lsa, faqat ishonchli ma'lumot uchun -->
{{ trusted_html|safe }}

<!-- Yoki -->
{% autoescape off %}
    {{ trusted_html }}
{% endautoescape %}
```

### 10.2 CSRF himoya

```html
<!-- Formalar uchun CSRF token -->
<form method="post">
    {% csrf_token %}
    <input type="text" name="title">
    <button type="submit">Yuborish</button>
</form>

<!-- AJAX so'rovlar uchun -->
<script>
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

fetch('/api/data/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
</script>
```

## 11. Performance optimallashtirish

### 11.1 Template cache

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

```html
<!-- Template cache -->
{% load cache %}

{% cache 300 news_sidebar %}
    <!-- Bu qism 5 daqiqaga cache qilinadi -->
    {% include 'includes/sidebar.html' %}
{% endcache %}

<!-- Shartli cache -->
{% cache 300 news_list request.user.id %}
    <!-- Har bir foydalanuvchi uchun alohida cache -->
    {% for article in articles %}
        {{ article.title }}
    {% endfor %}
{% endcache %}
```

### 11.2 Static fayllarni optimallash

```python
# settings.py

# Gzip siqish
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Static fayllar URL'iga versiya qo'shish
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

## Xulosa

Template va static fayllar Django ilovasining vizual qismini tashkil etadi. To'g'ri ishlatilganda:

- **Template inheritance** - kodning takrorlanishini kamaytiradi
- **Static fayllar** - CSS, JS va rasmlarni samarali boshqaradi  
- **Template teglar** - dinamik kontent yaratish imkonini beradi
- **Security** - XSS va CSRF hujumlardan himoya qiladi
- **Performance** - cache va optimallash orqali tezlikni oshiradi

## Best Practice'lar

1. **Template tuzilishi**: Base template yarating va barcha sahifalarda foydalaning
2. **Static fayllar tashkiloti**: CSS, JS va rasmlarni mantiqiy papkalarga ajrating  
3. **Namespace'lar**: App template'larini alohida papkalarga joylang
4. **Custom teglar**: Takrorlanuvchi logikani custom tag'larga chiqaring
5. **Xavfsizlik**: Foydalanuvchi ma'lumotlarini doim escape qiling
6. **Performance**: Katta sahifalar uchun cache'dan foydalaning
7. **Mobile-first**: Responsive dizayn yarating
8. **Code splitting**: Katta JS fayllarni kichik qismlarga bo'ling

**Keyingi dars:**
Yangiliklar sayti shablonini Django’ga o‘rnatish