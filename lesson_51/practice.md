# Dars 52: Amaliyot - Template'dagi matnlarni tarjima qilish

## Maqsad

Ushbu amaliyotda yangiliklar saytining barcha template fayllaridagi matnlarni tarjima qilish, tarjima fayllarini yaratish va til tanlash funksiyasini to'liq ishga tushiramiz.

## Boshlash oldidan

**Kerakli bilimlar:**
- Django template tizimi
- i18n asoslari (lesson_51)
- Template teglari va filtrlar

**Loyiha holati:**
- Virtual muhit faol
- Django o'rnatilgan
- Yangiliklar sayti ishlayotgan

## Bosqich 1: Loyihani tayyorlash

### 1.1. settings.py faylini tekshirish

Avval `settings.py` faylidagi sozlamalarni tekshiring:

```python
# config/settings.py

from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'uz'

LANGUAGES = [
    ('uz', _('O\'zbekcha')),
    ('en', _('English')),
    ('ru', _('Русский')),
]

TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

### 1.2. Middleware'ni tekshirish

`LocaleMiddleware` qo'shilganligini tekshiring:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Bu yerda
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 1.3. locale papkasini yaratish

Terminal orqali:

```bash
mkdir locale
```

Loyiha tuzilmasi:

```
news_project/
    config/
    news/
    accounts/
    locale/          # Yangi papka
    templates/
    static/
    media/
    manage.py
```

## Bosqich 2: Base template'ni tarjima qilish

### 2.1. templates/base.html faylini ochish

Faylning boshiga i18n kutubxonasini qo'shing:

```django
{% load i18n %}
{% load static %}

<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% trans "Yangiliklar sayti" %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
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
                    <li>
                        <a href="{% url 'profile' %}">
                            {% blocktrans with name=user.username %}
                            Salom, {{ name }}
                            {% endblocktrans %}
                        </a>
                    </li>
                    <li><a href="{% url 'logout' %}">{% trans "Chiqish" %}</a></li>
                {% else %}
                    <li><a href="{% url 'login' %}">{% trans "Kirish" %}</a></li>
                    <li><a href="{% url 'signup' %}">{% trans "Ro'yxatdan o'tish" %}</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>

    <main class="main-content">
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <footer class="footer">
        <div class="container">
            <p>{% blocktrans %}© 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.{% endblocktrans %}</p>
        </div>
    </footer>
</body>
</html>
```

**Tushuntirish:**
- `{% load i18n %}` - i18n kutubxonasini yuklaymiz (eng yuqorida)
- `{% trans %}` - oddiy matnlar uchun
- `{% blocktrans %}` - o'zgaruvchilar bilan matnlar uchun

### 2.2. Til tanlash menyusini qo'shish

Navbar ichiga til tanlash menyusini qo'shing:

```django
<nav class="navbar">
    <div class="container">
        <a href="{% url 'home' %}" class="logo">
            {% trans "Yangiliklar" %}
        </a>
        <ul class="nav-menu">
            <!-- Eski menyular... -->
        </ul>
        
        <!-- Til tanlash -->
        <div class="language-selector">
            <form action="{% url 'set_language' %}" method="post">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ redirect_to }}">
                <select name="language" onchange="this.form.submit()" class="language-dropdown">
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
    </div>
</nav>
```

## Bosqich 3: Home sahifasini tarjima qilish

### 3.1. templates/news/index.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Bosh sahifa" %}{% endblock %}

{% block content %}
<div class="container">
    <!-- Hero section -->
    <section class="hero">
        <h1>{% trans "Yangiliklar saytiga xush kelibsiz!" %}</h1>
        <p>{% trans "Eng so'nggi va dolzarb yangiliklar bilan tanishing" %}</p>
        <a href="{% url 'news_list' %}" class="btn btn-primary">
            {% trans "Barcha yangiliklar" %}
        </a>
    </section>

    <!-- Kategoriyalar bo'yicha yangiliklar -->
    {% for category, news_list in category_news.items %}
    <section class="category-section">
        <div class="section-header">
            <h2>{{ category.name }}</h2>
            <a href="{% url 'news_by_category' category.slug %}" class="view-all">
                {% trans "Barchasini ko'rish" %}
            </a>
        </div>

        {% if news_list %}
        <div class="news-grid">
            {% for news in news_list %}
            <article class="news-card">
                {% if news.photo %}
                <img src="{{ news.photo.url }}" alt="{{ news.title }}">
                {% endif %}
                
                <div class="news-content">
                    <span class="category-badge">{{ news.category.name }}</span>
                    <h3><a href="{{ news.get_absolute_url }}">{{ news.title }}</a></h3>
                    <p>{{ news.body|truncatewords:15 }}</p>
                    
                    <div class="news-meta">
                        <span class="date">{{ news.publish_time|date:"d M Y" }}</span>
                        <span class="views">
                            {% blocktrans count counter=news.views_count %}
                            {{ counter }} ko'rish
                            {% plural %}
                            {{ counter }} ko'rishlar
                            {% endblocktrans %}
                        </span>
                    </div>
                    
                    <a href="{{ news.get_absolute_url }}" class="read-more">
                        {% trans "O'qish" %} →
                    </a>
                </div>
            </article>
            {% endfor %}
        </div>
        {% else %}
        <p class="no-news">
            {% blocktrans with name=category.name %}
            {{ name }} kategoriyasida yangiliklar yo'q.
            {% endblocktrans %}
        </p>
        {% endif %}
    </section>
    {% endfor %}
</div>
{% endblock %}
```

