# Django i18n va Google Translator - Amaliyot

## Maqsad

Ushbu amaliyotda biz **Yangiliklar sayti** loyihasini 3 tilga (O'zbekcha, Ruscha, Inglizcha) tarjima qilamiz. Google Translate API yordamida avtomatik tarjima funksiyasini qo'shamiz.

## Amaliyot qismlari

1. Loyihani tayyorlash
2. i18n tizimini sozlash
3. Google Translate o'rnatish
4. Tarjima funksiyalarini yozish
5. Til tanlovchini qo'shish
6. Natijani tekshirish

---

## 1-qism: Loyihani tayyorlash

### 1.1. Virtual muhitni aktivlashtirish

```bash
# Loyiha papkasiga o'ting
cd yangiliklar_sayti

# Virtual muhitni aktivlashtiring
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 1.2. Hozirgi holatni tekshirish

```bash
python manage.py runserver
```

Brauzerda `http://127.0.0.1:8000` ochib, saytning ishlashini tekshiring.

---

## 2-qism: i18n tizimini sozlash

### 2.1. settings.py faylini o'zgartirish

`config/settings.py` faylini oching va quyidagi o'zgarishlarni kiriting:

```python
# config/settings.py

from django.utils.translation import gettext_lazy as _

# MIDDLEWARE ro'yxatiga LocaleMiddleware qo'shing
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ⬅️ Bu qatorni qo'shing
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Tillar sozlamalari
LANGUAGES = [
    ('uz', _('O\'zbekcha')),
    ('ru', _('Русский')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'uz'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
```

**Natija:** i18n tizimi yoqildi va 3 ta til qo'llab-quvvatlanadi.

### 2.2. URL konfiguratsiyasini o'zgartirish

`config/urls.py` faylini oching:

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

# Admin paneli til prefiksiz
urlpatterns = [
    path('admin/', admin.site.urls),
]

# Til prefiksli URL'lar
urlpatterns += i18n_patterns(
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('pages/', include('pages.urls')),
)

# Til o'zgartirish URL'i
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Natija:** URL'lar endi til prefiksli bo'ladi (`/uz/`, `/ru/`, `/en/`)

### 2.3. Locale papkasini yaratish

Terminal'da quyidagi buyruqni bajaring:

```bash
# Loyiha ildiz papkasida
mkdir locale
```

**Natija:** Tarjima fayllari uchun papka yaratildi.

---

## 3-qism: Google Translate o'rnatish

### 3.1. Googletrans kutubxonasini o'rnatish

```bash
pip install googletrans==4.0.0-rc1
```

**Eslatma:** Agar xato chiqsa, boshqa versiyani sinab ko'ring:

```bash
pip install googletrans==3.1.0a0
```

### 3.2. requirements.txt yangilash

```bash
pip freeze > requirements.txt
```

**Tekshirish:**

```bash
python manage.py shell
```

Python shell'da:

```python
from googletrans import Translator
translator = Translator()
result = translator.translate('Salom dunyo', dest='ru')
print(result.text)  # "Привет мир" chiqishi kerak
exit()
```

**Natija:** Google Translate ishlayapti! ✅

---

## 4-qism: Tarjima funksiyalarini yozish

### 4.1. utils.py faylini yaratish

`news/utils.py` fayl yarating:

```python
# news/utils.py

from googletrans import Translator
from django.core.cache import cache

def translate_text(text, dest_language='en', src_language='auto'):
    """
    Matnni tarjima qilish (kesh bilan)
    
    Args:
        text (str): Tarjima qilinadigan matn
        dest_language (str): Maqsad til ('ru', 'en')
        src_language (str): Manba til (default: 'auto')
    
    Returns:
        str: Tarjima qilingan matn
    """
    # Bo'sh matnni tekshirish
    if not text or not text.strip():
        return text
    
    # Kesh kaliti
    cache_key = f"trans_{dest_language}_{hash(text)}"
    
    # Keshdan tekshirish
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Tarjima qilish
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest_language, src=src_language)
        translated = result.text
        
        # Keshga saqlash (1 soat)
        cache.set(cache_key, translated, timeout=3600)
        
        return translated
    except Exception as e:
        print(f"Tarjima xatosi: {e}")
        return text  # Xato bo'lsa asl matnni qaytarish


def translate_queryset_fields(queryset, fields, dest_language):
    """
    QuerySet obyektlaridagi maydonlarni tarjima qilish
    
    Args:
        queryset: Django QuerySet
        fields (list): Tarjima qilinadigan maydonlar ['title', 'body']
        dest_language (str): Maqsad til
    
    Returns:
        queryset: Tarjima qilingan QuerySet
    """
    for obj in queryset:
        for field in fields:
            original_text = getattr(obj, field, None)
            if original_text:
                translated = translate_text(original_text, dest_language)
                setattr(obj, field, translated)
    
    return queryset
```

**Natija:** Tarjima funksiyalari tayyor.

### 4.2. settings.py'da keshni sozlash

`config/settings.py` fayliga qo'shing:

```python
# config/settings.py

# Kesh sozlamalari
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'translation-cache',
        'TIMEOUT': 3600,  # 1 soat
    }
}
```

**Natija:** Kesh yoqildi, tarjima tezroq ishlaydi.

---

## 5-qism: Views'da tarjima qilish

### 5.1. news/views.py faylini yangilash

`news/views.py` faylini oching va quyidagicha o'zgartiring:

```python
# news/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from .models import News, Category
from .utils import translate_text, translate_queryset_fields

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = News.published.all()
        current_lang = get_language()
        
        # O'zbekchadan boshqa tillar uchun tarjima
        if current_lang != 'uz':
            queryset = list(queryset)  # QuerySet'ni list'ga aylantirish
            queryset = translate_queryset_fields(
                queryset,
                fields=['title', 'body'],
                dest_language=current_lang
            )
        
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self):
        obj = super().get_object()
        current_lang = get_language()
        
        # Tarjima qilish
        if current_lang != 'uz':
            obj.title = translate_text(obj.title, dest_language=current_lang)
            obj.body = translate_text(obj.body, dest_language=current_lang)
            
            # Kategoriyani ham tarjima qilish
            if obj.category:
                obj.category.name = translate_text(
                    obj.category.name, 
                    dest_language=current_lang
                )
        
        return obj


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        queryset = News.published.all()[:5]  # Oxirgi 5 ta yangilik
        current_lang = get_language()
        
        if current_lang != 'uz':
            queryset = list(queryset)
            queryset = translate_queryset_fields(
                queryset,
                fields=['title'],
                dest_language=current_lang
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lang = get_language()
        
        # Kategoriyalarni ham tarjima qilish
        categories = Category.objects.all()
        if current_lang != 'uz':
            categories = list(categories)
            categories = translate_queryset_fields(
                categories,
                fields=['name'],
                dest_language=current_lang
            )
        
        context['categories'] = categories
        return context
```

**Natija:** Barcha view'lar avtomatik tarjima qiladi.

---

## 6-qism: Template'ga til tanlovchini qo'shish

### 6.1. base.html faylini yangilash

`templates/base.html` faylini oching:

```html
<!-- templates/base.html -->

{% load i18n %}
{% load static %}

<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <style>
        /* Til tanlovchi stillari */
        .language-selector {
            position: relative;
            display: inline-block;
        }
        
        .language-select {
            padding: 8px 30px 8px 12px;
            border: 2px solid #007bff;
            border-radius: 6px;
            background-color: white;
            color: #333;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23007bff' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 10px center;
        }
        
        .language-select:hover {
            border-color: #0056b3;
            background-color: #f8f9fa;
        }
        
        .language-select:focus {
            outline: none;
            border-color: #0056b3;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
        }
        
        /* Navbar stillari */
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .navbar-brand a {
            color: white;
            text-decoration: none;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .navbar-menu {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .navbar-menu a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        
        .navbar-menu a:hover {
            background: rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-brand">
                <a href="{% url 'news:home' %}">📰 Yangiliklar</a>
            </div>
            
            <div class="navbar-menu">
                <a href="{% url 'news:home' %}">Bosh sahifa</a>
                <a href="{% url 'news:news_list' %}">Yangiliklar</a>
                
                {% if user.is_authenticated %}
                    <a href="{% url 'accounts:profile' %}">Profil</a>
                    <a href="{% url 'accounts:logout' %}">Chiqish</a>
                {% else %}
                    <a href="{% url 'accounts:login' %}">Kirish</a>
                {% endif %}
                
                <!-- Til tanlovchi -->
                <div class="language-selector">
                    <form action="{% url 'set_language' %}" method="post">
                        {% csrf_token %}
                        <input name="next" type="hidden" value="{{ request.path }}">
                        <select name="language" onchange="this.form.submit()" class="language-select">
                            {% get_current_language as CURRENT_LANGUAGE %}
                            {% get_available_languages as AVAILABLE_LANGUAGES %}
                            {% for lang_code, lang_name in AVAILABLE_LANGUAGES %}
                                <option value="{{ lang_code }}" 
                                    {% if lang_code == CURRENT_LANGUAGE %}selected{% endif %}>
                                    {{ lang_name }}
                                </option>
                            {% endfor %}
                        </select>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <main class="container" style="max-width: 1200px; margin: 20px auto; padding: 0 20px;">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}" style="padding: 15px; margin-bottom: 20px; border-radius: 4px; background: #d4edda; border: 1px solid #c3e6cb;">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}
        {% endblock %}
    </main>

    <footer style="background: #333; color: white; text-align: center; padding: 20px; margin-top: 40px;">
        <p>&copy; 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
    </footer>
</body>
</html>
```

**Natija:** Til tanlovchi navbar'da paydo bo'ldi! 🎉

### 6.2. news_list.html faylini tekshirish

`templates/news/news_list.html`:

```html
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Barcha yangiliklar" %}{% endblock %}

{% block content %}
<h1>{% trans "Barcha yangiliklar" %}</h1>

<div class="news-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
    {% for news in news_list %}
    <div class="news-card" style="border: 1px solid #ddd; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        {% if news.photo %}
            <img src="{{ news.photo.url }}" alt="{{ news.title }}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 4px;">
        {% endif %}
        
        <h3><a href="{% url 'news:news_detail' news.slug %}" style="color: #333; text-decoration: none;">{{ news.title }}</a></h3>
        
        <p style="color: #666; font-size: 14px;">
            {{ news.body|truncatewords:20 }}
        </p>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; font-size: 12px; color: #999;">
            <span>📅 {{ news.publish_time|date:"d.m.Y" }}</span>
            <span>👁 {{ news.views }} {% trans "ko'rishlar" %}</span>
        </div>
    </div>
    {% empty %}
    <p>{% trans "Yangiliklar topilmadi" %}</p>
    {% endfor %}
</div>

<!-- Pagination -->
{% if is_paginated %}
<div class="pagination" style="text-align: center; margin-top: 30px;">
    {% if page_obj.has_previous %}
        <a href="?page=1">&laquo; {% trans "Birinchi" %}</a>
        <a href="?page={{ page_obj.previous_page_number }}">{% trans "Oldingi" %}</a>
    {% endif %}
    
    <span style="margin: 0 10px;">
        {% trans "Sahifa" %} {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
    </span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">{% trans "Keyingi" %}</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">{% trans "Oxirgi" %} &raquo;</a>
    {% endif %}
</div>
{% endif %}

{% endblock %}
```

**Natija:** Template'da `{% trans %}` teglari qo'shildi.

---

## 7-qism: Tarjima fayllarini yaratish

### 7.1. Tarjima fayllarini generatsiya qilish

Terminal'da:

```bash
# Ruscha uchun
django-admin makemessages -l ru

# Inglizcha uchun
django-admin makemessages -l en
```

**Natija:** `locale/ru/LC_MESSAGES/django.po` va `locale/en/LC_MESSAGES/django.po` fayllari yaratildi.

### 7.2. Tarjima fayllarini to'ldirish

`locale/ru/LC_MESSAGES/django.po` faylini oching:

```po
msgid "Barcha yangiliklar"
msgstr "Все новости"

msgid "ko'rishlar"
msgstr "просмотров"

msgid "Yangiliklar topilmadi"
msgstr "Новости не найдены"

msgid "Birinchi"
msgstr "Первая"

msgid "Oldingi"
msgstr "Предыдущая"

msgid "Sahifa"
msgstr "Страница"

msgid "Keyingi"
msgstr "Следующая"

msgid "Oxirgi"
msgstr "Последняя"
```

`locale/en/LC_MESSAGES/django.po`:

```po
msgid "Barcha yangiliklar"
msgstr "All News"

msgid "ko'rishlar"
msgstr "views"

msgid "Yangiliklar topilmadi"
msgstr "No news found"

msgid "Birinchi"
msgstr "First"

msgid "Oldingi"
msgstr "Previous"

msgid "Sahifa"
msgstr "Page"

msgid "Keyingi"
msgstr "Next"

msgid "Oxirgi"
msgstr "Last"
```

### 7.3. Tarjimalarni kompilyatsiya qilish

```bash
django-admin compilemessages
```

**Natija:** `.po` fayllar `.mo` fayllariga aylantirildi.

---

## 8-qism: Natijani tekshirish

### 8.1. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 8.2. Brauzerda tekshirish

**Test 1: O'zbekcha versiya**
- URL: `http://127.0.0.1:8000/uz/`
- Natija: Barcha kontentlar o'zbekcha

**Test 2: Ruscha versiya**
- Navbar'dan "Русский" tanlang
- URL avtomatik: `http://127.0.0.1:8000/ru/` bo'ladi
- Natija: Yangiliklar ruscha tarjima qilinadi (Google Translate orqali)

**Test 3: Inglizcha versiya**
- Navbar'dan "English" tanlang
- URL: `http://127.0.0.1:8000/en/`
- Natija: Yangiliklar inglizcha tarjima qilinadi

### 8.3. Tarjima tezligini tekshirish

1. **Birinchi marta:** Tarjima sekinroq (API chaqiruv)
2. **Ikkinchi marta:** Tezroq (keshdan olinadi)

Browser Developer Tools'da Network tab'ini ochib, so'rovlar tezligini kuzating.

---

## 9-qism: Qo'shimcha optimizatsiya

### 9.1. Loading indikatori qo'shish

Tarjima qilinayotganda loading ko'rsatish uchun:

```html
<!-- base.html ga qo'shing -->
<style>
.loading-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 9999;
    justify-content: center;
    align-items: center;
}

.loading-spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<div class="loading-overlay" id="loadingOverlay">
    <div class="loading-spinner"></div>
</div>

<script>
    // Til o'zgarganda loading ko'rsatish
    document.querySelector('.language-select').addEventListener('change', function() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    });
</script>
```

### 9.2. Tarjima xatolarini boshqarish

`news/utils.py` ga qo'shimcha:

```python
import logging

logger = logging.getLogger(__name__)

def translate_text(text, dest_language='en', src_language='auto'):
    # ... oldingi kod ...
    
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest_language, src=src_language)
        translated = result.text
        
        cache.set(cache_key, translated, timeout=3600)
        logger.info(f"Tarjima muvaffaqiyatli: {dest_language}")
        
        return translated
    except Exception as e:
        logger.error(f"Tarjima xatosi: {e}")
        return text
```

---

## 10-qism: Yakuniy tekshirish

### Tekshirish ro'yxati

- [ ] `settings.py` to'g'ri sozlangan
- [ ] `urls.py` da i18n_patterns qo'shilgan
- [ ] `googletrans` o'rnatilgan
- [ ] `utils.py` tarjima funksiyalari ishlayapti
- [ ] `views.py` da tarjima qo'shilgan
- [ ] Navbar'da til tanlovchi bor
- [ ] O'zbekcha versiya ishlayapti
- [ ] Ruscha avtomatik tarjima ishlayapti
- [ ] Inglizcha avtomatik tarjima ishlayapti
- [ ] URL'lar to'g'ri (`/uz/`, `/ru/`, `/en/`)
- [ ] Kesh ishlayapti

### Xatolarni tuzatish

**Xato 1:** `googletrans` xatosi
```bash
pip uninstall googletrans
pip install googletrans==4.0.0-rc1
```

**Xato 2:** Tarjima juda sekin
- Kesh sozlamalarini tekshiring
- Faqat kerakli maydonlarni tarjima qiling

**Xato 3:** URL'lar ishlamayapti
- `{% url %}` tegidan foydalaning
- Hard-coded URL'larni o'zgartiring

---

## Yakuniy natija

Tabriklaymiz! 🎉 Siz muvaffaqiyatli:

1. ✅ Django i18n tizimini sozladingiz
2. ✅ 3 ta til qo'llab-quvvatlash qo'shdingiz
3. ✅ Google Translate API bilan ishladingiz
4. ✅ Avtomatik tarjima funksiyasini yaratdingiz
5. ✅ Til tanlovchini qo'shdingiz
6. ✅ Kesh orqali tezlikni oshirdingiz

Keyingi darsda biz **ModelTranslation** bilan database'dagi kontentni tarjima qilishni o'rganamiz.

## Qo'shimcha topshiriqlar

1. **Kategoriyalarni tarjima qiling**
2. **Izohlarni tarjima qiling**
3. **Profil sahifasini tarjima qiling**
4. **404 va 500 sahifalarini tarjima qiling**
5. **Email xabarlarini tarjima qiling**

