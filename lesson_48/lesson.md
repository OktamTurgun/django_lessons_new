# Lesson 48: Ko'rishlar sonini template'da aks ettirish

## Kirish

Oldingi darsda biz yangilik sahifasi ochilganda ko'rishlar sonini avtomatik ravishda oshirib boradigan funksiyani yaratdik. Ushbu darsda esa ko'rishlar sonini template'da chiroyli ko'rinishda aks ettirishni o'rganamiz. Bu foydalanuvchilarga qaysi yangiliklarning mashhur ekanligini ko'rsatadi.

## Nazariy qism

### Ko'rishlar sonini qayerda ko'rsatish mumkin?

Ko'rishlar sonini turli joylarda ko'rsatish mumkin:

1. **Yangiliklar ro'yxatida** - Har bir yangilik kartochkasida
2. **Yangilik batafsil sahifasida** - Yangilik sarlavhasi yonida
3. **Eng ko'p ko'rilganlar bo'limida** - Top yangiliklarni ko'rsatishda
4. **Admin panelda** - Statistika uchun

### Template'da raqamlarni formatlash

Django'da raqamlarni chiroyli ko'rinishda ko'rsatish uchun built-in filterlar mavjud:

```django
{{ news.views_count }}  # Oddiy ko'rinish: 1234
{{ news.views_count|intcomma }}  # Vergul bilan: 1,234
```

## Amaliy qism

### 1-bosqich: Detail sahifada ko'rishlar sonini ko'rsatish

Yangilik batafsil sahifasida ko'rishlar sonini qo'shamiz.

**news_detail.html** faylini ochamiz:

```html
<!-- templates/news/news_detail.html -->

{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8">
            <!-- Yangilik sarlavhasi -->
            <h1 class="mt-4">{{ news.title }}</h1>
            
            <!-- Meta ma'lumotlar -->
            <div class="text-muted mb-3">
                <i class="fas fa-user"></i> {{ news.author.get_full_name }}
                <span class="mx-2">|</span>
                <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                <span class="mx-2">|</span>
                <i class="fas fa-folder"></i> {{ news.category.name }}
                <span class="mx-2">|</span>
                <i class="fas fa-eye"></i> {{ news.views_count }} ko'rishlar
            </div>
            
            <!-- Yangilik rasmi -->
            {% if news.image %}
            <img class="img-fluid rounded" src="{{ news.image.url }}" alt="{{ news.title }}">
            {% endif %}
            
            <!-- Yangilik matni -->
            <div class="mt-4">
                {{ news.body|safe }}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Tushuntirish:**
- `<i class="fas fa-eye"></i>` - Ko'z ikonkasi (FontAwesome)
- `{{ news.views_count }}` - Ko'rishlar sonini chiqaradi
- `ko'rishlar` - O'zbekcha matn qo'shamiz

### 2-bosqich: Yangiliklar ro'yxatida ko'rsatish

Bosh sahifadagi yangiliklar kartochkalarida ham ko'rishlar sonini qo'shamiz.

**news_list.html** faylini yangilaymiz:

```html
<!-- templates/news/news_list.html -->

{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row">
        {% for news in news_list %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100">
                <!-- Rasm -->
                {% if news.image %}
                <img class="card-img-top" src="{{ news.image.url }}" alt="{{ news.title }}">
                {% else %}
                <img class="card-img-top" src="{% static 'images/default-news.jpg' %}" alt="Default image">
                {% endif %}
                
                <div class="card-body">
                    <!-- Kategoriya -->
                    <span class="badge badge-primary">{{ news.category.name }}</span>
                    
                    <!-- Sarlavha -->
                    <h5 class="card-title mt-2">
                        <a href="{{ news.get_absolute_url }}">{{ news.title }}</a>
                    </h5>
                    
                    <!-- Qisqacha matn -->
                    <p class="card-text">{{ news.body|truncatewords:20|striptags }}</p>
                </div>
                
                <div class="card-footer text-muted">
                    <div class="d-flex justify-content-between align-items-center">
                        <small>
                            <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                        </small>
                        <small>
                            <i class="fas fa-eye"></i> {{ news.views_count }}
                        </small>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

**Tushuntirish:**
- `card-footer` - Kartochka pastki qismida meta ma'lumotlarni joylashtirdik
- `d-flex justify-content-between` - Ma'lumotlarni ikki tomonga yoyamiz
- Ko'rishlar sonini sana bilan birga qo'ydik

### 3-bosqich: Humanize filteridan foydalanish

Katta raqamlarni chiroyli ko'rsatish uchun Django'ning `humanize` ilovasidan foydalanamiz.

**settings.py** ga humanize qo'shamiz:

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'django.contrib.humanize',  # Yangi qo'shamiz
    
    # Local apps
    'news_app',
    'accounts',
]
```

**Template'da humanize filterini ishlatamiz:**

