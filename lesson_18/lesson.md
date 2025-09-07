# 18-dars: Home va Contact sahifalarini ishga tushurish

## Dars maqsadi
Ushbu darsda biz yangiliklar saytimiz uchun asosiy sahifalar - Home (Bosh sahifa) va Contact (Aloqa) sahifalarini yaratishni o'rganamiz. Bu sahifalar har qanday veb-saytning asosiy qismlari hisoblanadi.

## Nazariy qism

### 1. Home sahifasi nima?
Home sahifa - bu tashrif buyuruvchilar saytga kirganda birinchi ko'radigan sahifa. Bu sahifa:
- Saytning umumiy ko'rinishini beradi
- Asosiy kontentni namoyish etadi
- Foydalanuvchini boshqa sahifalarga yo'naltiradi
- SEO uchun juda muhim

### 2. Contact sahifasi nima?
Contact sahifa - bu foydalanuvchilar biz bilan bog'lanishi uchun mo'ljallangan sahifa. Bu sahifa:
- Aloqa ma'lumotlarini ko'rsatadi
- Xabar yuborish formasi mavjud
- Kompaniya manzili va xaritani o'z ichiga oladi
- Ijtimoiy tarmoq havolalarini o'z ichiga oladi

## Amaliy qism

### 1-bosqich: Views faylini tayyorlash

Avval `news/views.py` fayliga kerakli view'larni qo'shamiz:

```python
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import News

# Home sahifasi uchun view
def home_view(request):
    # Eng so'nggi 6 ta yangiliklarni olamiz
    latest_news = News.published.all()[:6]
    
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa'
    }
    return render(request, 'news/home.html', context)

# Contact sahifasi uchun view (Class-based view)
class ContactView(TemplateView):
    template_name = 'news/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Biz bilan bog\'lanish'
        return context
```

**Kodni tushuntirish:**
- `home_view` - funksiyaga asoslangan view
- `News.published.all()[:6]` - faqat nashr etilgan 6 ta yangiliklarni oladi
- `ContactView` - class-based view, `TemplateView`dan meros oladi
- `get_context_data` - templatega qo'shimcha ma'lumotlar yuborish uchun

### 2-bosqich: URL'larni sozlash

`news/urls.py` faylini yangilaymiz:

```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
]
```

**Kodni tushuntirish:**
- `path('', views.home_view, name='home')` - bosh sahifa uchun URL
- `path('contact/', views.ContactView.as_view(), name='contact')` - contact sahifasi uchun URL
- `.as_view()` - class-based view'ni ishlatish uchun zarur

### 3-bosqich: Asosiy URL'larni sozlash

Loyihaning asosiy `urls.py` fayliga o'zgarish kiritamiz:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # Bu yerda o'zgarish
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 4-bosqich: Home template yaratish

`templates/news/home.html` faylini yaratamiz:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<!-- Hero section -->
<div class="jumbotron jumbotron-fluid bg-primary text-white">
    <div class="container">
        <h1 class="display-4">Yangiliklar Saytiga Xush Kelibsiz!</h1>
        <p class="lead">Eng so'nggi va muhim yangiliklardan xabardor bo'ling</p>
        <a class="btn btn-light btn-lg" href="{% url 'news:news_list' %}" role="button">
            Barcha yangiliklar
        </a>
    </div>
</div>

<!-- Latest news section -->
<div class="container mt-5">
    <div class="row">
        <div class="col-12">
            <h2 class="mb-4">So'nggi yangiliklar</h2>
        </div>
    </div>
    
    <div class="row">
        {% for news in latest_news %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" class="card-img-top" alt="{{ news.title }}" style="height: 200px; object-fit: cover;">
                {% else %}
                <div class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;">
                    <span class="text-white">Rasm yo'q</span>
                </div>
                {% endif %}
                
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ news.title|truncatechars:60 }}</h5>
                    <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                    <div class="mt-auto">
                        <small class="text-muted">{{ news.publish_time|date:"d.m.Y H:i" }}</small>
                        <a href="{% url 'news:news_detail' news.id %}" class="btn btn-primary btn-sm float-right">
                            Batafsil
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info">
                Hozircha yangiliklar mavjud emas.
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- Call to action section -->
<div class="bg-light mt-5 py-5">
    <div class="container text-center">
        <h3>Bizning yangiliklarimizni kuzatib boring!</h3>
        <p class="lead">Har kuni yangi va qiziq yangiliklarni e'lon qilamiz</p>
        <a href="{% url 'news:contact' %}" class="btn btn-primary">Biz bilan bog'lanish</a>
    </div>
