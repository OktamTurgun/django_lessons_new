# Dars 52: Template'dagi matnlarni tarjima qilish

## Kirish

Oldingi darsda Django'da i18n tizimini sozladik. Endi template fayllaridagi matnlarni tarjima qilishni o'rganamiz. Django'da template'lardagi matnlarni tarjima qilish uchun maxsus teglar va filtrlar mavjud.

**Dars maqsadi:**
- Template'larda tarjima teglaridan foydalanish
- `{% trans %}` va `{% blocktrans %}` teglari bilan ishlash
- Tarjima fayllarini yaratish va to'ldirish
- O'zgaruvchilarni tarjimada ishlatish

## 1. Template'da tarjima teglari

Django'da template'lardagi matnlarni tarjima qilish uchun ikki asosiy teg mavjud:
- `{% trans %}` - oddiy matnlar uchun
- `{% blocktrans %}` - o'zgaruvchilar va murakkab matnlar uchun

### 1.1. i18n kutubxonasini ulash

Har bir template faylining boshida i18n kutubxonasini yuklash kerak:

```django
{% load i18n %}
```

**Muhim:** Bu qatorni template faylining eng yuqori qismiga, `{% extends %}` dan keyin yozing.

## 2. {% trans %} tegi bilan ishlash

`{% trans %}` tegi oddiy, statik matnlarni tarjima qilish uchun ishlatiladi.

### 2.1. Oddiy tarjima

```django
{% load i18n %}

<h1>{% trans "Yangiliklar" %}</h1>
<p>{% trans "Oxirgi yangiliklar ro'yxati" %}</p>
```

### 2.2. O'zgaruvchiga saqlash

Tarjimani o'zgaruvchiga saqlash mumkin:

```django
{% trans "Salom" as greeting %}
<h1>{{ greeting }}</h1>
```

### 2.3. Noop - tarjima qilmaslik

Ba'zan matnni faqat belgilash, lekin hozir tarjima qilmaslik kerak bo'ladi:

```django
{% trans "Future translation" noop %}
```

## 3. {% blocktrans %} tegi bilan ishlash

`{% blocktrans %}` tegi o'zgaruvchilar va murakkab matnlar uchun ishlatiladi.

### 3.1. O'zgaruvchilar bilan tarjima

```django
{% load i18n %}

{% blocktrans %}
Salom {{ user_name }}, saytga xush kelibsiz!
{% endblocktrans %}
```

### 3.2. Count bilan ishlash (ko'plik shakl)

```django
{% blocktrans count counter=comments.count %}
{{ counter }} ta izoh
{% plural %}
{{ counter }} ta izohlar
{% endblocktrans %}
```

**Tushuntirish:**
- `count` parametri raqamni aniqlaydi
- Agar `counter=1` bo'lsa, birinchi variant chiqadi
- Agar `counter>1` bo'lsa, `{% plural %}` dan keyingi variant chiqadi

### 3.3. Context o'zgaruvchilari

```django
{% blocktrans with author=news.author.get_full_name %}
Muallif: {{ author }}
{% endblocktrans %}
```

**Yoki bir nechta o'zgaruvchi:**

```django
{% blocktrans with name=user.name date=news.publish_time|date:"d M Y" %}
{{ name }} tomonidan {{ date }} da e'lon qilingan
{% endblocktrans %}
```

## 4. Amaliy misol: Yangiliklar sahifasini tarjima qilish

### 4.1. base.html faylini tayyorlash