## Bosqich 4: Yangiliklar ro'yxati sahifasini tarjima qilish

### 4.1. templates/news/news_list.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Yangiliklar ro'yxati" %}{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>{% trans "Barcha yangiliklar" %}</h1>
        <p class="page-subtitle">
            {% blocktrans count counter=paginator.count %}
            Jami {{ counter }} ta yangilik
            {% plural %}
            Jami {{ counter }} ta yangiliklar
            {% endblocktrans %}
        </p>
    </div>

    <!-- Qidiruv va filtr -->
    <div class="search-filter-section">
        <form method="get" action="{% url 'news_search' %}" class="search-form">
            <input 
                type="text" 
                name="q" 
                placeholder="{% trans 'Yangilik qidirish...' %}" 
                value="{{ request.GET.q }}"
                class="search-input"
            >
            <button type="submit" class="btn btn-search">
                {% trans "Qidirish" %}
            </button>
        </form>

        <!-- Kategoriya filtri -->
        <div class="category-filter">
            <a href="{% url 'news_list' %}" class="filter-btn {% if not request.GET.category %}active{% endif %}">
                {% trans "Barchasi" %}
            </a>
            {% for cat in categories %}
            <a href="?category={{ cat.slug }}" class="filter-btn {% if request.GET.category == cat.slug %}active{% endif %}">
                {{ cat.name }}
            </a>
            {% endfor %}
        </div>
    </div>

    <!-- Yangiliklar ro'yxati -->
    {% if news_list %}
    <div class="news-grid">
        {% for news in news_list %}
        <article class="news-card">
            {% if news.photo %}
            <div class="news-image">
                <img src="{{ news.photo.url }}" alt="{{ news.title }}">
                <span class="category-badge">{{ news.category.name }}</span>
            </div>
            {% endif %}
            
            <div class="news-content">
                <h2><a href="{{ news.get_absolute_url }}">{{ news.title }}</a></h2>
                <p class="news-excerpt">{{ news.body|truncatewords:20 }}</p>
                
                <div class="news-meta">
                    <span class="author">
                        {% blocktrans with author=news.author.get_full_name|default:news.author.username %}
                        {{ author }}
                        {% endblocktrans %}
                    </span>
                    <span class="date">{{ news.publish_time|date:"d M Y" }}</span>
                    <span class="views">
                        👁 {{ news.views_count }}
                    </span>
                    <span class="comments">
                        💬 {% blocktrans count counter=news.comments.count %}
                        {{ counter }} izoh
                        {% plural %}
                        {{ counter }} izohlar
                        {% endblocktrans %}
                    </span>
                </div>
                
                <a href="{{ news.get_absolute_url }}" class="btn btn-outline">
                    {% trans "Batafsil o'qish" %}
                </a>
            </div>
        </article>
        {% endfor %}
    </div>

    <!-- Pagination -->
    {% if is_paginated %}
    <nav class="pagination">
        {% if page_obj.has_previous %}
            <a href="?page=1" class="page-link">{% trans "Birinchi" %}</a>
            <a href="?page={{ page_obj.previous_page_number }}" class="page-link">{% trans "Oldingi" %}</a>
        {% endif %}

        <span class="current-page">
            {% blocktrans with current=page_obj.number total=page_obj.paginator.num_pages %}
            Sahifa {{ current }} / {{ total }}
            {% endblocktrans %}
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}" class="page-link">{% trans "Keyingi" %}</a>
            <a href="?page={{ page_obj.paginator.num_pages }}" class="page-link">{% trans "Oxirgi" %}</a>
        {% endif %}
    </nav>
    {% endif %}

    {% else %}
    <div class="no-results">
        <h3>{% trans "Yangiliklar topilmadi" %}</h3>
        <p>{% trans "Hozircha yangiliklar yo'q yoki qidiruv natijasi topilmadi." %}</p>
        <a href="{% url 'news_list' %}" class="btn btn-primary">
            {% trans "Barcha yangiliklarni ko'rish" %}
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}
```

## Bosqich 5: Yangilik detali sahifasini tarjima qilish

### 5.1. templates/news/news_detail.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container">
    <article class="news-detail">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
            <a href="{% url 'home' %}">{% trans "Bosh sahifa" %}</a> /
            <a href="{% url 'news_list' %}">{% trans "Yangiliklar" %}</a> /
            <span>{{ news.title|truncatewords:5 }}</span>
        </nav>

        <!-- Yangilik sarlavhasi -->
        <header class="news-header">
            <span class="category-badge">{{ news.category.name }}</span>
            <h1>{{ news.title }}</h1>
            
            <div class="news-meta">
                <div class="meta-item">
                    <span class="meta-label">{% trans "Muallif:" %}</span>
                    <span class="meta-value">
                        {{ news.author.get_full_name|default:news.author.username }}
                    </span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">{% trans "Sana:" %}</span>
                    <span class="meta-value">
                        {{ news.publish_time|date:"d M Y, H:i" }}
                    </span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">{% trans "Ko'rishlar:" %}</span>
                    <span class="meta-value">
                        {% blocktrans count counter=news.views_count %}
                        {{ counter }} ko'rish
                        {% plural %}
                        {{ counter }} ko'rishlar
                        {% endblocktrans %}
                    </span>
                </div>
            </div>
        </header>

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

        <!-- Tahrirlash tugmalari -->
        {% if request.user == news.author or request.user.is_staff %}
        <div class="news-actions">
            <a href="{% url 'news_update' news.slug %}" class="btn btn-edit">
                {% trans "Tahrirlash" %}
            </a>
            <a href="{% url 'news_delete' news.slug %}" class="btn btn-delete" 
               onclick="return confirm('{% trans "Rostdan ham o\'chirmoqchimisiz?" %}')">
                {% trans "O'chirish" %}
            </a>
        </div>
        {% endif %}
    </article>

    <!-- Izohlar bo'limi -->
    <section class="comments-section">
        <h2 class="section-title">
            {% blocktrans count counter=comments.count %}
            {{ counter }} ta izoh
            {% plural %}
            {{ counter }} ta izohlar
            {% endblocktrans %}
        </h2>

        <!-- Izoh qoldirish formasi -->
        {% if user.is_authenticated %}
        <div class="comment-form-wrapper">
            <h3>{% trans "Izoh qoldirish" %}</h3>
            <form method="post" action="{% url 'news_comment' news.slug %}" class="comment-form">
                {% csrf_token %}
                
                <div class="form-group">
                    <label for="{{ comment_form.body.id_for_label }}">
                        {% trans "Sizning izohingiz" %}
                    </label>
                    {{ comment_form.body }}
                    {% if comment_form.body.errors %}
                        <div class="error-message">
                            {{ comment_form.body.errors }}
                        </div>
                    {% endif %}
                </div>
                
                <button type="submit" class="btn btn-primary">
                    {% trans "Izoh yuborish" %}
                </button>
            </form>
        </div>
        {% else %}
        <div class="login-prompt">
            <p>
                {% trans "Izoh qoldirish uchun" %}
                <a href="{% url 'login' %}?next={{ request.path }}">
                    {% trans "tizimga kiring" %}
                </a>
                {% trans "yoki" %}
                <a href="{% url 'signup' %}?next={{ request.path }}">
                    {% trans "ro'yxatdan o'ting" %}
                </a>.
            </p>
        </div>
        {% endif %}

        <!-- Izohlar ro'yxati -->
        {% if comments %}
        <div class="comments-list">
            {% for comment in comments %}
            <div class="comment">
                <div class="comment-header">
                    <div class="comment-author">
                        <strong>
                            {{ comment.user.get_full_name|default:comment.user.username }}
                        </strong>
                    </div>
                    <div class="comment-date">
                        {{ comment.created_time|date:"d M Y, H:i" }}
                    </div>
                </div>
                <div class="comment-body">
                    {{ comment.body|linebreaks }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="no-comments">
            <p>{% trans "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!" %}</p>
        </div>
        {% endif %}
    </section>
</div>
{% endblock %}
```