```html
<!-- templates/news/news_detail.html -->

{% extends 'base.html' %}
{% load static %}
{% load humanize %}  <!-- Humanize yuklaymiz -->

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8">
            <h1 class="mt-4">{{ news.title }}</h1>
            
            <div class="text-muted mb-3">
                <i class="fas fa-user"></i> {{ news.author.get_full_name }}
                <span class="mx-2">|</span>
                <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                <span class="mx-2">|</span>
                <i class="fas fa-folder"></i> {{ news.category.name }}
                <span class="mx-2">|</span>
                <i class="fas fa-eye"></i> {{ news.views_count|intcomma }} ko'rishlar
            </div>
            
            <!-- Qolgan kod... -->
        </div>
    </div>
</div>
{% endblock %}
```

**Natija:**
- 1234 → 1,234
- 1234567 → 1,234,567

### 4-bosqich: Eng ko'p ko'rilgan yangiliklarni ko'rsatish

Sidebar'da eng ko'p ko'rilgan yangiliklarni ko'rsatamiz.

**views.py** da context'ga yangi ma'lumot qo'shamiz:

```python
# news_app/views.py

from django.views.generic import DetailView, ListView
from .models import News

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Eng ko'p ko'rilgan 5 ta yangiliklarni qo'shamiz
        context['most_viewed'] = News.published.order_by('-views_count')[:5]
        
        return context
```

**Tushuntirish:**
- `order_by('-views_count')` - Ko'rishlar soni bo'yicha kamayish tartibida saralanadi
- `[:5]` - Faqat birinchi 5 tasini olamiz
- `context['most_viewed']` - Template'da `most_viewed` nomi bilan ishlatamiz

**Template'da ko'rsatamiz:**

```html
<!-- templates/news/news_detail.html -->

{% extends 'base.html' %}
{% load static %}
{% load humanize %}

{% block content %}
<div class="container">
    <div class="row">
        <!-- Asosiy kontent -->
        <div class="col-lg-8">
            <!-- Yangilik matni... -->
        </div>
        
        <!-- Sidebar -->
        <div class="col-lg-4">
            <div class="card mb-4">
                <h5 class="card-header">Eng ko'p o'qilganlar</h5>
                <div class="card-body">
                    <ul class="list-unstyled">
                        {% for item in most_viewed %}
                        <li class="mb-3">
                            <a href="{{ item.get_absolute_url }}">
                                {{ item.title|truncatewords:8 }}
                            </a>
                            <div class="text-muted small">
                                <i class="fas fa-eye"></i> {{ item.views_count|intcomma }}
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

**Tushuntirish:**
- Sidebar'da alohida kartochka yaratdik
- `list-unstyled` - List stillarini olib tashlaymiz
- Har bir yangilik uchun sarlavha va ko'rishlar sonini ko'rsatamiz

### 5-bosqich: Custom template filter yaratish

O'zimizning maxsus filterimizni yaratamiz - raqamni qisqartirib ko'rsatish uchun.

**news_app** papkasida **templatetags** papkasini yaratamiz:

```
news_app/
    templatetags/
        __init__.py
        news_tags.py
```

**news_tags.py** faylini yaratamiz:

```python
# news_app/templatetags/news_tags.py

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

**Template'da ishlatamiz:**

```html
<!-- templates/news/news_list.html -->

{% extends 'base.html' %}
{% load static %}
{% load news_tags %}  <!-- O'zimizning filterimizni yuklaymiz -->

{% block content %}
<div class="container">
    <div class="row">
        {% for news in news_list %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100">
                <!-- Rasm va boshqa kod... -->
                
                <div class="card-footer text-muted">
                    <div class="d-flex justify-content-between align-items-center">
                        <small>
                            <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
                        </small>
                        <small>
                            <i class="fas fa-eye"></i> {{ news.views_count|compact_number }}
                        </small>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

**Natija:**
- 500 → 500
- 1250 → 1.3K
- 15000 → 15.0K
- 1500000 → 1.5M

### 6-bosqich: Ko'rishlar soniga rang berish

Ko'rishlar soni bo'yicha ranglar qo'shamiz - mashhur yangiliklarni ajratib ko'rsatish uchun.

**CSS yozamiz (style.css):**

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

**Custom template tag yaratamiz:**

```python
# news_app/templatetags/news_tags.py

from django import template

register = template.Library()

@register.filter
def views_class(count):
    """
    Ko'rishlar soniga qarab CSS class qaytaradi
    """
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

**Template'da ishlatamiz:**

```html
<!-- templates/news/news_list.html -->

{% load news_tags %}

<div class="card-footer text-muted">
    <div class="d-flex justify-content-between align-items-center">
        <small>
            <i class="fas fa-calendar"></i> {{ news.publish_time|date:"d-M, Y" }}
        </small>
        <small class="views-count {{ news.views_count|views_class }}">
            <i class="fas fa-eye"></i> {{ news.views_count|compact_number }}
        </small>
    </div>
</div>
```

### 7-bosqich: Natijani tekshirish

Serverni ishga tushiramiz:

```bash
python manage.py runserver
```