</div>
{% endblock %}
```

**Kodni tushuntirish:**
- `{% extends 'base.html' %}` - asosiy templatedan meros olish
- `{% load static %}` - static fayllarni yuklash
- Bootstrap classlari yordamida responsive dizayn
- `{{ news.title|truncatechars:60 }}` - matnni 60 belgida kesish
- `{% empty %}` - agar yangiliklar bo'lmasa nima ko'rsatish

### 5-bosqich: Contact template yaratish

`templates/news/contact.html` faylini yaratamiz:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-8">
            <h1>{{ page_title }}</h1>
            <hr>
            
            <!-- Contact form -->
            <div class="card">
                <div class="card-header">
                    <h4>Xabar yuborish</h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="name">Ismingiz *</label>
                                    <input type="text" class="form-control" id="name" name="name" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="email">Email *</label>
                                    <input type="email" class="form-control" id="email" name="email" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="subject">Mavzu *</label>
                            <input type="text" class="form-control" id="subject" name="subject" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="message">Xabaringiz *</label>
                            <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i> Xabar yuborish
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Contact info -->
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h4>Aloqa ma'lumotlari</h4>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <h6><i class="fas fa-map-marker-alt text-primary"></i> Manzil:</h6>
                        <p>Toshkent shahri, Yunusobod tumani<br>
                        Amir Temur ko'chasi, 123-uy</p>
                    </div>
                    
                    <div class="mb-3">
                        <h6><i class="fas fa-phone text-primary"></i> Telefon:</h6>
                        <p>+998 90 123 45 67</p>
                    </div>
                    
                    <div class="mb-3">
                        <h6><i class="fas fa-envelope text-primary"></i> Email:</h6>
                        <p>info@yangiliklar.uz</p>
                    </div>
                    
                    <div class="mb-3">
                        <h6><i class="fas fa-clock text-primary"></i> Ish vaqti:</h6>
                        <p>Dushanba - Juma: 9:00 - 18:00<br>
                        Shanba: 9:00 - 14:00</p>
                    </div>
                </div>
            </div>
            
            <!-- Social media -->
            <div class="card mt-4">
                <div class="card-header">
                    <h4>Ijtimoiy tarmoqlar</h4>
                </div>
                <div class="card-body text-center">
                    <a href="#" class="btn btn-primary btn-sm mx-1">
                        <i class="fab fa-facebook-f"></i> Facebook
                    </a>
                    <a href="#" class="btn btn-info btn-sm mx-1">
                        <i class="fab fa-twitter"></i> Twitter
                    </a>
                    <a href="#" class="btn btn-primary btn-sm mx-1">
                        <i class="fab fa-telegram"></i> Telegram
                    </a>
                    <a href="#" class="btn btn-danger btn-sm mx-1">
                        <i class="fab fa-instagram"></i> Instagram
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6-bosqich: Navigation menu yangilash

`templates/base.html` faylidagi navigation menyusini yangilaymiz:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">
            <i class="fas fa-newspaper"></i> Yangiliklar
        </a>
        
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'news:home' %}">
                        <i class="fas fa-home"></i> Bosh sahifa
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'news:news_list' %}">
                        <i class="fas fa-list"></i> Yangiliklar
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'news:contact' %}">
                        <i class="fas fa-envelope"></i> Aloqa
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### 7-bosqich: Sahifalarni sinash

1. **Development serverni ishga tushiring:**
```bash
python manage.py runserver
```

2. **Quyidagi sahifalarni tekshiring:**
   - http://127.0.0.1:8000/ - Bosh sahifa
   - http://127.0.0.1:8000/contact/ - Contact sahifasi
   - http://127.0.0.1:8000/news/ - Yangiliklar ro'yxati

## Xatoliklarni tuzatish

### Umumiy xatoliklar:

1. **TemplateDoesNotExist xatosi:**
   - Template fayllarining yo'lini tekshiring
   - `TEMPLATES` sozlamalarini tekshiring

2. **NoReverseMatch xatosi:**
   - URL nomlarini tekshiring
   - `app_name` ni to'g'ri yozganingizni tekshiring

3. **Static fayllar yuklanmayapti:**
   - `STATIC_URL` va `STATIC_ROOT` sozlamalarini tekshiring
   - `{% load static %}` yozganingizni tekshiring

## Best Practice va Maslahatlar

### 1. SEO uchun maslahatlar:
```html
<!-- Meta teglarni qo'shing -->
<meta name="description" content="Eng so'nggi yangiliklar va ma'lumotlar">
<meta name="keywords" content="yangiliklar, so'nggi xabarlar, Uzbekiston">
<meta name="author" content="Yangiliklar sayti">
```

### 2. Performance uchun:
- Rasmlarni optimizatsiya qiling
- CSS va JS fayllarni minify qiling
- Caching ishlatishni o'ylab ko'ring

### 3. User Experience:
- Sahifalar tez yuklanishi kerak
- Mobile-friendly dizayn ishlatilsin
- Clear navigation bo'lsin

### 4. Security:
- Har doim `{% csrf_token %}` ishlatilsin
- Form ma'lumotlarni validatsiya qiling
- XSS himoyasini o'ylab ko'ring

### 5. Code Organization:
```python
# views.py da context'ni alohida funksiyaga ajrating
def get_home_context():
    return {
        'latest_news': News.published.all()[:6],
        'featured_news': News.published.filter(featured=True)[:3],
        'categories': Category.objects.all()
    }

def home_view(request):
    context = get_home_context()
    context['page_title'] = 'Bosh sahifa'
    return render(request, 'news/home.html', context)
```

### 6. Template Optimization:
```html
<!-- Fragment caching ishlatilsin -->
{% load cache %}
{% cache 300 latest_news %}
    <!-- Yangiliklar ro'yxati -->
{% endcache %}
```

## Xulosa

Ushbu darsda biz:
- Home va Contact sahifalarini yaratdik
- Function-based va Class-based view'lar bilan ishladik
- Template'larni to'g'ri tashkil qildik
- Navigation menu'ni yangiladik
- Best practice'lar bilan tanishdik

**Keyingi dars:**
19-darsda: Formalar bilan ishlash va contact form