# 18-dars: Amaliyot - Home va Contact sahifalarini ishga tushirish

## Maqsad
Ushbu amaliyot darsida siz o'zingiz mustaqil ravishda Home va Contact sahifalarini yaratishni amalga oshirasiz.

## Topshiriq 1: Loyihani tayyorlash

### 1.1. Virtual muhitni faollashtiring
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 1.2. Loyihaning holatini tekshiring
```bash
# Database migrationlarini tekshiring
python manage.py showmigrations

# Agar kerak bo'lsa, migrationlarni bajaring
python manage.py migrate
```

### 1.3. Superuser mavjudligini tekshiring
```bash
# Agar superuser yo'q bo'lsa yarating
python manage.py createsuperuser
```

## Topshiriq 2: Views yaratish

### 2.1. news/views.py faylini oching va quyidagi kodni qo'shing:

```python
# Mavjud import'lar ustiga qo'shing
from django.views.generic import TemplateView

# Mavjud view'lar ostiga qo'shing
def home_view(request):
    """
    Bosh sahifa view'i
    Eng so'nggi 6 ta yangiliklarni ko'rsatadi
    """
    # TODO: Bu joyga kodingizni yozing
    # Maslahat: News.published.all()[:6] ishlatilsin
    pass

class ContactView(TemplateView):
    """
    Contact sahifasi uchun class-based view
    """
    template_name = 'news/contact.html'
    
    def get_context_data(self, **kwargs):
        # TODO: Bu joyga kodingizni yozing
        # Maslahat: context'ga page_title qo'shilsin
        pass
```

**Sizning vazifangiz:**
1. `home_view` funksiyasini to'ldiring
2. `ContactView` klassining `get_context_data` metodini to'ldiring

### 2.2. Yechim tekshirish
Kodingiz quyidagicha bo'lishi kerak:

```python
def home_view(request):
    """
    Bosh sahifa view'i
    Eng so'nggi 6 ta yangiliklarni ko'rsatadi
    """
    latest_news = News.published.all()[:6]
    
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa'
    }
    return render(request, 'news/home.html', context)

class ContactView(TemplateView):
    """
    Contact sahifasi uchun class-based view
    """
    template_name = 'news/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Biz bilan bog\'lanish'
        return context
```

## Topshiriq 3: URL'larni sozlash

### 3.1. news/urls.py faylini yangilang

```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # TODO: Bu yerga URL'larni qo'shing
    # Maslahat: 
    # - Bosh sahifa uchun: path('', views.home_view, name='home')
    # - Contact uchun: path('contact/', views.ContactView.as_view(), name='contact')
    
    # Mavjud URL'lar
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
]
```

