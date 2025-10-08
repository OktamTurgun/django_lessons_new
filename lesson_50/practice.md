# Lesson 50: Practice - ModelTranslation bilan amaliy mashq

## Maqsad

Ushbu amaliyotda biz `django-modeltranslation` kutubxonasini yangiliklar saytimizga to'liq integratsiya qilamiz va News hamda Category modellarini 3 tilda (O'zbekcha, Ruscha, Inglizcha) tarjima qilamiz.

---

## Bosqichma-bosqich amaliyot

### Bosqich 1: Loyihani tayyorlash

#### 1.1. Virtual muhitni ishga tushiring

```bash
# Terminal ochib, loyiha papkasiga o'ting
cd yangiliklar_sayti

# Virtual muhitni faollashtiring
# Windows uchun:
pipenv shell

# yoki
source venv/bin/activate  # Linux/Mac
```

#### 1.2. Hozirgi holatni tekshiring

```bash
# Server ishga tushiring
python manage.py runserver

# Browser'da http://127.0.0.1:8000 ni oching
# Sayt to'g'ri ishlayotganini tekshiring
```

---

### Bosqich 2: django-modeltranslation o'rnatish

#### 2.1. Kutubxonani o'rnatish

```bash
pip install django-modeltranslation
```

#### 2.2. Requirements.txt ni yangilash

```bash
pip freeze > requirements.txt
```

**Tekshirish:** `requirements.txt` faylida `django-modeltranslation` borligini ko'ring.

---

### Bosqich 3: Settings.py ni sozlash

#### 3.1. config/settings.py faylini oching

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # MUHIM: modeltranslation admin'dan oldin!
    'modeltranslation',
    
    # Local apps
    'news_app',
    'accounts_app',
]
```

**Eslatma:** `modeltranslation` ni aynan shu joyga qo'yish kerak - `django.contrib.admin` dan keyin, lekin sizning appalaringizdan oldin.

#### 3.2. Til sozlamalarini qo'shish

`settings.py` faylining oxiriga qo'shing:

```python
# Internationalization settings
LANGUAGE_CODE = 'uz'

LANGUAGES = (
    ('uz', "O'zbekcha"),
    ('ru', 'Русский'),
    ('en', 'English'),
)

# Modeltranslation sozlamalari
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')

# Fallback sozlamalari (agar tarjima bo'lmasa)
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'en')

# Locale papkasi (keyingi darslar uchun)
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

**Saqlang!**

---

### Bosqich 4: translation.py fayli yaratish

#### 4.1. news_app/translation.py faylini yarating

Yangi fayl yarating: `news_app/translation.py`

```python
from modeltranslation.translator import register, TranslationOptions
from .models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    """News modelini tarjima qilish uchun sozlamalar"""
    fields = ('title', 'body')  # Tarjima qilinadigan maydonlar


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Category modelini tarjima qilish uchun sozlamalar"""
    fields = ('name',)  # Kategoriya nomini tarjima qilamiz
```

**Tushuntirish:**

- `@register(News)` - News modelini tarjima uchun ro'yxatdan o'tkazadi
- `fields = ('title', 'body')` - faqat title va body maydonlari tarjima qilinadi
- Slug, sana, status kabi texnik maydonlar tarjima qilinmaydi

**Saqlang!**

---

### Bosqich 5: Migratsiya yaratish va qo'llash

#### 5.1. Migratsiya yaratish

```bash
python manage.py makemigrations
```

Siz quyidagicha xabar ko'rasiz:

```
Migrations for 'news_app':
  news_app/migrations/0002_alter_category_name_alter_news_body_and_more.py
    - Alter field name on category
    - Alter field body on news
    - Alter field title on news
```

#### 5.2. Migratsiyani qo'llash

```bash
python manage.py migrate
```

**Nima bo'ldi?**

Database'ga quyidagi yangi ustunlar qo'shildi:

**News modeli uchun:**
- `title_uz`, `title_ru`, `title_en`
- `body_uz`, `body_ru`, `body_en`

**Category modeli uchun:**
- `name_uz`, `name_ru`, `name_en`

---

### Bosqich 6: Mavjud ma'lumotlarni ko'chirish

Hozir sizda mavjud yangiliklar bor, lekin ular yangi tarjima maydonlarida yo'q. Ularni ko'chirish kerak.

#### 6.1. Management command yaratish

`news_app/management/commands/` papkalarini yarating (agar yo'q bo'lsa):

```bash
# Linux/Mac
mkdir -p news_app/management/commands

# Windows
mkdir news_app\management
mkdir news_app\management\commands
```

