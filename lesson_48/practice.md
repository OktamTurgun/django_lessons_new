# Lesson 48: Ko'rishlar sonini template'da aks ettirish - Amaliyot

## Amaliyot maqsadi

Ushbu amaliyotda siz:
- Ko'rishlar sonini yangilik detail sahifasida ko'rsatasiz
- Yangiliklar ro'yxatida ko'rishlar sonini qo'shasiz
- Humanize filteridan foydalanasiz
- Custom template filterlar yaratasiz
- Eng ko'p ko'rilgan yangiliklarni sidebar'da ko'rsatasiz

## Boshlash

Avval loyihangizni ishga tushiring va virtual muhitni faollashtiring:

```bash
cd newspaper_project
pipenv shell
python manage.py runserver
```

## Topshiriq 1: Humanize ilovasini o'rnatish

### 1.1. settings.py faylini ochish

`config/settings.py` faylini oching.

### 1.2. Humanize qo'shish

`INSTALLED_APPS` ro'yxatiga `django.contrib.humanize` qo'shing:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'django.contrib.humanize',  # Bu qatorni qo'shing
    
    # Local apps
    'news_app',
    'accounts',
]
```

### 1.3. Saqlash va tekshirish

Faylni saqlang va serverni qayta ishga tushiring.

**Natija:** Humanize ilova muvaffaqiyatli o'rnatildi.

---

## Topshiriq 2: Detail sahifada ko'rishlar sonini ko'rsatish

### 2.1. news_detail.html faylini ochish

`templates/news/news_detail.html` faylini oching.

### 2.2. Humanize yukash

Fayl boshiga humanize'ni yuklaymiz:

```html
{% extends 'base.html' %}
{% load static %}
{% load humanize %}  <!-- Bu qatorni qo'shing -->
```

### 2.3. Ko'rishlar sonini qo'shish

Meta ma'lumotlar qismiga ko'rishlar sonini qo'shing:

```html
<div class="text-muted mb-3">
    <i class="fas fa-user"></i> {{ news.author.get_full_name }}
    <span class="mx-2">|</span>
    <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
    <span class="mx-2">|</span>
    <i class="fas fa-folder"></i> {{ news.category.name }}
    <span class="mx-2">|</span>
    <!-- Bu qismni qo'shing -->
    <i class="fas fa-eye"></i> {{ news.views_count|intcomma }} ko'rishlar
</div>
```

### 2.4. Natijani tekshirish

Brauzerda biror yangilik sahifasini oching va ko'rishlar sonini ko'ring.

**Natija:** Yangilik sahifasida ko'rishlar soni ko'rinmoqda.

---

## Topshiriq 3: Yangiliklar ro'yxatida ko'rsatish

### 3.1. news_list.html faylini ochish

`templates/news/news_list.html` yoki `index.html` faylini oching.

### 3.2. Card footer qo'shish

Har bir yangilik kartochkasiga footer qo'shing:

```html
{% for news in news_list %}
<div class="col-lg-4 col-md-6 mb-4">
    <div class="card h-100">
        <!-- Rasm -->
        {% if news.image %}
        <img class="card-img-top" src="{{ news.image.url }}" alt="{{ news.title }}">
        {% endif %}
        
        <div class="card-body">
            <span class="badge badge-primary">{{ news.category.name }}</span>
            <h5 class="card-title mt-2">
                <a href="{{ news.get_absolute_url }}">{{ news.title }}</a>
            </h5>
            <p class="card-text">{{ news.body|truncatewords:20|striptags }}</p>
        </div>
        
        <!-- Bu qismni qo'shing -->
        <div class="card-footer text-muted">
            <div class="d-flex justify-content-between align-items-center">
                <small>
                    <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                </small>
                <small>
                    <i class="fas fa-eye"></i> {{ news.views_count|intcomma }}
                </small>
            </div>
        </div>
    </div>