```django
{% load i18n %}
{% load static %}

<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% trans "Yangiliklar sayti" %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <a href="{% url 'home' %}" class="logo">
                {% trans "Yangiliklar" %}
            </a>
            <ul class="nav-menu">
                <li><a href="{% url 'home' %}">{% trans "Bosh sahifa" %}</a></li>
                <li><a href="{% url 'news_list' %}">{% trans "Yangiliklar" %}</a></li>
                <li><a href="{% url 'contact' %}">{% trans "Aloqa" %}</a></li>
                
                {% if user.is_authenticated %}
                    <li><a href="{% url 'profile' %}">{% trans "Profil" %}</a></li>
                    <li><a href="{% url 'logout' %}">{% trans "Chiqish" %}</a></li>
                {% else %}
                    <li><a href="{% url 'login' %}">{% trans "Kirish" %}</a></li>
                    <li><a href="{% url 'signup' %}">{% trans "Ro'yxatdan o'tish" %}</a></li>
                {% endif %}
            </ul>
            
            <!-- Til tanlash -->
            <form action="{% url 'set_language' %}" method="post" class="language-selector">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ redirect_to }}">
                <select name="language" onchange="this.form.submit()">
                    {% get_current_language as LANGUAGE_CODE %}
                    {% get_available_languages as LANGUAGES %}
                    {% for lang_code, lang_name in LANGUAGES %}
                        <option value="{{ lang_code }}"{% if lang_code == LANGUAGE_CODE %} selected{% endif %}>
                            {{ lang_name }}
                        </option>
                    {% endfor %}
                </select>
            </form>
        </div>
    </nav>

    <!-- Content -->
    <main class="main-content">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>{% blocktrans %}© 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.{% endblocktrans %}</p>
        </div>
    </footer>
</body>
</html>
```

**Tushuntirish:**
- `{% load i18n %}` - i18n kutubxonasini yuklaymiz
- `{% trans %}` - oddiy matnlarni tarjima qilamiz
- `{% get_current_language %}` - joriy tilni olamiz
- `{% get_available_languages %}` - mavjud tillar ro'yxatini olamiz

### 4.2. news_list.html faylini tarjima qilish

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Yangiliklar ro'yxati" %}{% endblock %}

{% block content %}
<div class="container">
    <h1>{% trans "Barcha yangiliklar" %}</h1>
    
    <!-- Qidiruv -->
    <div class="search-box">
        <form method="get" action="{% url 'news_search' %}">
            <input type="text" name="q" placeholder="{% trans 'Yangilik qidirish...' %}" value="{{ request.GET.q }}">
            <button type="submit">{% trans "Qidirish" %}</button>
        </form>
    </div>

    <!-- Yangiliklar ro'yxati -->
    {% if news_list %}
        <div class="news-grid">
            {% for news in news_list %}
            <article class="news-card">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" alt="{{ news.title }}">
                {% endif %}
                
                <div class="news-content">
                    <span class="category">{{ news.category.name }}</span>
                    <h2><a href="{{ news.get_absolute_url }}">{{ news.title }}</a></h2>
                    <p>{{ news.body|truncatewords:20 }}</p>
                    
                    <div class="news-meta">
                        <span class="author">
                            {% blocktrans with author=news.author.get_full_name %}
                            Muallif: {{ author }}
                            {% endblocktrans %}
                        </span>
                        <span class="date">{{ news.publish_time|date:"d M Y" }}</span>
                        <span class="views">
                            {% blocktrans count counter=news.views_count %}
                            {{ counter }} ko'rishlar
                            {% plural %}
                            {{ counter }} ko'rishlar
                            {% endblocktrans %}
                        </span>
                    </div>
                    
                    <a href="{{ news.get_absolute_url }}" class="read-more">
                        {% trans "Batafsil o'qish" %}
                    </a>
                </div>
            </article>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">{% trans "Birinchi" %}</a>
                <a href="?page={{ page_obj.previous_page_number }}">{% trans "Oldingi" %}</a>
            {% endif %}
            
            <span class="current-page">
                {% blocktrans with current=page_obj.number total=page_obj.paginator.num_pages %}
                Sahifa {{ current }} / {{ total }}
                {% endblocktrans %}
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">{% trans "Keyingi" %}</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">{% trans "Oxirgi" %}</a>
            {% endif %}
        </div>
        {% endif %}
        
    {% else %}
        <p class="no-news">{% trans "Hozircha yangiliklar yo'q." %}</p>
    {% endif %}