### 3.2. config/urls.py faylini tekshiring

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: Bu yerda news app'ni include qilish to'g'ri ekanini tekshiring
    path('', include('news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Topshiriq 4: Template'larni yaratish

### 4.1. templates/news/ papkasini yarating (agar yo'q bo'lsa)

### 4.2. home.html template yaratish

`templates/news/home.html` faylini yarating va quyidagi strukturani to'ldiring:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<!-- TODO: Hero section yarating -->
<div class="jumbotron jumbotron-fluid bg-primary text-white">
    <div class="container">
        <!-- Bu yerga sarlavha va tavsif yozing -->
    </div>
</div>

<!-- TODO: So'nggi yangiliklar section -->
<div class="container mt-5">
    <!-- Bu yerga yangiliklar ro'yxatini yozing -->
</div>

<!-- TODO: Call to action section -->
<div class="bg-light mt-5 py-5">
    <!-- Bu yerga qo'shimcha bo'lim yozing -->
</div>
{% endblock %}
```

**Maslahatlar:**
- Hero section'da sayt haqida qisqacha ma'lumot beriring
- Yangiliklar uchun card component'lar ishlatilsin
- Bootstrap grid system (row, col) ishlatilsin
- Rasm bo'lmasa placeholder ko'rsatilsin

### 4.3. contact.html template yaratish

`templates/news/contact.html` faylini yarating:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-8">
            <!-- TODO: Contact form yarating -->
            
        </div>
        <div class="col-lg-4">
            <!-- TODO: Contact info yarating -->
            
        </div>
    </div>
</div>
{% endblock %}
```

**Maslahatlar:**
- Form'da name, email, subject, message maydonlari bo'lsin
- Contact info'da manzil, telefon, email ko'rsatilsin
- Ijtimoiy tarmoq havolalari qo'shilsin

## Topshiriq 5: Navigation menu yangilash

### 5.1. templates/base.html faylidagi navigation'ni yangilang

```html
<!-- Navbar ichida quyidagi strukturani yarating -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="#">
            <!-- TODO: Logo va sayt nomi -->
        </a>
        
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ml-auto">
                <!-- TODO: Menu item'larini qo'shing -->
                <!-- Bosh sahifa, Yangiliklar, Aloqa -->
            </ul>
        </div>
    </div>
</nav>
```

## Topshiriq 6: Sahifalarni test qilish

### 6.1. Development server'ni ishga tushiring
```bash
python manage.py runserver
```

### 6.2. Quyidagi sahifalarga kiring va ishlashini tekshiring:
1. http://127.0.0.1:8000/ - Bosh sahifa
2. http://127.0.0.1:8000/contact/ - Contact sahifasi
3. http://127.0.0.1:8000/news/ - Yangiliklar

### 6.3. Har bir sahifada quyidagilarni tekshiring:
- [ ] Sahifa to'g'ri yuklanmoqda
- [ ] Navigation menu ishlaydi
- [ ] Ma'lumotlar to'g'ri ko'rsatilmoqda
- [ ] Responsive dizayn ishlaydi
- [ ] Linklar to'g'ri ishlaydi

## Topshiriq 7: Qo'shimcha funksionallik (Ixtiyoriy)

### 7.1. Home sahifasini boyitish

```python
# views.py da home_view'ni yangilang
def home_view(request):
    # So'nggi yangiliklar
    latest_news = News.published.all()[:6]
    
    # Eng ko'p o'qilgan yangiliklar (agar views_count maydoni bo'lsa)
    # popular_news = News.published.order_by('-views_count')[:3]
    
    # Kategoriyalar bo'yicha yangiliklar
    # from .models import Category
    # categories = Category.objects.all()[:5]
    
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa',
        # 'popular_news': popular_news,
        # 'categories': categories,
    }
    return render(request, 'news/home.html', context)
```

### 7.2. Meta taglar qo'shish

```html
<!-- base.html head bo'limiga qo'shing -->
<meta name="description" content="Eng so'nggi yangiliklar va ma'lumotlar">
<meta name="keywords" content="yangiliklar, so'nggi xabarlar, Uzbekiston">
<meta name="author" content="Yangiliklar sayti">

<!-- Open Graph meta taglar (ijtimoiy tarmoqlar uchun) -->
<meta property="og:title" content="Yangiliklar Sayti">
<meta property="og:description" content="Eng so'nggi yangiliklar va ma'lumotlar">
<meta property="og:type" content="website">
```

## Tekshirish ro'yxati

Quyidagi barcha punktlar bajarilganini tekshiring:

### Views
- [ ] `home_view` funksiyasi yaratildi va to'g'ri ishlaydi
- [ ] `ContactView` klassi yaratildi va to'g'ri ishlaydi
- [ ] Context ma'lumotlari to'g'ri uzatilmoqda

### URLs
- [ ] `news/urls.py`da yangi URL'lar qo'shildi
- [ ] `config/urls.py` to'g'ri sozlangan
- [ ] URL nomlari to'g'ri berilgan (`app_name` ishlatilgan)

### Templates
- [ ] `home.html` template yaratildi va to'liq
- [ ] `contact.html` template yaratildi va to'liq
- [ ] Template'lar `base.html`dan extend qiladi
- [ ] Bootstrap klasslari to'g'ri ishlatilgan

### Navigation
- [ ] Base template'da navigation menu yangilangan
- [ ] Barcha havolalar to'g'ri ishlaydi
- [ ] Active sahifa ko'rsatilmoqda (ixtiyoriy)

### Functionality
- [ ] Bosh sahifada so'nggi yangiliklar ko'rsatilmoqda
- [ ] Yangilik rasmlar to'g'ri ko'rsatilmoqda
- [ ] Contact sahifasida barcha kerakli ma'lumotlar bor

## Keng tarqalgan xatoliklar va ularni tuzatish

### Xato 2: NoReverseMatch
```
Reverse for 'home' not found. 'home' is not a valid view function or pattern name.
```
**Yechim:**
- `urls.py`da URL name to'g'ri yozilganligini tekshiring
- `app_name = 'news'` qo'shilganligini tekshiring
- Template'da `{% url 'news:home' %}` ishlatilganligini tekshiring

### Xato 3: AttributeError: 'News' has no attribute 'published'
```
AttributeError: 'News' has no attribute 'published'
```
**Yechim:**
- `News` modelida `published` manager yaratilganligini tekshiring
- Yoki `News.objects.filter(status='PB')` ishlatilsin

### Xato 4: Static fayllar yuklanmayapti
**Yechim:**
```python
# settings.py da tekshiring
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Development uchun urls.py da
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Mustaqil topshiriqlar

### Topshiriq A: Advanced Home Page
1. Home sahifasiga kategoriya bo'yicha yangiliklar qo'shing
2. Search form qo'shing (keyingi darslarda ishlatiladigan)
3. Newsletter subscription form qo'shing

### Topshiriq B: Contact Page Enhancement
1. Contact sahifasiga Google Maps qo'shing
2. Working hours ma'lumotini qo'shing
3. FAQ section qo'shing

### Topshiriq C: SEO Optimization
1. Har bir sahifa uchun unique meta description yozing
2. Breadcrumb navigation qo'shing
3. Schema.org markup qo'shing

## Yechimlar va kodlar

### Home View to'liq yechimi:
```python
def home_view(request):
    """
    Bosh sahifa view'i - eng so'nggi yangiliklarni ko'rsatadi
    """
    # So'nggi 6 ta nashr etilgan yangiliklarni olamiz
    latest_news = News.published.all().order_by('-publish_time')[:6]
    
    # Context'ga ma'lumotlarni qo'shamiz
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa',
        'meta_description': 'Eng so\'nggi yangiliklar va ma\'lumotlardan xabardor bo\'ling',
    }
    return render(request, 'news/home.html', context)
```

### Contact View to'liq yechimi:
```python
class ContactView(TemplateView):
    """
    Contact sahifasi uchun class-based view
    """
    template_name = 'news/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Biz bilan bog\'lanish',
            'meta_description': 'Biz bilan bog\'laning va savollaringizni yo\'llang',
            'company_info': {
                'name': 'Yangiliklar sayti',
                'address': 'Toshkent shahri, Yunusobod tumani',
                'phone': '+998 90 123 45 67',
                'email': 'info@yangiliklar.uz',
                'working_hours': 'Dushanba - Juma: 9:00-18:00'
            }
        })
        return context
