# Veb-saytni i18n va GoogleTranslator orqali tarjima qilish

## Kirish

Zamonaviy veb-saytlar ko'p tillarda ishlashi kerak. Django'da **i18n (internationalization)** va **l10n (localization)** yordamida saytimizni bir necha tilga tarjima qilishimiz mumkin. Bu darsda biz Google Translator API dan foydalanib, veb-saytimizni avtomatik ravishda tarjima qilishni o'rganamiz.

**i18n** - Internationalization (xalqarolashtirish) - dasturni turli tillarda ishlashga tayyor holga keltirish.
**l10n** - Localization (mahalliylashtirish) - dasturni ma'lum bir til va mintaqaga moslashtirish.

## Maqsad

Ushbu darsda quyidagilarni o'rganamiz:
- Django'da i18n tizimini yoqish va sozlash
- Tillarni tanlash imkoniyatini qo'shish
- Google Translate API bilan ishlash
- Sayt kontentini avtomatik tarjima qilish
- Til tanlash tugmasini qo'shish

## 1-bosqich: Django i18n tizimini yoqish

### settings.py faylini sozlash

Birinchi navbatda, `config/settings.py` fayliga kerakli sozlamalarni qo'shamiz:

```python
# config/settings.py

from django.utils.translation import gettext_lazy as _

# Middleware'larga LocaleMiddleware qo'shish
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Yangi qo'shildi
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Tillar ro'yxati
LANGUAGES = [
    ('uz', _('O\'zbekcha')),
    ('ru', _('Русский')),
    ('en', _('English')),
]

# Asosiy til
LANGUAGE_CODE = 'uz'

# Tarjimalar saqlanadigan papka
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Vaqt zonasi
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Tashkent'
```

**Tushuntirish:**
- `LocaleMiddleware` - foydalanuvchining til tanlashini boshqaradi
- `LANGUAGES` - saytda qo'llab-quvvatlanadigan tillar ro'yxati
- `LANGUAGE_CODE` - standart til (sayt birinchi marta ochilganda)
- `LOCALE_PATHS` - tarjima fayllari saqlanadigan papka
- `USE_I18N = True` - xalqarolashtirish tizimini yoqadi

## 2-bosqich: URL konfiguratsiyasi

### config/urls.py faylini yangilash

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

# i18n patterns - til prefiksli URL'lar
urlpatterns += i18n_patterns(
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('pages/', include('pages.urls')),
)

# Til o'zgartirish uchun URL
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Tushuntirish:**
- `i18n_patterns` - URL'larga til prefiksini qo'shadi (masalan: `/uz/`, `/ru/`, `/en/`)
- `django.conf.urls.i18n` - til o'zgartirish uchun maxsus URL
- Admin panel til prefixsiz qoladi

## 3-bosqich: Google Translate kutubxonasini o'rnatish

### Googletrans kutubxonasini o'rnatish

Terminal orqali quyidagi buyruqni bajaring:

```bash
pip install googletrans==4.0.0-rc1
```

**Eslatma:** `googletrans==4.0.0-rc1` versiyasini ishlating, chunki yangi versiyalarda ba'zi muammolar mavjud.

Agar muammo bo'lsa, alternativ versiyani sinab ko'ring:

```bash
pip install googletrans==3.1.0a0
```

### requirements.txt faylini yangilash

```bash
pip freeze > requirements.txt
```

## 4-bosqich: Tarjima funksiyasini yaratish

### utils.py faylini yaratish

Loyihangizda yangi `utils.py` fayl yarating (masalan: `news/utils.py`):

```python
# news/utils.py

from googletrans import Translator

def translate_text(text, dest_language='en', src_language='auto'):
    """
    Google Translate API orqali matnni tarjima qilish
    
    Args:
        text (str): Tarjima qilinadigan matn
        dest_language (str): Maqsadli til kodi (default: 'en')
        src_language (str): Manba til kodi (default: 'auto' - avtomatik aniqlash)
    
    Returns:
        str: Tarjima qilingan matn
    """
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest_language, src=src_language)
        return translation.text
    except Exception as e:
        print(f"Tarjima xatosi: {e}")
        return text  # Xato bo'lsa, asl matnni qaytaradi


def translate_queryset(queryset, fields, dest_language='en'):
    """
    QuerySet obyektlaridagi maydonlarni tarjima qilish
    
    Args:
        queryset: Django QuerySet obyekti
        fields (list): Tarjima qilinadigan maydonlar ro'yxati
        dest_language (str): Maqsadli til kodi
    
    Returns:
        queryset: Tarjima qilingan QuerySet
    """
    translator = Translator()
    
    for obj in queryset:
        for field in fields:
            original_text = getattr(obj, field)
            if original_text:
                try:
                    translated = translator.translate(
                        original_text, 
                        dest=dest_language, 
                        src='auto'
                    )
                    setattr(obj, field, translated.text)
                except Exception as e:
                    print(f"Tarjima xatosi ({field}): {e}")
    
    return queryset
```