Har bir papkada `__init__.py` fayl yarating:

```bash
# Linux/Mac
touch news_app/management/__init__.py
touch news_app/management/commands/__init__.py

# Windows (yoki VS Code'da o'zingiz yarating)
```

#### 6.2. migrate_translations.py faylini yarating

`news_app/management/commands/migrate_translations.py`:

```python
from django.core.management.base import BaseCommand
from news_app.models import News, Category


class Command(BaseCommand):
    help = 'Mavjud ma\'lumotlarni tarjima maydonlariga ko\'chirish'

    def handle(self, *args, **kwargs):
        self.stdout.write('Tarjimalarni ko\'chirishni boshlaymiz...')
        
        # News modelini yangilash
        news_count = 0
        for news in News.objects.all():
            # Agar tarjima maydonlari bo'sh bo'lsa, asosiy maydondan ko'chirish
            if not news.title_uz:
                news.title_uz = news.title
            if not news.body_uz:
                news.body_uz = news.body
            
            # Rus va ingliz tillariga ham nusxa (keyinchalik o'zgartiriladi)
            if not news.title_ru:
                news.title_ru = news.title
            if not news.body_ru:
                news.body_ru = news.body
                
            if not news.title_en:
                news.title_en = news.title
            if not news.body_en:
                news.body_en = news.body
            
            news.save()
            news_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{news_count} ta yangilik tarjima maydonlariga ko\'chirildi')
        )
        
        # Category modelini yangilash
        category_count = 0
        for category in Category.objects.all():
            if not category.name_uz:
                category.name_uz = category.name
            if not category.name_ru:
                category.name_ru = category.name
            if not category.name_en:
                category.name_en = category.name
            
            category.save()
            category_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{category_count} ta kategoriya tarjima maydonlariga ko\'chirildi')
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Barcha ma\'lumotlar muvaffaqiyatli ko\'chirildi!'))
```

#### 6.3. Buyruqni ishga tushiring

```bash
python manage.py migrate_translations
```

Siz quyidagicha xabar ko'rasiz:

```
Tarjimalarni ko'chirishni boshlaymiz...
10 ta yangilik tarjima maydonlariga ko'chirildi
5 ta kategoriya tarjima maydonlariga ko'chirildi
✅ Barcha ma'lumotlar muvaffaqiyatli ko'chirildi!
```

---

### Bosqich 7: Admin panelni yangilash

#### 7.1. news_app/admin.py faylini yangilang

```python
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import News, Category


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'category', 'publish_time', 'status')
    list_filter = ('status', 'category', 'publish_time', 'created_time')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    
    # Tab'li interfeys uchun media fayllar
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
```

**Saqlang!**

---

### Bosqich 8: Admin panelda tarjimalarni to'ldirish

#### 8.1. Admin panelga kiring

```bash
# Server ishga tushiring (agar ishlamasa)
python manage.py runserver

# Browser'da oching
http://127.0.0.1:8000/admin
```

#### 8.2. News bo'limiga o'ting

1. Admin panelda **News** bo'limini oching
2. Biror yangilikni tahrirlash uchun bosing
3. Endi har bir maydon uchun 3 ta tab ko'rasiz:
   - **O'zbekcha** (Uzbek)
   - **Русский** (Russian)
   - **English**

#### 8.3. Tarjimalarni to'ldiring

Masalan, yangilik sarlavhasi:

**O'zbekcha tab:**
```
O'zbekistonda yangi texnologiyalar taqdim etildi
```

**Русский tab:**
```
В Узбекистане представлены новые технологии
```

**English tab:**
```
New technologies presented in Uzbekistan
```

**Body (matn) uchun ham xuddi shunday qiling.**

#### 8.4. Kategoriyalarni tarjima qiling

1. **Categories** bo'limiga o'ting
2. Har bir kategoriyani oching va tarjimalarini to'ldiring

Masalan, "Texnologiya" kategoriyasi:

- **O'zbekcha:** Texnologiya
- **Русский:** Технология
- **English:** Technology

**Kamida 2-3 ta yangilik va barcha kategoriyalarni tarjima qiling!**

---

### Bosqich 9: Template'larda tarjimalarni ko'rsatish

#### 9.1. news_list.html ni yangilang

`news_app/templates/news/news_list.html` faylini oching va tekshiring:

```html
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Barcha yangiliklar" %}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{% trans "Barcha yangiliklar" %}</h1>
    
    <div class="row">
        {% for news in news_list %}
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <!-- Avtomatik joriy tildagi sarlavha -->
                    <h5 class="card-title">{{ news.title }}</h5>
                    
                    <!-- Avtomatik joriy tildagi kategoriya -->
                    <p class="card-text">
                        <span class="badge bg-primary">{{ news.category.name }}</span>
                    </p>
                    
                    <!-- Avtomatik joriy tildagi matn -->
                    <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                    
                    <a href="{% url 'news_detail' news.slug %}" class="btn btn-primary">
                        {% trans "Batafsil" %}
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

**Muhim:** `news.title` va `news.category.name` avtomatik ravishda joriy tildagi tarjimani qaytaradi!

#### 9.2. news_detail.html ni tekshiring

```html
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <article>
        <!-- Avtomatik tarjima -->
        <h1>{{ news.title }}</h1>
        
        <div class="news-meta mb-3">
            <span class="badge bg-info">{{ news.category.name }}</span>
            <span class="text-muted">{{ news.publish_time|date:"d.m.Y" }}</span>
        </div>
        
        <div class="news-body">
            {{ news.body|safe }}
        </div>
    </article>
</div>
{% endblock %}
```

---

### Bosqich 10: Til almashtirish funksiyasini qo'shish

#### 10.1. base.html ga til tanlash menyu qo'shing

`templates/base.html` faylini oching va navbar'ga qo'shing:

```html
{% load i18n %}

<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">{% trans "Yangiliklar" %}</a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news_list' %}">{% trans "Yangiliklar" %}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'contact' %}">{% trans "Aloqa" %}</a>
                    </li>
                </ul>
                
                <!-- Til tanlash -->
                <ul class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="languageDropdown" role="button" 
                           data-bs-toggle="dropdown" aria-expanded="false">
                            🌐 {% trans "Til" %}
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="languageDropdown">
                            <li>
                                <a class="dropdown-item" href="{% url 'set_language' %}?language=uz">
                                    O'zbekcha
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'set_language' %}?language=ru">
                                    Русский
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'set_language' %}?language=en">
                                    English
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    {% block content %}{% endblock %}
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### 10.2. Til almashtirish view yaratish

`news_app/views.py` ga qo'shing:

```python
from django.utils.translation import activate
from django.shortcuts import redirect


def set_language(request):
    """Tilni o'zgartirish view"""
    language = request.GET.get('language', 'uz')
    
    # Tilni faollashtirish
    activate(language)
    
    # Session'ga saqlash
    request.session['django_language'] = language
    
    # Oldingi sahifaga qaytish
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)
```

#### 10.3. URL qo'shish

`news_app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Til almashtirish
    path('set-language/', views.set_language, name='set_language'),
]
```

#### 10.4. config/settings.py ga middleware qo'shish

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Bu qatorni qo'shing!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

### Bosqich 11: Saytni test qilish

#### 11.1. Serverni qayta ishga tushiring

```bash
# Ctrl+C bilan to'xtatib, qayta ishga tushiring
python manage.py runserver
```

#### 11.2. Browser'da test qiling

1. http://127.0.0.1:8000 ga o'ting
2. Navbar'dagi til menyusini oching
3. **Русский** ni tanlang
4. Sayt rus tiliga o'tishi kerak
5. Yangiliklar sarlavhasi va matnlari rus tilida ko'rinadi
6. **English** ni tanlang - ingliz tilida
7. **O'zbekcha** ni tanlang - o'zbek tilida

**Agar tarjimalar ko'rinmasa:**

- Admin panelda tarjimalarni to'ldirganingizni tekshiring
- Browser cache'ni tozalang (Ctrl+Shift+R)
- Serverni qayta ishga tushiring

---

### Bosqich 12: Qidiruv funksiyasini yangilash

Agar sizda qidiruv funksiyasi bo'lsa, barcha tillarda qidirish uchun yangilang.

#### 12.1. views.py da SearchView ni yangilash

```python
from django.db.models import Q
from django.views.generic import ListView


class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if query:
            # Barcha tillarda qidirish
            return News.objects.filter(
                Q(title_uz__icontains=query) |
                Q(title_ru__icontains=query) |
                Q(title_en__icontains=query) |
                Q(body_uz__icontains=query) |
                Q(body_ru__icontains=query) |
                Q(body_en__icontains=query)
            ).filter(status='PB')
        
        return News.objects.filter(status='PB')
```

#### 12.2. URL qo'shish

```python
urlpatterns = [
    # ...
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
```

#### 12.3. Qidiruv formasini base.html ga qo'shish

```html
<!-- Navbar ichida -->
<form class="d-flex" method="GET" action="{% url 'search_results' %}">
    <input class="form-control me-2" type="search" name="q" 
           placeholder="{% trans 'Qidirish...' %}" aria-label="Search">
    <button class="btn btn-outline-success" type="submit">
        {% trans "Qidirish" %}
    </button>
</form>
```