</div>
{% endblock %}
```

### 4.3. news_detail.html faylini tarjima qilish

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container">
    <article class="news-detail">
        <!-- Yangilik sarlavhasi -->
        <h1>{{ news.title }}</h1>
        
        <!-- Meta ma'lumotlar -->
        <div class="news-meta">
            <span class="category">{{ news.category.name }}</span>
            <span class="author">
                {% blocktrans with author=news.author.get_full_name %}
                Muallif: {{ author }}
                {% endblocktrans %}
            </span>
            <span class="date">{{ news.publish_time|date:"d M Y, H:i" }}</span>
            <span class="views">
                {% blocktrans count counter=news.views_count %}
                {{ counter }} ko'rish
                {% plural %}
                {{ counter }} ko'rishlar
                {% endblocktrans %}
            </span>
        </div>

        <!-- Rasm -->
        {% if news.photo %}
        <div class="news-image">
            <img src="{{ news.photo.url }}" alt="{{ news.title }}">
        </div>
        {% endif %}

        <!-- Yangilik matni -->
        <div class="news-body">
            {{ news.body|linebreaks }}
        </div>

        <!-- Tahrirlash tugmalari (faqat muallif uchun) -->
        {% if request.user == news.author or request.user.is_staff %}
        <div class="news-actions">
            <a href="{% url 'news_update' news.slug %}" class="btn btn-edit">
                {% trans "Tahrirlash" %}
            </a>
            <a href="{% url 'news_delete' news.slug %}" class="btn btn-delete">
                {% trans "O'chirish" %}
            </a>
        </div>
        {% endif %}
    </article>

    <!-- Izohlar bo'limi -->
    <section class="comments-section">
        <h2>
            {% blocktrans count counter=comments.count %}
            {{ counter }} ta izoh
            {% plural %}
            {{ counter }} ta izohlar
            {% endblocktrans %}
        </h2>

        <!-- Izoh qoldirish formasi -->
        {% if user.is_authenticated %}
        <div class="comment-form">
            <h3>{% trans "Izoh qoldirish" %}</h3>
            <form method="post" action="{% url 'news_comment' news.slug %}">
                {% csrf_token %}
                <div class="form-group">
                    <label for="id_body">{% trans "Sizning izohingiz" %}</label>
                    {{ comment_form.body }}
                </div>
                <button type="submit" class="btn btn-primary">
                    {% trans "Izoh yuborish" %}
                </button>
            </form>
        </div>
        {% else %}
        <p class="login-message">
            {% trans "Izoh qoldirish uchun" %}
            <a href="{% url 'login' %}?next={{ request.path }}">{% trans "tizimga kiring" %}</a>.
        </p>
        {% endif %}

        <!-- Izohlar ro'yxati -->
        {% if comments %}
        <div class="comments-list">
            {% for comment in comments %}
            <div class="comment">
                <div class="comment-header">
                    <strong>{{ comment.user.get_full_name|default:comment.user.username }}</strong>
                    <span class="comment-date">{{ comment.created_time|date:"d M Y, H:i" }}</span>
                </div>
                <div class="comment-body">
                    {{ comment.body|linebreaks }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="no-comments">{% trans "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!" %}</p>
        {% endif %}
    </section>
</div>
{% endblock %}
```

## 5. Tarjima fayllarini yaratish

Template'lardagi matnlarni belgilab bo'lgach, tarjima fayllarini yaratamiz.

### 5.1. locale papkasini yaratish

Loyiha asosiy papkasida `locale` papkasini yarating:

```bash
mkdir locale
```

### 5.2. Tarjima fayllarini generatsiya qilish

Terminal orqali quyidagi buyruqni bajaring:

```bash
django-admin makemessages -l en
django-admin makemessages -l ru
```

**Tushuntirish:**
- `-l en` - ingliz tili uchun
- `-l ru` - rus tili uchun

Bu buyruq `locale` papkasida quyidagi tuzilmani yaratadi:

```
locale/
    en/
        LC_MESSAGES/
            django.po
    ru/
        LC_MESSAGES/
            django.po
```

### 5.3. .po fayllarini to'ldirish

`locale/en/LC_MESSAGES/django.po` faylini oching va tarjimalarni qo'shing:

```po
# locale/en/LC_MESSAGES/django.po

msgid "Yangiliklar"
msgstr "News"

msgid "Bosh sahifa"
msgstr "Home"

msgid "Yangiliklar ro'yxati"
msgstr "News List"

msgid "Barcha yangiliklar"
msgstr "All News"

msgid "Qidirish"
msgstr "Search"

msgid "Yangilik qidirish..."
msgstr "Search news..."

msgid "Batafsil o'qish"
msgstr "Read more"

msgid "Birinchi"
msgstr "First"

msgid "Oldingi"
msgstr "Previous"

msgid "Keyingi"
msgstr "Next"

msgid "Oxirgi"
msgstr "Last"

#: templates/news_detail.html:15
#, python-format
msgid "Muallif: %(author)s"
msgstr "Author: %(author)s"

#: templates/news_detail.html:25
msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s view"
msgstr[1] "%(counter)s views"

msgid "Tahrirlash"
msgstr "Edit"

msgid "O'chirish"
msgstr "Delete"

msgid "Izoh qoldirish"
msgstr "Leave a comment"

msgid "Sizning izohingiz"
msgstr "Your comment"

msgid "Izoh yuborish"
msgstr "Submit comment"

msgid "Izoh qoldirish uchun"
msgstr "To leave a comment"

msgid "tizimga kiring"
msgstr "log in"

msgid "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!"
msgstr "No comments yet. Be the first to comment!"

msgid "Hozircha yangiliklar yo'q."
msgstr "No news yet."

#: templates/news_list.html:45
#, python-format
msgid "Sahifa %(current)s / %(total)s"
msgstr "Page %(current)s of %(total)s"
```

**Rus tili uchun** `locale/ru/LC_MESSAGES/django.po`:

```po
# locale/ru/LC_MESSAGES/django.po

msgid "Yangiliklar"
msgstr "Новости"

msgid "Bosh sahifa"
msgstr "Главная"

msgid "Yangiliklar ro'yxati"
msgstr "Список новостей"

msgid "Barcha yangiliklar"
msgstr "Все новости"

msgid "Qidirish"
msgstr "Поиск"

msgid "Yangilik qidirish..."
msgstr "Поиск новостей..."

msgid "Batafsil o'qish"
msgstr "Читать далее"

msgid "Birinchi"
msgstr "Первая"

msgid "Oldingi"
msgstr "Предыдущая"

msgid "Keyingi"
msgstr "Следующая"

msgid "Oxirgi"
msgstr "Последняя"

#, python-format
msgid "Muallif: %(author)s"
msgstr "Автор: %(author)s"

msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s просмотр"
msgstr[1] "%(counter)s просмотра"
msgstr[2] "%(counter)s просмотров"

msgid "Tahrirlash"
msgstr "Редактировать"

msgid "O'chirish"
msgstr "Удалить"

msgid "Izoh qoldirish"
msgstr "Оставить комментарий"

msgid "Sizning izohingiz"
msgstr "Ваш комментарий"

msgid "Izoh yuborish"
msgstr "Отправить комментарий"

msgid "Izoh qoldirish uchun"
msgstr "Чтобы оставить комментарий"

msgid "tizimga kiring"
msgstr "войдите в систему"

msgid "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!"
msgstr "Пока нет комментариев. Будьте первым!"

msgid "Hozircha yangiliklar yo'q."
msgstr "Пока нет новостей."

#, python-format
msgid "Sahifa %(current)s / %(total)s"
msgstr "Страница %(current)s из %(total)s"
```

### 5.4. Tarjimalarni kompilyatsiya qilish

Tarjimalarni to'ldirgach, ularni kompilyatsiya qiling:

```bash
django-admin compilemessages
```

Bu buyruq `.po` fayllardan `.mo` fayllarni yaratadi. Django `.mo` fayllarni o'qiydi.

## 6. Til tanlash funksiyasini qo'shish

### 6.1. URL sozlamalari

Asosiy `urls.py` faylida:

```python
# config/urls.py

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Til o'zgartirish uchun
]

# i18n patterns - til prefiksi bilan URL'lar
urlpatterns += i18n_patterns(
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=False,  # Asosiy til uchun prefiks qo'shmaslik
)

# Media fayllar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Tushuntirish:**
- `i18n_patterns` - URL'larga til prefiksini qo'shadi (masalan: `/en/news/`, `/ru/news/`)
- `prefix_default_language=False` - asosiy til uchun prefiks qo'shmaslik
- `path('i18n/', include('django.conf.urls.i18n'))` - til o'zgartirish URL'i

### 6.2. Middleware sozlamalari

`settings.py` da `LocaleMiddleware` ni qo'shing:

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Bu qatorni qo'shing
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Muhim:** `LocaleMiddleware` `SessionMiddleware` dan keyin va `CommonMiddleware` dan oldin turishi kerak.

## 7. Xatolarni tuzatish (Debugging)

### 7.1. Tarjima ko'rinmasa

Agar tarjimalar ko'rinmasa:

1. **Server'ni qayta ishga tushiring:**
```bash
python manage.py runserver
```

2. **Tarjimalarni qayta kompilyatsiya qiling:**
```bash
django-admin compilemessages
```

3. **Cache'ni tozalang:**
```bash
python manage.py clear_cache
```

### 7.2. Ko'plik shakllar ishlamasa

Rus tilida ko'plik shakl uchun 3 ta variant kerak:

```po
msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s просмотр"     # 1, 21, 31...
msgstr[1] "%(counter)s просмотра"    # 2-4, 22-24...
msgstr[2] "%(counter)s просмотров"   # 5-20, 25-30...
```

### 7.3. .po faylni yangilash

Yangi tarjima kerakli matnlar qo'shilganda:

```bash
django-admin makemessages -l en --ignore=venv
django-admin makemessages -l ru --ignore=venv
django-admin compilemessages
```

`--ignore=venv` - virtual muhitni e'tiborsiz qoldirish

## 8. Best Practices (Eng yaxshi amaliyotlar)

### 8.1. Tarjima matnlarini to'g'ri yozish

**Yaxshi:**
```django
{% trans "Bosh sahifa" %}
```

**Yomon:**
```django
{% trans "Bosh sahifa " %}  <!-- Ortiqcha bo'shliq -->
```

### 8.2. Context ishlatish

O'zgaruvchilar bilan ishlashda context ishlatish:

```django
{% blocktrans with name=user.name %}
Salom, {{ name }}!
{% endblocktrans %}
```

### 8.3. Uzun matnlar uchun

Uzun matnlar uchun `blocktrans` ishlatish:

```django
{% blocktrans %}
Bu juda uzun matn bo'lib, bir necha
qatorga cho'zilishi mumkin. Bunday
holatlarda blocktrans ishlatish kerak.
{% endblocktrans %}
```

### 8.4. Tarjima fayllarini tartibli saqlash

Tarjima fayllarini kategoriyalarga bo'lish:

```
locale/
    en/
        LC_MESSAGES/
            django.po          # Umumiy tarjimalar
    ru/
        LC_MESSAGES/
            django.po
```

### 8.5. Izohlar qo'shish

`.po` faylga izohlar qo'shish:

```po
# Bosh sahifa menyusi uchun
msgid "Bosh sahifa"
msgstr "Home"

# News detail sahifasidagi tugma
msgid "Batafsil o'qish"
msgstr "Read more"
```

## 9. Qo'shimcha maslahatlar

### 9.1. Placeholder matnlar

Input maydonlari uchun:

```django
<input type="text" placeholder="{% trans 'Nomingizni kiriting' %}">
```

### 9.2. JavaScript bilan ishlash

JavaScript fayllarida ham tarjima kerak bo'lsa, Django'ning `javascript_catalog` view'dan foydalaning.

### 9.3. SEO uchun

Har bir til uchun alohida meta teglar:

```django
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta name="description" content="{% trans 'Sayt tavsifi' %}">
    <title>{% trans "Sahifa sarlavhasi" %}</title>
</head>
```

### 9.4. Sana va vaqt formatlar

Har bir til uchun sana formati:

```python
# settings.py

DATE_FORMAT = 'd E Y'  # 01 January 2024
DATETIME_FORMAT = 'd E Y H:i'  # 01 January 2024 15:30
```

## 10. Xulosa

Ushbu darsda biz:
- Template'larda `{% trans %}` va `{% blocktrans %}` teglaridan foydalanishni o'rgandik
- Tarjima fayllarini yaratish va to'ldirishni o'rgandik
- Til tanlash funksiyasini qo'shdik
- Ko'plik shakllar va o'zgaruvchilar bilan ishlashni ko'rdik

**Keyingi dars:** ModelTranslation moduli orqali model maydonlarini tarjima qilish

## Topshiriq

1. O'z loyihangizning barcha template fayllaridagi matnlarni `{% trans %}` va `{% blocktrans %}` teglari bilan belgilang
2. Kamida 2 ta til uchun tarjima fayllarini yarating va to'ldiring
3. Til tanlash funksiyasini qo'shing va tekshiring
4. Ko'plik shakllar to'g'ri ishlayotganini tekshiring
5. GitHub'ga o'zgarishlarni yuklang

**E'tibor bering:** Tarjimalarni kompilyatsiya qilishni unutmang: `django-admin compilemessages`