**Tushuntirish:**
- `translate_text()` - oddiy matnni tarjima qiladi
- `translate_queryset()` - database'dan olingan obyektlarni tarjima qiladi
- `try-except` bloki xatolarni ushlaydi va saytning ishdan chiqmasligi uchun asl matnni qaytaradi

## 5-bosqich: Views'da tarjima qilish

### news/views.py faylini yangilash

```python
# news/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from .models import News
from .utils import translate_text, translate_queryset

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = News.published.all()
        current_language = get_language()  # Joriy tilni aniqlash
        
        # Agar til o'zbek bo'lmasa, tarjima qilish
        if current_language != 'uz':
            queryset = translate_queryset(
                queryset, 
                fields=['title', 'body'],
                dest_language=current_language
            )
        
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_language = get_language()
        
        # Yangilikni tarjima qilish
        if current_language != 'uz':
            news = context['news']
            news.title = translate_text(news.title, dest_language=current_language)
            news.body = translate_text(news.body, dest_language=current_language)
            context['news'] = news
        
        return context
```

**Tushuntirish:**
- `get_language()` - foydalanuvchining tanlagan tilini qaytaradi
- Agar til o'zbekcha bo'lmasa, kontentni avtomatik tarjima qilamiz
- `NewsListView` - ro'yxatdagi barcha yangiliklarni tarjima qiladi
- `NewsDetailView` - faqat ko'rilayotgan yangilikni tarjima qiladi

## 6-bosqich: Template'da til tanlovchini qo'shish

### base.html'ga til tanlovchini qo'shish

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
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-brand">
                <a href="{% url 'news:home' %}">Yangiliklar</a>
            </div>
            
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
    </nav>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Yangiliklar sayti</p>
    </footer>
</body>
</html>
```

**Tushuntirish:**
- `{% load i18n %}` - i18n teglarini yuklaydi
- `{% url 'set_language' %}` - til o'zgartirish URL'i
- `{% get_current_language %}` - joriy tilni oladi
- `{% get_available_languages %}` - mavjud tillar ro'yxatini oladi
- `onchange="this.form.submit()"` - til tanlanishi bilanoq forma yuboriladi

### CSS stillarini qo'shish

```css
/* static/css/style.css */

.navbar {
    background-color: #333;
    padding: 1rem 0;
    color: white;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand a {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

.language-selector {
    display: flex;
    align-items: center;
}

.language-select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ddd;
    background-color: white;
    cursor: pointer;
    font-size: 1rem;
}

.language-select:hover {
    border-color: #007bff;
}

.language-select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}
```

## 7-bosqich: Til prefikslarini URL'larda boshqarish

### Template'larda URL'larni to'g'ri yozish

Til prefixli URL'lar bilan ishlashda `{% url %}` tegidan foydalaning:

```html
<!-- Noto'g'ri -->
<a href="/news/">Yangiliklar</a>

<!-- To'g'ri -->
<a href="{% url 'news:home' %}">Yangiliklar</a>
```

Django avtomatik ravishda til prefiksini qo'shadi:
- O'zbekcha: `/uz/news/`
- Ruscha: `/ru/news/`
- Inglizcha: `/en/news/`

## 8-bosqich: Locale papkasini yaratish

### Locale papkasini yaratish

Loyiha ildiz papkasida `locale` papkasini yarating:

```bash
mkdir locale
```

### Tarjima fayllarini yaratish

```bash
django-admin makemessages -l ru
django-admin makemessages -l en
```

Bu buyruqlar `locale/ru/LC_MESSAGES/django.po` va `locale/en/LC_MESSAGES/django.po` fayllarini yaratadi.

### Tarjima fayllarini kompilyatsiya qilish

```bash
django-admin compilemessages
```

Bu buyruq `.po` fayllarini `.mo` fayllariga aylantiradi (binary format).

## 9-bosqich: Statik matnlarni tarjima qilish

### Template'da statik matnlarni belgilash

```html
{% load i18n %}