```

### URLs to'liq yechimi:
```python
# news/urls.py
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

### Home Template to'liq yechimi:
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block meta %}
<meta name="description" content="{{ meta_description }}">
<meta name="keywords" content="yangiliklar, so'nggi xabarlar, Uzbekiston">
{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="jumbotron jumbotron-fluid bg-primary text-white mb-0">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-md-8">
                <h1 class="display-4 font-weight-bold">Yangiliklar Saytiga Xush Kelibsiz!</h1>
                <p class="lead">Eng so'nggi va muhim yangiliklardan xabardor bo'ling. Har kuni yangi va qiziqarli ma'lumotlar.</p>
                <a class="btn btn-light btn-lg mt-3" href="{% url 'news:news_list' %}" role="button">
                    <i class="fas fa-newspaper"></i> Barcha yangiliklar
                </a>
            </div>
            <div class="col-md-4 text-center">
                <i class="fas fa-globe fa-5x opacity-50"></i>
            </div>
        </div>
    </div>
</div>

<!-- Latest News Section -->
<div class="container mt-5">
    <div class="row">
        <div class="col-12 text-center mb-5">
            <h2 class="display-5">So'nggi yangiliklar</h2>
            <p class="lead text-muted">Eng muhim va qiziq yangiliklarni o'qing</p>
            <hr class="w-25 mx-auto">
        </div>
    </div>
    
    <div class="row">
        {% for news in latest_news %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 shadow-sm">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" class="card-img-top" alt="{{ news.title }}" style="height: 200px; object-fit: cover;">
                {% else %}
                <div class="card-img-top bg-secondary d-flex align-items-center justify-content-center text-white" style="height: 200px;">
                    <i class="fas fa-image fa-3x opacity-50"></i>
                </div>
                {% endif %}
                
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ news.title|truncatechars:60 }}</h5>
                    <p class="card-text text-muted">{{ news.body|truncatewords:20 }}</p>
                    
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d.m.Y" }}
                            </small>
                            <small class="text-muted">
                                <i class="fas fa-clock"></i> {{ news.publish_time|date:"H:i" }}
                            </small>
                        </div>
                        <a href="{% url 'news:news_detail' news.id %}" class="btn btn-primary btn-sm mt-2 w-100">
                            <i class="fas fa-arrow-right"></i> Batafsil o'qish
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle fa-2x mb-3"></i>
                <h4>Yangiliklar topilmadi</h4>
                <p>Hozircha yangiliklar mavjud emas. Tez orada yangi ma'lumotlar qo'shiladi.</p>
            </div>
        </div>
        {% endfor %}
    </div>
    
    {% if latest_news %}
    <div class="row mt-4">
        <div class="col-12 text-center">
            <a href="{% url 'news:news_list' %}" class="btn btn-outline-primary btn-lg">
                <i class="fas fa-list"></i> Barcha yangiliklarni ko'rish
            </a>
        </div>
    </div>
    {% endif %}