## Bosqich 6: Contact sahifasini tarjima qilish

### 6.1. templates/news/contact.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Aloqa" %}{% endblock %}

{% block content %}
<div class="container">
    <div class="contact-page">
        <h1>{% trans "Biz bilan bog'laning" %}</h1>
        <p class="page-description">
            {% trans "Sizning fikr va takliflaringizni eshitishdan xursandmiz. Quyidagi forma orqali biz bilan bog'lanishingiz mumkin." %}
        </p>

        <div class="contact-wrapper">
            <!-- Aloqa formasi -->
            <div class="contact-form-section">
                <h2>{% trans "Xabar yuborish" %}</h2>
                
                <form method="post" class="contact-form">
                    {% csrf_token %}
                    
                    <div class="form-group">
                        <label for="{{ form.name.id_for_label }}">
                            {% trans "Ismingiz" %} <span class="required">*</span>
                        </label>
                        {{ form.name }}
                        {% if form.name.errors %}
                            <div class="error-message">{{ form.name.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="form-group">
                        <label for="{{ form.email.id_for_label }}">
                            {% trans "Email manzilingiz" %} <span class="required">*</span>
                        </label>
                        {{ form.email }}
                        {% if form.email.errors %}
                            <div class="error-message">{{ form.email.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="form-group">
                        <label for="{{ form.message.id_for_label }}">
                            {% trans "Xabaringiz" %} <span class="required">*</span>
                        </label>
                        {{ form.message }}
                        {% if form.message.errors %}
                            <div class="error-message">{{ form.message.errors }}</div>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-primary">
                        {% trans "Xabarni yuborish" %}
                    </button>
                </form>
            </div>

            <!-- Aloqa ma'lumotlari -->
            <div class="contact-info-section">
                <h2>{% trans "Aloqa ma'lumotlari" %}</h2>
                
                <div class="contact-info">
                    <div class="info-item">
                        <h3>{% trans "Manzil" %}</h3>
                        <p>{% trans "Toshkent, O'zbekiston" %}</p>
                    </div>

                    <div class="info-item">
                        <h3>{% trans "Telefon" %}</h3>
                        <p>+998 90 123 45 67</p>
                    </div>

                    <div class="info-item">
                        <h3>{% trans "Email" %}</h3>
                        <p>info@yangiliklar.uz</p>
                    </div>

                    <div class="info-item">
                        <h3>{% trans "Ish vaqti" %}</h3>
                        <p>{% trans "Dushanba - Juma: 9:00 - 18:00" %}</p>
                        <p>{% trans "Dam olish kunlari: Shanba, Yakshanba" %}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Bosqich 7: Authentication sahifalarini tarjima qilish

### 7.1. templates/registration/login.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Tizimga kirish" %}{% endblock %}

{% block content %}
<div class="container">
    <div class="auth-page">
        <div class="auth-box">
            <h1>{% trans "Tizimga kirish" %}</h1>
            <p class="auth-subtitle">
                {% trans "Hisobingizga kirish uchun ma'lumotlaringizni kiriting" %}
            </p>

            <form method="post" class="auth-form">
                {% csrf_token %}
                
                <div class="form-group">
                    <label for="{{ form.username.id_for_label }}">
                        {% trans "Foydalanuvchi nomi" %}
                    </label>
                    {{ form.username }}
                    {% if form.username.errors %}
                        <div class="error-message">{{ form.username.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="{{ form.password.id_for_label }}">
                        {% trans "Parol" %}
                    </label>
                    {{ form.password }}
                    {% if form.password.errors %}
                        <div class="error-message">{{ form.password.errors }}</div>
                    {% endif %}
                </div>

                {% if form.non_field_errors %}
                    <div class="error-message">
                        {{ form.non_field_errors }}
                    </div>
                {% endif %}

                <button type="submit" class="btn btn-primary btn-block">
                    {% trans "Kirish" %}
                </button>
            </form>

            <div class="auth-links">
                <p>
                    <a href="{% url 'password_reset' %}">
                        {% trans "Parolni unutdingizmi?" %}
                    </a>
                </p>
                <p>
                    {% trans "Hisobingiz yo'qmi?" %}
                    <a href="{% url 'signup' %}">
                        {% trans "Ro'yxatdan o'ting" %}
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 7.2. templates/registration/signup.html

```django
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Ro'yxatdan o'tish" %}{% endblock %}

{% block content %}
<div class="container">
    <div class="auth-page">
        <div class="auth-box">
            <h1>{% trans "Ro'yxatdan o'tish" %}</h1>
            <p class="auth-subtitle">
                {% trans "Yangi hisob yaratish uchun quyidagi ma'lumotlarni to'ldiring" %}
            </p>

            <form method="post" class="auth-form">
                {% csrf_token %}
                
                <div class="form-group">
                    <label for="{{ form.username.id_for_label }}">
                        {% trans "Foydalanuvchi nomi" %}
                    </label>
                    {{ form.username }}
                    <small class="form-text">
                        {% trans "150 belgidan kam. Faqat harflar, raqamlar va @/./+/-/_ belgilar" %}
                    </small>
                    {% if form.username.errors %}
                        <div class="error-message">{{ form.username.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="{{ form.first_name.id_for_label }}">
                            {% trans "Ism" %}
                        </label>
                        {{ form.first_name }}
                        {% if form.first_name.errors %}
                            <div class="error-message">{{ form.first_name.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="form-group">
                        <label for="{{ form.last_name.id_for_label }}">
                            {% trans "Familiya" %}
                        </label>
                        {{ form.last_name }}
                        {% if form.last_name.errors %}
                            <div class="error-message">{{ form.last_name.errors }}</div>
                        {% endif %}
                    </div>
                </div>

                <div class="form-group">
                    <label for="{{ form.email.id_for_label }}">
                        {% trans "Email manzil" %}
                    </label>
                    {{ form.email }}
                    {% if form.email.errors %}
                        <div class="error-message">{{ form.email.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="{{ form.password1.id_for_label }}">
                        {% trans "Parol" %}
                    </label>
                    {{ form.password1 }}
                    <small class="form-text">
                        {% trans "Parolingiz juda oddiy bo'lmasligi kerak va kamida 8 belgidan iborat bo'lishi kerak" %}
                    </small>
                    {% if form.password1.errors %}
                        <div class="error-message">{{ form.password1.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="{{ form.password2.id_for_label }}">
                        {% trans "Parolni tasdiqlash" %}
                    </label>
                    {{ form.password2 }}
                    {% if form.password2.errors %}
                        <div class="error-message">{{ form.password2.errors }}</div>
                    {% endif %}
                </div>

                <button type="submit" class="btn btn-primary btn-block">
                    {% trans "Ro'yxatdan o'tish" %}
                </button>
            </form>

            <div class="auth-links">
                <p>
                    {% trans "Hisobingiz bormi?" %}
                    <a href="{% url 'login' %}">
                        {% trans "Tizimga kiring" %}
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Bosqich 8: URLs.py faylini sozlash

### 8.1. config/urls.py

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
    prefix_default_language=False,
)

# Media va static fayllar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Bosqich 9: Tarjima fayllarini yaratish

### 9.1. Barcha matnlarni to'plash

Terminal orqali tarjima fayllarini yaratamiz:

```bash
# Ingliz tili uchun
django-admin makemessages -l en --ignore=venv

# Rus tili uchun
django-admin makemessages -l ru --ignore=venv
```

**Natija:**
```
locale/
    en/
        LC_MESSAGES/
            django.po
    ru/
        LC_MESSAGES/
            django.po
```

### 9.2. locale/en/LC_MESSAGES/django.po faylini to'ldirish

Faylni ochib tarjimalarni qo'shing:

```po
# locale/en/LC_MESSAGES/django.po

msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Language: en\n"

# Base template
msgid "Yangiliklar sayti"
msgstr "News Site"

msgid "Yangiliklar"
msgstr "News"

msgid "Bosh sahifa"
msgstr "Home"

msgid "Aloqa"
msgstr "Contact"

msgid "Kirish"
msgstr "Login"

msgid "Chiqish"
msgstr "Logout"

msgid "Ro'yxatdan o'tish"
msgstr "Sign Up"

#, python-format
msgid "Salom, %(name)s"
msgstr "Hello, %(name)s"

msgid "© 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan."
msgstr "© 2024 News Site. All rights reserved."

# Home page
msgid "Yangiliklar saytiga xush kelibsiz!"
msgstr "Welcome to News Site!"

msgid "Eng so'nggi va dolzarb yangiliklar bilan tanishing"
msgstr "Stay updated with the latest and trending news"

msgid "Barcha yangiliklar"
msgstr "All News"

msgid "Barchasini ko'rish"
msgstr "View All"

#, python-format
msgid "%(name)s kategoriyasida yangiliklar yo'q."
msgstr "No news in %(name)s category."

msgid "O'qish"
msgstr "Read"

# News list
msgid "Yangiliklar ro'yxati"
msgstr "News List"

#, python-format
msgid "Jami %(counter)s ta yangilik"
msgid_plural "Jami %(counter)s ta yangiliklar"
msgstr[0] "Total %(counter)s news"
msgstr[1] "Total %(counter)s news"

msgid "Yangilik qidirish..."
msgstr "Search news..."

msgid "Qidirish"
msgstr "Search"

msgid "Barchasi"
msgstr "All"

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

#, python-format
msgid "Sahifa %(current)s / %(total)s"
msgstr "Page %(current)s of %(total)s"

msgid "Yangiliklar topilmadi"
msgstr "No news found"

msgid "Hozircha yangiliklar yo'q yoki qidiruv natijasi topilmadi."
msgstr "No news available yet or no search results found."

msgid "Barcha yangiliklarni ko'rish"
msgstr "View all news"

# News detail
msgid "Muallif:"
msgstr "Author:"

msgid "Sana:"
msgstr "Date:"

msgid "Ko'rishlar:"
msgstr "Views:"

#, python-format
msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s view"
msgstr[1] "%(counter)s views"

msgid "Tahrirlash"
msgstr "Edit"

msgid "O'chirish"
msgstr "Delete"

msgid "Rostdan ham o'chirmoqchimisiz?"
msgstr "Are you sure you want to delete?"

#, python-format
msgid "%(counter)s ta izoh"
msgid_plural "%(counter)s ta izohlar"
msgstr[0] "%(counter)s comment"
msgstr[1] "%(counter)s comments"

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

msgid "yoki"
msgstr "or"

msgid "ro'yxatdan o'ting"
msgstr "sign up"

msgid "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!"
msgstr "No comments yet. Be the first to comment!"

# Contact page
msgid "Biz bilan bog'laning"
msgstr "Contact Us"

msgid "Sizning fikr va takliflaringizni eshitishdan xursandmiz. Quyidagi forma orqali biz bilan bog'lanishingiz mumkin."
msgstr "We'd love to hear your feedback and suggestions. You can contact us through the form below."

msgid "Xabar yuborish"
msgstr "Send Message"

msgid "Ismingiz"
msgstr "Your Name"

msgid "Email manzilingiz"
msgstr "Your Email"

msgid "Xabaringiz"
msgstr "Your Message"

msgid "Xabarni yuborish"
msgstr "Send Message"

msgid "Aloqa ma'lumotlari"
msgstr "Contact Information"

msgid "Manzil"
msgstr "Address"

msgid "Toshkent, O'zbekiston"
msgstr "Tashkent, Uzbekistan"

msgid "Telefon"
msgstr "Phone"

msgid "Email"
msgstr "Email"

msgid "Ish vaqti"
msgstr "Working Hours"

msgid "Dushanba - Juma: 9:00 - 18:00"
msgstr "Monday - Friday: 9:00 AM - 6:00 PM"

msgid "Dam olish kunlari: Shanba, Yakshanba"
msgstr "Weekends: Saturday, Sunday"

# Authentication
msgid "Tizimga kirish"
msgstr "Login"

msgid "Hisobingizga kirish uchun ma'lumotlaringizni kiriting"
msgstr "Enter your credentials to access your account"

msgid "Foydalanuvchi nomi"
msgstr "Username"

msgid "Parol"
msgstr "Password"

msgid "Parolni unutdingizmi?"
msgstr "Forgot password?"

msgid "Hisobingiz yo'qmi?"
msgstr "Don't have an account?"

msgid "Hisobingiz bormi?"
msgstr "Already have an account?"

msgid "Ro'yxatdan o'tish"
msgstr "Sign Up"

msgid "Yangi hisob yaratish uchun quyidagi ma'lumotlarni to'ldiring"
msgstr "Fill in the information below to create a new account"

msgid "150 belgidan kam. Faqat harflar, raqamlar va @/./+/-/_ belgilar"
msgstr "150 characters or fewer. Letters, digits and @/./+/-/_ only"

msgid "Ism"
msgstr "First Name"

msgid "Familiya"
msgstr "Last Name"

msgid "Email manzil"
msgstr "Email Address"

msgid "Parolni tasdiqlash"
msgstr "Confirm Password"

msgid "Parolingiz juda oddiy bo'lmasligi kerak va kamida 8 belgidan iborat bo'lishi kerak"
msgstr "Your password must not be too simple and should contain at least 8 characters"

msgid "Tizimga kiring"
msgstr "Log In"
```

### 9.3. locale/ru/LC_MESSAGES/django.po faylini to'ldirish

```po
# locale/ru/LC_MESSAGES/django.po

msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Language: ru\n"
"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

# Base template
msgid "Yangiliklar sayti"
msgstr "Новостной сайт"

msgid "Yangiliklar"
msgstr "Новости"

msgid "Bosh sahifa"
msgstr "Главная"

msgid "Aloqa"
msgstr "Контакты"

msgid "Kirish"
msgstr "Войти"

msgid "Chiqish"
msgstr "Выйти"

msgid "Ro'yxatdan o'tish"
msgstr "Регистрация"

#, python-format
msgid "Salom, %(name)s"
msgstr "Привет, %(name)s"

msgid "© 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan."
msgstr "© 2024 Новостной сайт. Все права защищены."

# Home page
msgid "Yangiliklar saytiga xush kelibsiz!"
msgstr "Добро пожаловать на новостной сайт!"

msgid "Eng so'nggi va dolzarb yangiliklar bilan tanishing"
msgstr "Будьте в курсе последних и актуальных новостей"

msgid "Barcha yangiliklar"
msgstr "Все новости"

msgid "Barchasini ko'rish"
msgstr "Смотреть все"

#, python-format
msgid "%(name)s kategoriyasida yangiliklar yo'q."
msgstr "Нет новостей в категории %(name)s."

msgid "O'qish"
msgstr "Читать"

# News list
msgid "Yangiliklar ro'yxati"
msgstr "Список новостей"

#, python-format
msgid "Jami %(counter)s ta yangilik"
msgid_plural "Jami %(counter)s ta yangiliklar"
msgstr[0] "Всего %(counter)s новость"
msgstr[1] "Всего %(counter)s новости"
msgstr[2] "Всего %(counter)s новостей"

msgid "Yangilik qidirish..."
msgstr "Поиск новостей..."

msgid "Qidirish"
msgstr "Поиск"

msgid "Barchasi"
msgstr "Все"

msgid "Batafsil o'qish"
msgstr "Читать подробнее"

msgid "Birinchi"
msgstr "Первая"

msgid "Oldingi"
msgstr "Предыдущая"

msgid "Keyingi"
msgstr "Следующая"

msgid "Oxirgi"
msgstr "Последняя"

#, python-format
msgid "Sahifa %(current)s / %(total)s"
msgstr "Страница %(current)s из %(total)s"

msgid "Yangiliklar topilmadi"
msgstr "Новости не найдены"

msgid "Hozircha yangiliklar yo'q yoki qidiruv natijasi topilmadi."
msgstr "Пока нет новостей или результаты поиска не найдены."

msgid "Barcha yangiliklarni ko'rish"
msgstr "Посмотреть все новости"

# News detail
msgid "Muallif:"
msgstr "Автор:"

msgid "Sana:"
msgstr "Дата:"

msgid "Ko'rishlar:"
msgstr "Просмотры:"

#, python-format
msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s просмотр"
msgstr[1] "%(counter)s просмотра"
msgstr[2] "%(counter)s просмотров"

msgid "Tahrirlash"
msgstr "Редактировать"

msgid "O'chirish"
msgstr "Удалить"

msgid "Rostdan ham o'chirmoqchimisiz?"
msgstr "Вы уверены, что хотите удалить?"

#, python-format
msgid "%(counter)s ta izoh"
msgid_plural "%(counter)s ta izohlar"
msgstr[0] "%(counter)s комментарий"
msgstr[1] "%(counter)s комментария"
msgstr[2] "%(counter)s комментариев"

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

msgid "yoki"
msgstr "или"

msgid "ro'yxatdan o'ting"
msgstr "зарегистрируйтесь"

msgid "Hozircha izohlar yo'q. Birinchi bo'lib izoh qoldiring!"
msgstr "Пока нет комментариев. Будьте первым!"

# Contact page
msgid "Biz bilan bog'laning"
msgstr "Свяжитесь с нами"

msgid "Sizning fikr va takliflaringizni eshitishdan xursandmiz. Quyidagi forma orqali biz bilan bog'lanishingiz mumkin."
msgstr "Мы будем рады услышать ваши отзывы и предложения. Вы можете связаться с нами через форму ниже."

msgid "Xabar yuborish"
msgstr "Отправить сообщение"

msgid "Ismingiz"
msgstr "Ваше имя"

msgid "Email manzilingiz"
msgstr "Ваш Email"

msgid "Xabaringiz"
msgstr "Ваше сообщение"

msgid "Xabarni yuborish"
msgstr "Отправить сообщение"

msgid "Aloqa ma'lumotlari"
msgstr "Контактная информация"

msgid "Manzil"
msgstr "Адрес"

msgid "Toshkent, O'zbekiston"
msgstr "Ташкент, Узбекистан"

msgid "Telefon"
msgstr "Телефон"

msgid "Email"
msgstr "Email"

msgid "Ish vaqti"
msgstr "Рабочее время"

msgid "Dushanba - Juma: 9:00 - 18:00"
msgstr "Понедельник - Пятница: 9:00 - 18:00"

msgid "Dam olish kunlari: Shanba, Yakshanba"
msgstr "Выходные: Суббота, Воскресенье"

# Authentication
msgid "Tizimga kirish"
msgstr "Вход в систему"

msgid "Hisobingizga kirish uchun ma'lumotlaringizni kiriting"
msgstr "Введите свои данные для входа в аккаунт"

msgid "Foydalanuvchi nomi"
msgstr "Имя пользователя"

msgid "Parol"
msgstr "Пароль"

msgid "Parolni unutdingizmi?"
msgstr "Забыли пароль?"

msgid "Hisobingiz yo'qmi?"
msgstr "Нет аккаунта?"

msgid "Hisobingiz bormi?"
msgstr "Уже есть аккаунт?"

msgid "Ro'yxatdan o'tish"
msgstr "Регистрация"

msgid "Yangi hisob yaratish uchun quyidagi ma'lumotlarni to'ldiring"
msgstr "Заполните информацию ниже, чтобы создать новый аккаунт"

msgid "150 belgidan kam. Faqat harflar, raqamlar va @/./+/-/_ belgilar"
msgstr "150 символов или меньше. Только буквы, цифры и @/./+/-/_"

msgid "Ism"
msgstr "Имя"

msgid "Familiya"
msgstr "Фамилия"

msgid "Email manzil"
msgstr "Email адрес"

msgid "Parolni tasdiqlash"
msgstr "Подтвердите пароль"

msgid "Parolingiz juda oddiy bo'lmasligi kerak va kamida 8 belgidan iborat bo'lishi kerak"
msgstr "Ваш пароль не должен быть слишком простым и должен содержать не менее 8 символов"

msgid "Tizimga kiring"
msgstr "Войти"
```

## Bosqich 10: Tarjimalarni kompilyatsiya qilish

### 10.1. Tarjimalarni kompilyatsiya qilish

Terminal orqali:

```bash
django-admin compilemessages
```

**Muvaffaqiyatli natija:**
```
processing file django.po in locale/en/LC_MESSAGES
processing file django.po in locale/ru/LC_MESSAGES
```

### 10.2. Natijani tekshirish

Server'ni ishga tushiring:

```bash
python manage.py runserver
```

Brauzerda `http://127.0.0.1:8000/` ga kiring va til tanlash menyusidan tilni o'zgartiring.

## Bosqich 11: CSS stillarini qo'shish (Ixtiyoriy)

### 11.1. static/css/style.css

Til tanlash uchun stillar:

```css
/* Til tanlash menyu */
.language-selector {
    margin-left: auto;
}

.language-dropdown {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.language-dropdown:hover {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

.language-dropdown:focus {
    outline: none;
    border-color: #007bff;
}

/* Navbar responsive */
@media (max-width: 768px) {
    .language-selector {
        margin: 10px 0;
    }
    
    .language-dropdown {
        width: 100%;
    }
}
```

## Bosqich 12: Xatolarni tuzatish

### 12.1. Tarjima ko'rinmasa

**Muammo:** Tilni o'zgartirganimda tarjima ko'rinmayapti

**Yechim:**
```bash
# 1. Server'ni to'xtating (Ctrl+C)
# 2. Tarjimalarni qayta kompilyatsiya qiling
django-admin compilemessages

# 3. Server'ni qayta ishga tushiring
python manage.py runserver
```

### 12.2. Ko'plik shakllar ishlamasa

**Muammo:** Ko'plik shakllar (plural) noto'g'ri ko'rinmoqda

**Yechim:** `.po` faylda ko'plik shakl to'g'ri yozilganligini tekshiring:

```po
#, python-format
msgid "%(counter)s ko'rish"
msgid_plural "%(counter)s ko'rishlar"
msgstr[0] "%(counter)s view"
msgstr[1] "%(counter)s views"
```

Rus tili uchun 3 ta shakl kerak:
```po
msgstr[0] "%(counter)s просмотр"     # 1, 21, 31...
msgstr[1] "%(counter)s просмотра"    # 2-4, 22-24...
msgstr[2] "%(counter)s просмотров"   # 5-20, 25-30...
```

### 12.3. Yangi matnlar qo'shganda

**Qadamlar:**
```bash
# 1. Yangi tarjima kerakli matnlarni template'ga qo'shing
# 2. Tarjima fayllarini yangilang
django-admin makemessages -l en --ignore=venv
django-admin makemessages -l ru --ignore=venv

# 3. .po fayllarni ochib yangi tarjimalarni qo'shing
# 4. Kompilyatsiya qiling
django-admin compilemessages

# 5. Server'ni qayta ishga tushiring
python manage.py runserver
```

### 12.4. LocaleMiddleware ishlamasa

**Tekshirish kerak:**

1. `settings.py` da `USE_I18N = True` ekanligini
2. `LocaleMiddleware` to'g'ri joyda ekanligini:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Bu yerda
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

3. `urls.py` da `i18n_patterns` ishlatilganligini

## Bosqich 13: Testlar

### 13.1. Barcha sahifalarni tekshirish

Har bir sahifada tilni o'zgartirib ko'ring:

1. ✅ Bosh sahifa (`/`)
2. ✅ Yangiliklar ro'yxati (`/news/`)
3. ✅ Yangilik detali (`/news/slug/`)
4. ✅ Kontakt sahifa (`/contact/`)
5. ✅ Login sahifa (`/accounts/login/`)
6. ✅ Signup sahifa (`/accounts/signup/`)

### 13.2. O'zgaruvchilarni tekshirish

Quyidagilarni tekshiring:

1. ✅ Foydalanuvchi nomi to'g'ri ko'rinmoqda
2. ✅ Ko'rishlar soni to'g'ri (1 ko'rish / 5 ko'rishlar)
3. ✅ Izohlar soni to'g'ri (1 ta izoh / 5 ta izohlar)
4. ✅ Sana formatlari to'g'ri
5. ✅ Pagination to'g'ri ishlayapti

### 13.3. URL'larni tekshirish

URL'larda til prefiksi to'g'ri qo'shilganligini tekshiring:

- O'zbek: `http://127.0.0.1:8000/news/`
- Ingliz: `http://127.0.0.1:8000/en/news/`
- Rus: `http://127.0.0.1:8000/ru/news/`

## Bosqich 14: GitHub'ga yuklash

### 14.1. O'zgarishlarni saqlash

```bash
# 1. Git status
git status

# 2. Barcha o'zgarishlarni qo'shish
git add .

# 3. Commit
git commit -m "Template matnlarini tarjima qilish - lesson 52

- Barcha template'larga i18n teglari qo'shildi
- Ingliz va rus tillariga tarjima qo'shildi
- Til tanlash menyu qo'shildi
- URL'larga til prefiksi qo'shildi"

# 4. GitHub'ga push
git push origin main
```

## Xulosa

Ushbu amaliyotda biz:

✅ **Barcha template'larni tarjima qildik:**
- base.html
- index.html (home)
- news_list.html
- news_detail.html
- contact.html
- login.html
- signup.html

✅ **Tarjima tizimini to'liq sozladik:**
- `{% trans %}` va `{% blocktrans %}` teglarini ishlatdik
- O'zgaruvchilar bilan ishladik
- Ko'plik shakllarni to'g'ri yozdik

✅ **Tarjima fayllarini yaratdik:**
- Ingliz tili (en)
- Rus tili (ru)
- Barcha matnlarni tarjima qildik

✅ **Til tanlash funksiyasini qo'shdik:**
- Navbar'da til tanlash menyu
- URL'larda til prefiksi
- Avtomatik til o'zgartirish

## Keyingi qadam

**lesson_52** da biz model maydonlarini (database ma'lumotlarini) tarjima qilishni o'rganamiz - **ModelTranslation** moduli bilan ishlash.

## Qo'shimcha topshiriqlar

1. **Profil sahifasini tarjima qiling** - foydalanuvchi profil sahifasidagi barcha matnlarni tarjima qiling
2. **Form xatolarini tarjima qiling** - validatsiya xatolarini ham tarjima qiling
3. **Admin panelni tarjima qiling** - admin panel uchun ham tarjima qo'shing
4. **SEO uchun hreflang teglar qo'shing** - har bir til uchun hreflang meta teglar qo'shing

## Foydali linklar

- [Django i18n documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [Translation guidelines](https://docs.djangoproject.com/en/stable/topics/i18n/translation/)
- [Locale documentation](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-LOCALE_PATHS)