<h1>{% trans "Yangiliklar" %}</h1>
<p>{% trans "Barcha yangiliklarni bu yerda topishingiz mumkin" %}</p>

<!-- Ko'p qatorli matnlar uchun -->
{% blocktrans %}
    Bu saytda siz eng so'nggi yangiliklarni o'qishingiz mumkin.
    Yangiliklar har kuni yangilanadi.
{% endblocktrans %}
```

**Tushuntirish:**
- `{% trans %}` - qisqa matnlarni tarjima qilish uchun
- `{% blocktrans %}` - uzun matnlarni tarjima qilish uchun

### Tarjima fayllarida matnlarni to'ldirish

`locale/ru/LC_MESSAGES/django.po` fayli:

```
msgid "Yangiliklar"
msgstr "Новости"

msgid "Barcha yangiliklarni bu yerda topishingiz mumkin"
msgstr "Здесь вы можете найти все новости"
```

## 10-bosqich: Keshni sozlash (Performance uchun)

Google Translate API'ni har safar chaqirish sekin ishlaydi. Keshdan foydalanib, tezlikni oshiramiz:

### settings.py'da keshni yoqish

```python
# config/settings.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 3600,  # 1 soat
    }
}
```

### utils.py'da keshdan foydalanish

```python
# news/utils.py

from django.core.cache import cache
from googletrans import Translator

def translate_text(text, dest_language='en', src_language='auto'):
    """
    Kesh bilan tarjima qilish
    """
    # Kesh kalitini yaratish
    cache_key = f"translation_{dest_language}_{hash(text)}"
    
    # Keshdan tekshirish
    cached_translation = cache.get(cache_key)
    if cached_translation:
        return cached_translation
    
    # Keshda yo'q bo'lsa, tarjima qilish
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest_language, src=src_language)
        translated_text = translation.text
        
        # Keshga saqlash
        cache.set(cache_key, translated_text, timeout=3600)
        
        return translated_text
    except Exception as e:
        print(f"Tarjima xatosi: {e}")
        return text
```

**Tushuntirish:**
- Birinchi marta tarjima qilingan matn keshga saqlanadi
- Keyingi safar shu matn uchun keshdan olinadi
- Bu API chaqiruvlarini kamaytirib, tezlikni oshiradi

## 11-bosqich: Middleware orqali avtomatik tarjima

Agar barcha view'larda tarjima kodini yozishni istmasangiz, maxsus middleware yaratishingiz mumkin:

### middleware.py faylini yaratish

```python
# news/middleware.py

from django.utils.translation import get_language
from django.utils.deprecation import MiddlewareMixin
from .utils import translate_text

class AutoTranslationMiddleware(MiddlewareMixin):
    """
    Avtomatik tarjima middleware'i
    """
    def process_template_response(self, request, response):
        current_language = get_language()
        
        # Faqat o'zbekchadan boshqa tillarda ishlaydi
        if current_language != 'uz' and hasattr(response, 'context_data'):
            context = response.context_data
            
            # Context'dagi ma'lumotlarni tarjima qilish
            if 'news_list' in context:
                for news in context['news_list']:
                    news.title = translate_text(news.title, dest_language=current_language)
                    news.body = translate_text(news.body, dest_language=current_language)
            
            if 'news' in context:
                news = context['news']
                news.title = translate_text(news.title, dest_language=current_language)
                news.body = translate_text(news.body, dest_language=current_language)
        
        return response
```

### settings.py'ga middleware qo'shish

```python
# config/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'news.middleware.AutoTranslationMiddleware',  # Yangi qo'shildi
]
```

## 12-bosqich: Tekshirish

### Server ishga tushirish

```bash
python manage.py runserver
```

### Brauzerda tekshirish

1. `http://127.0.0.1:8000/uz/` - O'zbekcha versiya
2. `http://127.0.0.1:8000/ru/` - Ruscha versiya (avtomatik tarjima)
3. `http://127.0.0.1:8000/en/` - Inglizcha versiya (avtomatik tarjima)

Navbar'dagi til tanlovchidan ham tilni o'zgartirishingiz mumkin.

## Xatolar va yechimlar

### 1. Googletrans xatosi

**Xato:**
```
AttributeError: 'NoneType' object has no attribute 'group'
```

**Yechim:**
```bash
pip uninstall googletrans
pip install googletrans==4.0.0-rc1
```