---

### Bosqich 13: GitHub'ga o'zgarishlarni saqlash

#### 13.1. Git status tekshiring

```bash
git status
```

#### 13.2. O'zgarishlarni qo'shish

```bash
git add .
```

#### 13.3. Commit yaratish

```bash
git commit -m "Add django-modeltranslation for multilingual support

- Installed django-modeltranslation package
- Added translation for News and Category models
- Created translation.py files
- Updated admin panel with TranslationAdmin
- Added language switcher to navbar
- Migrated existing data to translation fields
- Added search functionality for all languages"
```

#### 13.4. GitHub'ga yuklash

```bash
git push origin main
```

---

## Xatoliklarni tuzatish (Troubleshooting)

### Xato 1: Tarjimalar ko'rinmaydi

**Sabab:** Admin panelda tarjimalar to'ldirilmagan.

**Yechim:**
```bash
python manage.py migrate_translations
```

Va admin panelda qo'lda to'ldiring.

---

### Xato 2: Admin panelda tab'lar yo'q

**Sabab:** `modeltranslation` `INSTALLED_APPS` da noto'g'ri joyda.

**Yechim:** `modeltranslation` ni `django.contrib.admin` dan keyin qo'ying:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'modeltranslation',  # Bu yerda!
    # ...
]
```

---

### Xato 3: FieldError: Unknown field(s)

**Sabab:** Migratsiya qilinmagan.

**Yechim:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Xato 4: Til almashtirilmaydi

**Sabab:** `LocaleMiddleware` qo'shilmagan.

**Yechim:** `settings.py` da:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',  # Qo'shing!
    # ...
]
```

---

## Qo'shimcha amaliyot topshiriqlari

### Topshiriq 1: Contact modelini tarjima qilish

1. `Contact` modelini tarjima qiling (agar mavjud bo'lsa)
2. `message` maydonini tarjimaga qo'shing
3. Admin panelda test qiling

### Topshiriq 2: Slug maydonini tarjima qilish

1. `translation.py` da `slug` maydonini qo'shing
2. Migratsiya qiling
3. Har bir til uchun alohida slug yarating

### Topshiriq 3: Category filtri

1. Bosh sahifada kategoriyalar ro'yxatini ko'rsating
2. Kategoriya bo'yicha filtrlash
3. Har bir kategoriya nomi joriy tilda ko'rinishi kerak

---

## Natijani tekshirish

✅ Quyidagilarni tekshiring:

1. **Admin panel:**
   - News va Category modellarida 3 ta tab bor (Uzbek, Russian, English)
   - Har bir tab'da tarjimalar to'ldirilgan

2. **Frontend:**
   - Navbar'da til tanlash menyusi mavjud
   - Tilni o'zgartirganda sayt tarjimasi o'zgaradi
   - Yangiliklar sarlavhasi va matni joriy tilda

3. **Qidiruv:**
   - Qidiruv barcha tillarda ishlaydi
   - Rus tilida qidirilsa, rus tilidagi yangiliklar topiladi

4. **GitHub:**
   - O'zgarishlar commit qilingan
   - Remote repository'ga yuklangan

---

## Keyingi qadamlar

Keyingi darsda biz:

1. Template'dagi statik matnlarni tarjima qilamiz
2. `{% trans %}` va `{% blocktrans %}` teglaridan foydalanamiz
3. `.po` va `.mo` fayllarni yaratamiz
4. Tarjima jarayonini to'liq avtomatlashtiramiz

---

## Foydali buyruqlar

```bash
# Virtual muhitni ishga tushirish
pipenv shell

# Server ishga tushirish
python manage.py runserver

# Migratsiya
python manage.py makemigrations
python manage.py migrate

# Ma'lumotlarni ko'chirish
python manage.py migrate_translations

# Git
git add .
git commit -m "Xabar"
git push origin main
```

---

## Xulosa

Ushbu amaliyotda biz:

✅ `django-modeltranslation` o'rnatdik
✅ News va Category modellarini tarjima qildik
✅ Admin panelni sozladik
✅ Til almashtirish funksiyasini qo'shdik
✅ Qidiruv funksiyasini barcha tillar uchun sozladik
✅ GitHub'ga o'zgarishlarni saqladik

Endi sizning saytingiz to'liq ko'p tilli (multilingual) saytga aylandi! 🎉

---

**Tabriklaymiz! Siz Lesson 50 ni muvaffaqiyatli yakunladingiz!** 🚀