</div>

<!-- Call to Action Section -->
<div class="bg-light mt-5 py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto text-center">
                <h3 class="display-6">Bizning yangiliklarimizni kuzatib boring!</h3>
                <p class="lead">Har kuni yangi va qiziq yangiliklarni e'lon qilamiz. Muhim voqealardan birinchi bo'lib xabardor bo'ling.</p>
                
                <div class="row mt-4">
                    <div class="col-md-4 mb-3">
                        <div class="text-primary">
                            <i class="fas fa-clock fa-2x"></i>
                        </div>
                        <h5 class="mt-2">Har kuni yangilik</h5>
                        <p class="text-muted">Kundalik yangi ma'lumotlar</p>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="text-primary">
                            <i class="fas fa-shield-alt fa-2x"></i>
                        </div>
                        <h5 class="mt-2">Ishonchli manba</h5>
                        <p class="text-muted">Tekshirilgan ma'lumotlar</p>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="text-primary">
                            <i class="fas fa-users fa-2x"></i>
                        </div>
                        <h5 class="mt-2">Katta jamiyat</h5>
                        <p class="text-muted">Minglab o'quvchilar</p>
                    </div>
                </div>
                
                <a href="{% url 'news:contact' %}" class="btn btn-primary btn-lg mt-3">
                    <i class="fas fa-envelope"></i> Biz bilan bog'lanish
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Contact Template to'liq yechimi:
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }} - Yangiliklar sayti{% endblock %}

{% block meta %}
<meta name="description" content="{{ meta_description }}">
{% endblock %}