</div>
{% endfor %}
```

### 3.3. Natijani tekshirish

Bosh sahifani oching va har bir kartochkada ko'rishlar sonini ko'ring.

**Natija:** Barcha yangilik kartochkalarida ko'rishlar soni ko'rinmoqda.

---

## Topshiriq 4: Custom template filter yaratish

### 4.1. templatetags papkasini yaratish

`news_app` papkasida `templatetags` papkasini yarating:

```
news_app/
    templatetags/
```

### 4.2. __init__.py fayli yaratish

`templatetags` papkasida bo'sh `__init__.py` faylini yarating.

### 4.3. news_tags.py fayli yaratish

`templatetags` papkasida `news_tags.py` faylini yarating va quyidagi kodni yozing:

```python
from django import template

register = template.Library()

@register.filter
def compact_number(value):
    """
    Raqamni qisqa formatda ko'rsatadi.
    1000 → 1K
    1500 → 1.5K
    1000000 → 1M
    """
    try:
        value = int(value)
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return str(value)
    except (ValueError, TypeError):
        return value
```

### 4.4. Template'da ishlatish

`news_list.html` faylida filterdan foydalaning:

```html
{% load news_tags %}  <!-- Bu qatorni qo'shing -->
{% load humanize %}

<!-- ... -->

<small>
    <i class="fas fa-eye"></i> {{ news.views_count|compact_number }}
</small>
```

### 4.5. Serverni qayta ishga tushirish

Template taglarni o'zgartirganingizdan keyin serverni qayta ishga tushiring:

```bash
# Ctrl+C bilan to'xtating
python manage.py runserver
```

### 4.6. Natijani tekshirish

Bosh sahifani yangilang va raqamlarning qisqa formatda ko'rinishini tekshiring.

**Natija:** Katta raqamlar K va M bilan ko'rinmoqda (masalan: 1.5K).

---

## Topshiriq 5: Eng ko'p ko'rilgan yangiliklarni ko'rsatish

### 5.1. views.py faylini yangilash

`news_app/views.py` faylini oching va `NewsDetailView` ni yangilang:

```python
from django.views.generic import DetailView
from django.db.models import F
from .models import News

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = F('views_count') + 1
        obj.save(update_fields=['views_count'])
        obj.refresh_from_db()
        return obj
    
    # Bu metodini qo'shing
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Eng ko'p ko'rilgan 5 ta yangiliklarni qo'shamiz
        context['most_viewed'] = News.published.order_by('-views_count')[:5]
        return context