Brauzerda tekshiramiz:
- http://127.0.0.1:8000/ - Bosh sahifada ko'rishlar ko'rinishi kerak
- Biror yangilikning sahifasini bir necha marta yangilaymiz
- Ko'rishlar soni oshib borishini kuzatamiz

## To'liq kod misoli

### news_app/views.py

```python
from django.views.generic import DetailView, ListView
from django.db.models import F
from .models import News

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Ko'rishlar sonini oshirish
        obj.views_count = F('views_count') + 1
        obj.save(update_fields=['views_count'])
        obj.refresh_from_db()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Eng ko'p ko'rilgan yangiliklarni qo'shamiz
        context['most_viewed'] = News.published.order_by('-views_count')[:5]
        return context


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        return News.published.all()
```

### news_app/templatetags/news_tags.py

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

## Xulosa

Ushbu darsda biz:
- Ko'rishlar sonini yangilik detail sahifasida ko'rsatdik
- Yangiliklar ro'yxatida ko'rishlar sonini qo'shdik
- Humanize filteri yordamida raqamlarni chiroyli formatlash
- Eng ko'p ko'rilgan yangiliklarni sidebar'da ko'rsatdik
- Custom template filterlar yaratdik
- Ko'rishlar soniga qarab ranglarni qo'shdik

## Keyingi dars

Keyingi darsda izohlar sonini template'dan chiqarishni va loyihani GitHub'ga saqlashni o'rganamiz.

## Maslahatlar va Best Practices

### 1. Raqamlarni formatlash

Har doim foydalanuvchiga tushunarli formatda raqamlarni ko'rsating:
- Kichik raqamlar uchun: oddiy format (123)
- O'rta raqamlar uchun: vergul bilan (1,234)
- Katta raqamlar uchun: qisqartirilgan format (1.5K, 2.3M)

### 2. Ikonkalar

Ko'rishlar sonini ko'rsatishda doim ko'z ikonkasini ishlating - bu universal belgi va foydalanuvchilar uchun tushunarli.

### 3. Performance

Ko'p miqdordagi yangiliklarni ko'rsatishda:
- `select_related()` va `prefetch_related()` dan foydalaning
- Kerakli maydonlarni `only()` bilan cheklang
- Keshdan foydalaning

### 4. A/B Testing

Turli ko'rinishlarni sinab ko'ring:
- Ko'rishlar sonini turli joylarda joylashtiring
- Ranglar va ikonkalarni o'zgartiring
- Foydalanuvchilarning qaysi variantni ko'proq yoqtirganini tekshiring

### 5. Privacy

Ba'zi loyihalarda ko'rishlar sonini:
- Faqat admin'ga ko'rsating
- Yoki umumiy statistika sifatida ko'rsating (aniq raqam emas)
- Yoki faqat ma'lum darajadan yuqori bo'lganda ko'rsating

### 6. Caching

Ko'p kirib-chiquvchi saytlarda:
```python
from django.core.cache import cache

def get_most_viewed_news():
    cache_key = 'most_viewed_news'
    news = cache.get(cache_key)
    
    if not news:
        news = News.published.order_by('-views_count')[:5]
        cache.set(cache_key, news, 3600)  # 1 soat
    
    return news
```

### 7. Real-time ko'rsatish

Agar real-time ko'rishlar sonini ko'rsatmoqchi bo'lsangiz:
- Django Channels ishlatish
- WebSocket orqali yangilanishlar yuborish
- JavaScript bilan sahifa yangilanmasdan ko'rishlar sonini o'zgartirish

### 8. SEO uchun

Ko'rishlar soni SEO uchun ham foydali:
```html
<meta property="article:views" content="{{ news.views_count }}">
```

### 9. Analytics

Ko'rishlar sonini Google Analytics bilan birlashtiring:
```javascript
gtag('event', 'page_view', {
  'article_id': '{{ news.id }}',
  'article_title': '{{ news.title }}',
  'views_count': {{ news.views_count }}
});
```

### 10. Testing

Ko'rishlar sonini test qiling:
```python
from django.test import TestCase
from .models import News

class ViewsCountTest(TestCase):
    def test_views_count_increases(self):
        news = News.objects.create(title="Test", views_count=0)
        response = self.client.get(news.get_absolute_url())
        news.refresh_from_db()
        self.assertEqual(news.views_count, 1)
```

## Xulosa va keyingi qadamlar

Ushbu darsda biz ko'rishlar sonini template'da professional darajada aks ettirishni o'rgandik. Biz:

✅ Humanize ilovasidan foydalanib raqamlarni chiroyli formatladik
✅ Custom template filterlar yaratdik
✅ Ko'rishlar soniga dinamik ranglar qo'shdik
✅ Eng ko'p ko'rilgan yangiliklarni sidebar'da ko'rsatdik
✅ Performance va best practice'larni o'rgandik

Keyingi darsda izohlar sonini template'dan chiqarishni va loyihani GitHub'ga saqlashni o'rganamiz.

---

**Eslatma:** Ushbu darsda o'rgangan bilimlaringizni amaliyotda qo'llang va o'z loyihangizda sinab ko'ring!