{% block content %}
<div class="container mt-4 mb-5">
    <!-- Page Header -->
    <div class="row mb-5">
        <div class="col-12 text-center">
            <h1 class="display-5">{{ page_title }}</h1>
            <p class="lead text-muted">Biz bilan bog'laning va savollaringizni yo'llang</p>
            <hr class="w-25 mx-auto">
        </div>
    </div>
    
    <div class="row">
        <!-- Contact Form -->
        <div class="col-lg-8 mb-4">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-paper-plane"></i> Xabar yuborish
                    </h4>
                </div>
                <div class="card-body">
                    <p class="text-muted mb-4">Quyidagi formani to'ldirish orqali biz bilan bog'lanishingiz mumkin. Barcha maydonlarni to'ldirish majburiy.</p>
                    
                    <form method="post" id="contactForm">
                        {% csrf_token %}
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="name">
                                        <i class="fas fa-user text-primary"></i> Ismingiz *
                                    </label>
                                    <input type="text" class="form-control" id="name" name="name" required placeholder="To'liq ismingizni kiriting">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="email">
                                        <i class="fas fa-envelope text-primary"></i> Email manzili *
                                    </label>
                                    <input type="email" class="form-control" id="email" name="email" required placeholder="example@email.com">
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="subject">
                                <i class="fas fa-tag text-primary"></i> Xabar mavzusi *
                            </label>
                            <input type="text" class="form-control" id="subject" name="subject" required placeholder="Xabaringiz mavzusini kiriting">
                        </div>
                        
                        <div class="form-group">
                            <label for="message">
                                <i class="fas fa-comment text-primary"></i> Xabaringiz *
                            </label>
                            <textarea class="form-control" id="message" name="message" rows="6" required placeholder="Xabaringizni batafsil yozing..."></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-paper-plane"></i> Xabar yuborish
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Contact Information -->
        <div class="col-lg-4">
            <!-- Contact Details -->
            <div class="card shadow mb-4">
                <div class="card-header bg-info text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-info-circle"></i> Aloqa ma'lumotlari
                    </h4>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <h6 class="text-primary">
                            <i class="fas fa-building"></i> Kompaniya nomi:
                        </h6>
                        <p class="mb-0">{{ company_info.name }}</p>
                    </div>
                    
                    <div class="mb-3">
                        <h6 class="text-primary">
                            <i class="fas fa-map-marker-alt"></i> Manzil:
                        </h6>
                        <p class="mb-0">{{ company_info.address }}<br>
                        Amir Temur ko'chasi, 123-uy</p>
                    </div>
                    
                    <div class="mb-3">
                        <h6 class="text-primary">
                            <i class="fas fa-phone"></i> Telefon:
                        </h6>
                        <p class="mb-0">
                            <a href="tel:{{ company_info.phone }}" class="text-decoration-none">
                                {{ company_info.phone }}
                            </a>
                        </p>
                    </div>
                    
                    <div class="mb-3">
                        <h6 class="text-primary">
                            <i class="fas fa-envelope"></i> Email:
                        </h6>
                        <p class="mb-0">
                            <a href="mailto:{{ company_info.email }}" class="text-decoration-none">
                                {{ company_info.email }}
                            </a>
                        </p>
                    </div>
                    
                    <div class="mb-0">
                        <h6 class="text-primary">
                            <i class="fas fa-clock"></i> Ish vaqti:
                        </h6>
                        <p class="mb-0">{{ company_info.working_hours }}<br>
                        Shanba: 9:00 - 14:00<br>
                        Yakshanba: Dam olish</p>
                    </div>
                </div>
            </div>
            
            <!-- Social Media -->
            <div class="card shadow mb-4">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-share-alt"></i> Ijtimoiy tarmoqlar
                    </h4>
                </div>
                <div class="card-body text-center">
                    <p class="text-muted mb-3">Bizni ijtimoiy tarmoqlarda kuzatib boring</p>
                    <div class="d-flex flex-wrap justify-content-center">
                        <a href="#" class="btn btn-primary btn-sm m-1" target="_blank">
                            <i class="fab fa-facebook-f"></i> Facebook
                        </a>
                        <a href="#" class="btn btn-info btn-sm m-1" target="_blank">
                            <i class="fab fa-twitter"></i> Twitter
                        </a>
                        <a href="#" class="btn btn-primary btn-sm m-1" target="_blank">
                            <i class="fab fa-telegram"></i> Telegram
                        </a>
                        <a href="#" class="btn btn-danger btn-sm m-1" target="_blank">
                            <i class="fab fa-instagram"></i> Instagram
                        </a>
                        <a href="#" class="btn btn-danger btn-sm m-1" target="_blank">
                            <i class="fab fa-youtube"></i> YouTube
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Quick Links -->
            <div class="card shadow">
                <div class="card-header bg-warning text-dark">
                    <h4 class="mb-0">
                        <i class="fas fa-link"></i> Foydali havolalar
                    </h4>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <a href="{% url 'news:home' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-home"></i> Bosh sahifa
                        </a>
                        <a href="{% url 'news:news_list' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-newspaper"></i> Barcha yangiliklar
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <i class="fas fa-question-circle"></i> Tez-tez so'raladigan savollar
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <i class="fas fa-shield-alt"></i> Maxfiylik siyosati
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Contact form validation
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Simple validation
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    
    if (name && email && subject && message) {
        alert('Xabaringiz muvaffaqiyatli yuborildi! Tez orada javob beramiz.');
        // Bu yerda real formani yuborish logikasi bo'lishi kerak
    } else {
        alert('Iltimos, barcha maydonlarni to\'ldiring.');
    }
});
</script>
{% endblock %}
```

### Navigation Menu to'liq yechimi:
```html
<!-- base.html ichida navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
    <div class="container">
        <a class="navbar-brand font-weight-bold" href="{% url 'news:home' %}">
            <i class="fas fa-newspaper text-primary"></i> Yangiliklar
        </a>
        
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false">
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