### 2. Locale papka topilmadi

**Xato:**
```
Locale path doesn't exist
```

**Yechim:**
```bash
mkdir locale
django-admin makemessages -l ru
django-admin compilemessages
```

### 3. Tarjima sekin ishlayapti

**Yechim:** Yuqoridagi kesh sozlamalarini qo'llang.

### 4. URL'lar ishlamayapti

**Yechim:** Barcha URL'larni `{% url %}` tegi bilan yozing:
```html
<!-- Noto'g'ri -->
<a href="/news/1/">Yangilik</a>

<!-- To'g'ri -->
<a href="{% url 'news:detail' news.id %}">Yangilik</a>
```

## Best Practices (Eng yaxshi amaliyotlar)

### 1. Keshdan foydalaning
Tarjima qilingan matnlarni keshda saqlang, bu tezlikni oshiradi va API chaqiruvlarini kamaytiradi.

### 2. Faqat kerakli matnlarni tarjima qiling
Barcha kontentni emas, faqat foydalanuvchiga ko'rinadigan matnlarni tarjima qiling.

### 3. Database'da original tilni saqlang
Har doim original tilni (masalan, o'zbekcha) database'da saqlang va tarjimani runtime'da bajaring.

### 4. Error handling qo'shing
Tarjima xatolari yuzaga kelganda, asl matnni ko'rsating.

```python
try:
    translated = translate_text(text, dest_language)
except:
    translated = text  # Asl matn
```

### 5. Rate limiting
Google Translate API'da so'rovlar soni cheklangan. Ko'p so'rov yubormaslik uchun kesh va rate limiting qo'llang.

### 6. Professional tarjima uchun
Muhim loyihalar uchun Google Translate Cloud API'ni ishlating (pulli, lekin sifatliroq).

```bash
pip install google-cloud-translate
```

### 7. SEO uchun
Har bir til uchun alohida URL qo'llang:
- `/uz/yangiliklar/`
- `/ru/novosti/`
- `/en/news/`

### 8. Hreflang teglarini qo'shing

```html
<link rel="alternate" hreflang="uz" href="https://example.com/uz/" />
<link rel="alternate" hreflang="ru" href="https://example.com/ru/" />
<link rel="alternate" hreflang="en" href="https://example.com/en/" />
```

## Qo'shimcha imkoniyatlar

### 1. Til avtomatik aniqlash

Brauzer tilini avtomatik aniqlash:

```python
# news/middleware.py

from django.utils import translation
from django.conf import settings

class AutoDetectLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('language'):
            # Accept-Language header'dan tilni olish
            lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if lang.startswith('ru'):
                language = 'ru'
            elif lang.startswith('en'):
                language = 'en'
            else:
                language = 'uz'
            
            translation.activate(language)
            request.session['language'] = language
        
        response = self.get_response(request)
        return response
```

### 2. Til sessionda saqlash

```python
# views.py

from django.utils import translation

def set_language_view(request, language):
    translation.activate(language)
    request.session['django_language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))
```

### 3. Cookie'da til saqlash

```python
# views.py

from django.http import HttpResponse
from django.utils import translation

def set_language(request, language):
    translation.activate(language)
    response = HttpResponse()
    response.set_cookie('django_language', language, max_age=31536000)  # 1 yil
    return response
```

## Xulosa

Ushbu darsda biz Django'da i18n tizimi va Google Translator yordamida veb-saytni ko'p tilga tarjima qilishni o'rgandik. Asosiy qismlar:

1. ✅ Django i18n tizimini sozladik
2. ✅ Google Translate API'ni o'rnatdik
3. ✅ Avtomatik tarjima funksiyalarini yaratdik
4. ✅ Til tanlovchini qo'shdik
5. ✅ URL'larda til prefikslarini qo'lladik
6. ✅ Kesh orqali performanceni oshirdik
7. ✅ Middleware orqali avtomatlashtirishni o'rgandik

Keyingi darsda biz **ModelTranslation** modulidan foydalanib, database'dagi kontentni tarjima qilishni o'rganamiz.

## Topshiriq

1. O'z loyihangizda i18n tizimini sozlang
2. Kamida 2 ta til qo'shing (masalan: o'zbek va rus)
3. Til tanlovchini navbar'ga qo'shing
4. Bitta sahifani to'liq tarjima qiling
5. Kesh sozlamalarini qo'llang

Omad! 🚀
```