```

### 5.2. Template'da sidebar yaratish

`news_detail.html` faylida sidebar qo'shing:

```html
{% extends 'base.html' %}
{% load static %}
{% load humanize %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Asosiy kontent -->
        <div class="col-lg-8">
            <h1>{{ news.title }}</h1>
            
            <div class="text-muted mb-3">
                <i class="fas fa-user"></i> {{ news.author.get_full_name }}
                <span class="mx-2">|</span>
                <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                <span class="mx-2">|</span>
                <i class="fas fa-folder"></i> {{ news.category.name }}
                <span class="mx-2">|</span>
                <i class="fas fa-eye"></i> {{ news.views_count|intcomma }} ko'rishlar
            </div>
            
            {% if news.image %}
            <img class="img-fluid rounded mb-4" src="{{ news.image.url }}" alt="{{ news.title }}">
            {% endif %}
            
            <div class="mt-4">
                {{ news.body|safe }}
            </div>
        </div>
        
        <!-- Sidebar - Bu qismni qo'shing -->
        <div class="col-lg-4">
            <div class="card mb-4">
                <h5 class="card-header">Eng ko'p o'qilganlar</h5>
                <div class="card-body">
                    <ul class="list-unstyled">
                        {% for item in most_viewed %}
                        <li class="mb-3 pb-3 border-bottom">
                            <a href="{{ item.get_absolute_url }}" class="text-decoration-none">
                                <h6>{{ item.title|truncatewords:8 }}</h6>
                            </a>
                            <div class="text-muted small">
                                <i class="fas fa-eye"></i> {{ item.views_count|intcomma }} ko'rishlar
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.3. Natijani tekshirish

Yangilik sahifasini oching va o'ng tomonda eng ko'p ko'rilgan yangiliklarni ko'ring.

**Natija:** Sidebar'da eng mashhur 5 ta yangilik ko'rinmoqda.

---

## Topshiriq 6: Ko'rishlar soniga rang qo'shish

### 6.1. CSS fayli yaratish

`static/css/style.css` faylini yarating (agar yo'q bo'lsa):

```css
/* static/css/style.css */

.views-count {
    display: inline-flex;
    align-items: center;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 500;
}

.views-low {
    background-color: #e3f2fd;
    color: #1976d2;
}

.views-medium {
    background-color: #fff3e0;
    color: #f57c00;
}

.views-high {
    background-color: #fce4ec;
    color: #c2185b;
}

.views-viral {
    background-color: #f3e5f5;
    color: #7b1fa2;
}

.views-count i {
    margin-right: 4px;
}
```

### 6.2. CSS'ni base.html'ga ulash

`base.html` faylida CSS'ni ulang:

```html
<head>
    <!-- ... boshqa linklar ... -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
```

### 6.3. Custom filter qo'shish

`news_app/templatetags/news_tags.py` faylini yangilang:

```python
from django import template

register = template.Library()

@register.filter
def compact_number(value):
    """Raqamni qisqa formatda ko'rsatadi"""
    try:
        value = int(value)
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return str(value)
    except (ValueError, TypeError):
        return value

# Bu yangi filterni qo'shing
@register.filter
def views_class(count):
    """Ko'rishlar soniga qarab CSS class qaytaradi"""
    try:
        count = int(count)
        if count < 100:
            return 'views-low'
        elif count < 500:
            return 'views-medium'
        elif count < 1000:
            return 'views-high'
        else:
            return 'views-viral'
    except (ValueError, TypeError):
        return 'views-low'
```

### 6.4. Template'da ishlatish

`news_list.html` faylida class qo'shing:

```html
{% load news_tags %}

<div class="card-footer text-muted">
    <div class="d-flex justify-content-between align-items-center">
        <small>
            <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
        </small>
        <!-- Bu qismni o'zgartiring -->
        <small class="views-count {{ news.views_count|views_class }}">
            <i class="fas fa-eye"></i> {{ news.views_count|compact_number }}
        </small>
    </div>
</div>
```

### 6.5. Serverni qayta ishga tushirish

```bash
# Ctrl+C
python manage.py runserver
```

### 6.6. Natijani tekshirish

Bosh sahifani yangilang va ko'rishlar soniga qarab turli ranglardagi badge'larni ko'ring.

**Natija:** Ko'rishlar soni ranglar bilan ajratilgan.

---

## Topshiriq 7: Test ma'lumotlari yaratish

### 7.1. Django shell ochish

```bash
python manage.py shell
```

### 7.2. Yangiliklarning ko'rishlar sonini o'zgartirish

```python
from news_app.models import News

# Barcha yangiliklarni olamiz
news_list = News.objects.all()

# Har biriga tasodifiy ko'rishlar soni beramiz
import random

for news in news_list:
    news.views_count = random.randint(50, 2000)
    news.save()

# Tekshirish
for news in News.objects.all()[:5]:
    print(f"{news.title}: {news.views_count} ko'rishlar")

# Shell'dan chiqish
exit()
```

### 7.3. Natijani brauzerda tekshirish

Bosh sahifani yangilang va turli xil ko'rishlar sonlariga ega yangiliklarni ko'ring.

**Natija:** Yangiliklarning ko'rishlar soni turli xil va ranglar bilan ajratilgan.

---

## Topshiriq 8: Qo'shimcha funksiyalar

### 8.1. Bugungi eng ko'p ko'rilganlar

`views.py` da yangi context qo'shing:

```python
from django.utils import timezone
from datetime import timedelta

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = F('views_count') + 1
        obj.save(update_fields=['views_count'])
        obj.refresh_from_db()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Eng ko'p ko'rilganlar
        context['most_viewed'] = News.published.order_by('-views_count')[:5]
        
        # Bugungi eng ko'p ko'rilganlar (qo'shimcha)
        today = timezone.now().date()
        context['today_popular'] = News.published.filter(
            publish_time__date=today
        ).order_by('-views_count')[:3]
        
        return context
```

### 8.2. Template'da ko'rsatish

Sidebar'ga qo'shimcha kartochka qo'shing:

```html
<div class="col-lg-4">
    <!-- Eng ko'p ko'rilganlar -->
    <div class="card mb-4">
        <h5 class="card-header">Eng ko'p o'qilganlar</h5>
        <div class="card-body">
            <!-- ... oldingi kod ... -->
        </div>
    </div>
    
    <!-- Bugungi mashhurlar - Yangi kartochka -->
    {% if today_popular %}
    <div class="card mb-4">
        <h5 class="card-header">Bugungi mashhurlar</h5>
        <div class="card-body">
            <ul class="list-unstyled">
                {% for item in today_popular %}
                <li class="mb-3 pb-3 border-bottom">
                    <a href="{{ item.get_absolute_url }}" class="text-decoration-none">
                        <h6>{{ item.title|truncatewords:8 }}</h6>
                    </a>
                    <div class="text-muted small">
                        <i class="fas fa-eye"></i> {{ item.views_count|intcomma }}
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
    {% endif %}
</div>
```

---

## Yakuniy tekshirish

### Tekshirish ro'yxati:

- [ ] Humanize ilova o'rnatilgan
- [ ] Detail sahifada ko'rishlar soni ko'rinmoqda
- [ ] Yangiliklar ro'yxatida ko'rishlar soni bor
- [ ] Custom filter ishlayapti (K, M formatda)
- [ ] Eng ko'p ko'rilganlar sidebar'da
- [ ] Ko'rishlar soniga ranglar qo'shilgan
- [ ] Sahifa yangilanganda ko'rishlar soni oshadi

### Agar xato bo'lsa:

**Xato 1:** Template tag topilmadi
```
Yechim: Serverni qayta ishga tushiring
python manage.py runserver
```

**Xato 2:** CSS ishlamayapti
```
Yechim: Static fayllarni to'plang
python manage.py collectstatic
```

**Xato 3:** Ko'rishlar soni oshmiayapti
```
Yechim: views.py da get_object metodini tekshiring
```

---

## Qo'shimcha mashqlar

### Mashq 1: Haftalik top yangiliklarni ko'rsatish

O'z kuchingiz bilan haftalik eng ko'p ko'rilgan 10 ta yangiliklarni alohida sahifada ko'rsating.

**Maslahat:**
```python
from datetime import timedelta
from django.utils import timezone

last_week = timezone.now() - timedelta(days=7)
weekly_top = News.published.filter(
    publish_time__gte=last_week
).order_by('-views_count')[:10]
```

### Mashq 2: Kategoriya bo'yicha eng mashhur

Har bir kategoriya uchun eng ko'p ko'rilgan yangiliklarni ko'rsating.

**Maslahat:**
```python
from .models import Category

for category in Category.objects.all():
    top_news = category.news_set.order_by('-views_count')[:3]
```

### Mashq 3: Ko'rishlar soni grafikda

Chart.js yordamida ko'rishlar sonini grafikda ko'rsating.

**Maslahat:** Django'dan JSON formatda ma'lumot yuborib, JavaScript'da grafik chizish.

---

## Xulosa

Tabriklaymiz! Siz muvaffaqiyatli:
✅ Ko'rishlar sonini detail sahifada ko'rsatdingiz
✅ Yangiliklar ro'yxatida ko'rishlar sonini qo'shdingiz
✅ Humanize filteridan foydalandingiz
✅ Custom template filterlar yaratdingiz
✅ Eng ko'p ko'rilgan yangiliklarni ko'rsatdingiz
✅ Ko'rishlar soniga ranglar qo'shdingiz

Keyingi darsda izohlar sonini template'dan chiqarishni va loyihani GitHub'ga saqlashni o'rganamiz!