## Yakuniy tekshirish va baholash

### 1. Funksionallik testi
Quyidagi barcha punktlar ishlashini tekshiring:

**Bosh sahifa (/):**
- [ ] Sahifa to'g'ri yuklanadi (200 status)
- [ ] Hero section ko'rsatiladi
- [ ] So'nggi yangiliklar ko'rsatiladi (6 ta)
- [ ] Yangilik kartalarida rasm, sarlavha, qisqacha matn bor
- [ ] "Batafsil o'qish" tugmalari ishlaydi
- [ ] Call-to-action bo'limi mavjud

**Contact sahifasi (/contact/):**
- [ ] Sahifa to'g'ri yuklanadi
- [ ] Contact form barcha maydonlar bilan ko'rsatiladi
- [ ] Aloqa ma'lumotlari to'liq ko'rsatiladi
- [ ] Ijtimoiy tarmoq havolalari mavjud
- [ ] Responsive dizayn ishlaydi

**Navigation menu:**
- [ ] Barcha sahifalarda ko'rsatiladi
- [ ] Linklar to'g'ri ishlaydi
- [ ] Mobile versiyada hamburger menu ishlaydi

### 2. Kod sifatini baholash

**Views.py tekshiruvi:**
```python
# To'g'ri yozilgan kod misoli
def home_view(request):
    latest_news = News.published.all()[:6]  # ✓ To'g'ri
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa'
    }
    return render(request, 'news/home.html', context)  # ✓ To'g'ri
```

**URLs.py tekshiruvi:**
- [ ] `app_name = 'news'` mavjud
- [ ] URL patterns to'g'ri yozilgan
- [ ] Name parametrlari berilgan

### 3. Template sifatini baholash

**HTML struktura:**
- [ ] `{% extends 'base.html' %}` ishlatilgan
- [ ] `{% load static %}` qo'shilgan (agar kerak bo'lsa)
- [ ] Bootstrap klasslari to'g'ri ishlatilgan
- [ ] Semantic HTML ishlatilgan

**Template filterlari:**
- [ ] `|truncatechars` va `|truncatewords` to'g'ri ishlatilgan
- [ ] `|date` filteri to'g'ri formatlangan
- [ ] `{% empty %}` tag ishlatilgan

### 4. Performance va UX baholash

**Yuklanish tezligi:**
- [ ] Sahifalar 3 soniyadan tez yuklanadi
- [ ] Rasmlar optimize qilingan
- [ ] CSS va JS fayllar to'g'ri ulangan

**User Experience:**
- [ ] Sahifalar intuitiv va oson foydalanish
- [ ] Button'lar va linklar aniq ko'rinadi
- [ ] Xato holatlarda mos xabarlar ko'rsatiladi

## Yakuniy loyiha testi

### Terminal orqali test
```bash
# Server ishga tushuring
python manage.py runserver

# Yangi terminal oynasida quyidagi URL'larni tekshiring:
curl -I http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/contact/
curl -I http://127.0.0.1:8000/news/
```

Barcha URL'lar 200 status qaytarishi kerak.

### Browser'da test
1. **Desktop versiyasini tekshiring:**
   - Chrome, Firefox, Safari da oching
   - Barcha funksiyalar ishlashini tekshiring

2. **Mobile versiyasini tekshiring:**
   - Developer tools'da mobile view'ni yoqing
   - Responsive dizayn ishlashini tekshiring

## Kodni yaxshilash bo'yicha maslahatlar

### 1. SEO yaxshilash
```html
<!-- base.html head qismiga qo'shing -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{{ request.build_absolute_uri }}">
```

### 2. Performance yaxshilash
```python
# views.py da caching qo'shing
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 daqiqa cache
def home_view(request):
    # kod...
```

### 3. Error handling yaxshilash
```python
# views.py da try-except qo'shing
def home_view(request):
    try:
        latest_news = News.published.all()[:6]
    except Exception as e:
        # Log the error
        latest_news = []
    
    context = {
        'latest_news': latest_news,
        'page_title': 'Bosh sahifa'
    }
    return render(request, 'news/home.html', context)
```

## Keyingi qadamlar

### 1. Qo'shimcha funksiyalar (ixtiyoriy)
- Search functionality qo'shish
- Newsletter subscription
- Social media sharing buttons
- Breadcrumb navigation

### 2. Testing yozish
```python
# tests.py faylida
from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, 'Yangiliklar Saytiga Xush Kelibsiz!')
```

### 3. Documentation yozish
```markdown
# Home va Contact sahifalari

## Maqsad
Bu sahifalar saytning asosiy kirish nuqtalari hisoblanadi.

## Foydalanish
- Home: Eng so'nggi yangiliklarni ko'rsatish
- Contact: Foydalanuvchilar bilan aloqa o'rnatish

## Texnik ma'lumotlar
- Views: Function-based va Class-based
- Templates: Bootstrap 4 ishlatilgan
- Caching: 15 daqiqa
```

## Loyiha holati xulosasi

### Muvaffaqiyatli bajarilgan
- Home sahifasi to'liq yaratildi
- Contact sahifasi professional ko'rinishda
- Navigation system ishlaydi
- Responsive dizayn qo'llanildi
- Code best practice'larga mos

### 🔄 Keyingi bosqichlar
- Contact form functionality (19-dars)
- Search va filtering (kelajakda)
- User authentication (kelajakda)
- Admin panel customization (kelajakda)

### 📊 O'rganilgan texnologiyalar
- Django Views (Function & Class-based)
- URL routing va namespacing
- Template inheritance va context
- Bootstrap responsive design
- Navigation systems

## Tabriklaymiz! 

Siz muvaffaqiyatli Home va Contact sahifalarini yaratdingiz. Bu Django'da web development'ning asosiy qismidir. Sizning loyihangiz endi:

- Professional ko'rinishga ega
- Foydalanuvchi uchun qulay
- SEO-friendly
- Responsive dizaynli
- Kengaytirish uchun tayyor
